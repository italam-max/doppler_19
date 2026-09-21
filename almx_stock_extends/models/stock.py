# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError, UserError
from datetime import date
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    not_validate = fields.Boolean(string='No se puede validar', help='Muestra si la condición de pagado aplica para la orden de venta relacionada al movimiento de almacén actual', compute='compute_spare_sale_order')
    detect_move_type = fields.Boolean(string='Tipo de movimiento', compute='compute_picking_type_move')
    pick_move = fields.Boolean(string='Es un PICK')
    out_move = fields.Boolean(string='Es un OUT')
    in_move = fields.Boolean(string='Es un IN')

    @api.depends('picking_type_id.sequence_code')
    def compute_picking_type_move(self):
        for rec in self:
            sequence_code = rec.picking_type_id.sequence_code
            move_flags = {
                'NWH/PICK/': 'pick_move',
                'NWH/OUT/': 'out_move',
                'NWH/IN/': 'in_move',
            }

            rec.pick_move = rec.out_move = rec.in_move = False

            move_attr = move_flags.get(sequence_code)
            if move_attr:
                setattr(rec, move_attr, True)
                rec.detect_move_type = True
            else:
                rec.detect_move_type = False

    def compute_spare_sale_order(self):
        op_type = self.picking_type_id.id
        sale_type = self.x_studio_tipo_de_venta
        comp_paid = self.x_studio_completamente_pagado
        if sale_type == 'spare' and comp_paid != True and op_type == 2: #Aplica solo para movimientos que son OUT
            self.not_validate = True
        else:
            self.not_validate = False

    # ------------------------------------------------------------------
    # ALMX FIX (blindaje enlace PICK/OUT manual, ago 2026):
    # action_create_related_out/action_create_related_int ya enlazan
    # move_orig_ids/move_dest_ids correctamente -- pero SOLO cuando se usa
    # el botón. Cuando un PICK/OUT manual se crea a mano (o se duplica un
    # traslado existente) y related_pick_id/related_out_id se llenan
    # directamente en el formulario, ese enlace nunca se ejecutaba, y el
    # OUT quedaba sin poder reservar la existencia que su propio PICK
    # generó (puede perderla ante otra orden que estaba esperando el mismo
    # producto). Este bloque reproduce el mismo enlace nativo sin importar
    # cómo se haya creado el par PICK/OUT, cada vez que se guarda el
    # traslado con related_pick_id/related_out_id o con líneas nuevas.
    # ------------------------------------------------------------------
    def _almx_sync_pick_out_move_chain(self, pick_picking, out_picking):
        """Enlaza (move_orig_ids/move_dest_ids) los movimientos del PICK
        con los del OUT relacionado, emparejando por producto. Idempotente
        (seguro de llamar varias veces) y defensivo: exige que ambos
        traslados compartan el mismo 'origin' (misma orden/referencia)
        antes de tocar cualquier movimiento, para no encadenar por error
        movimientos de pedidos distintos.

        ALMX FIX (hotfix ago 2026): durante un create() en el que la
        vista manda las líneas de movimiento junto con el encabezado
        (move_ids_without_package ya viene poblado en el mismo create),
        Odoo procesa el inverse de ese campo ANTES de que los stock.move
        recién creados tengan un id real -- en ese momento su id es un
        NewId (marcador interno, no un entero de la base de datos
        todavía). Si en ese punto se intenta escribir move_orig_ids/
        move_dest_ids referenciando ese NewId, psycopg2 truena con
        "can't adapt type 'NewId'" porque intenta mandar ese valor
        directo a una consulta SQL. Este bloque detecta esa situación y
        simplemente no hace nada todavía -- el propio create() de este
        modelo (más abajo) vuelve a llamar este mismo enlace justo
        después de que super().create() termina, momento en el que todos
        los ids ya son reales.
        """
        if not pick_picking or not out_picking:
            return
        if not (pick_picking.pick_move and out_picking.out_move):
            return
        if not pick_picking.origin or pick_picking.origin != out_picking.origin:
            return

        pick_moves = pick_picking.move_ids_without_package
        out_moves = out_picking.move_ids_without_package

        if any(isinstance(m.id, models.NewId) for m in pick_moves | out_moves):
            return

        for product in out_moves.product_id:
            pending_pick = pick_moves.filtered(
                lambda m, p=product: m.product_id == p and not (m.move_dest_ids & out_moves)
            )
            pending_out = out_moves.filtered(
                lambda m, p=product: m.product_id == p and not (m.move_orig_ids & pick_moves)
            )
            for p_move, o_move in zip(pending_pick, pending_out):
                o_move.write({'move_orig_ids': [(4, p_move.id)]})
                p_move.write({'move_dest_ids': [(4, o_move.id)]})

    def _almx_autolink_related_moves(self):
        for picking in self:
            if isinstance(picking.id, models.NewId):
                continue
            if picking.related_pick_id:
                picking._almx_sync_pick_out_move_chain(picking.related_pick_id, picking)
            if picking.related_out_id:
                picking._almx_sync_pick_out_move_chain(picking, picking.related_out_id)

    # ------------------------------------------------------------------
    # ALMX FIX (autoenlace PICK/OUT automáticos, sep 2026):
    # related_pick_id/related_out_id solo se llenaban cuando el par se
    # creaba con el botón "Crear OUT"/"Crear INT", o a mano en el
    # formulario. Cuando el PICK y el OUT los genera el motor de
    # aprovisionamiento nativo de Odoo (al confirmar una orden de venta
    # -- así se crea la mayoría), nada llenaba estos campos: quedaban
    # vacíos, y por lo tanto _almx_sync_pick_out_move_chain (arriba)
    # tampoco se disparaba nunca para ellos.
    #
    # OJO -- un enfoque parecido a este YA se intentó antes y se revirtió
    # (ver relational_moves en transfer_relation.py y el changelog
    # 16.0.1.0.7): esa versión buscaba pickings con
    # [('group_id', '=', False)], y como los traslados MANUALES casi
    # nunca tienen group_id, ese filtro devolvía traslados de CUALQUIER
    # otra orden sin relación alguna y pisaba related_pick_id/
    # related_out_id con el par equivocado cada vez que se leía el
    # campo. Este método evita exactamente ese punto de falla: solo
    # actúa cuando 'group_id' SÍ tiene un valor real (nunca sobre
    # False/vacío), y usa ese group_id -- que Odoo asigna de forma única
    # por aprovisionamiento -- para emparejar, no un valor compartido
    # por cualquier registro sin grupo. Además, solo enlaza cuando hay
    # EXACTAMENTE un PICK y un OUT en ese grupo; si hay más de uno
    # (backorders, entregas parciales, reintentos tras cancelación), no
    # adivina -- lo deja sin tocar para revisión manual, igual que se
    # hizo con los 96 casos "con ruido" del backfill manual de
    # jul-sep 2026. Tampoco pisa un related_pick_id/related_out_id que
    # ya tenga un valor (manual o del botón).
    #
    # Identifica PICK/OUT leyendo picking_type_id.sequence_code
    # DIRECTAMENTE ('NWH/PICK/', 'NWH/OUT/') en vez de usar los campos
    # pick_move/out_move ya existentes en este archivo -- se probó con
    # pick_move/out_move primero y falló: esos dos son campos
    # ordinarios (sin `compute=` en su propia declaración), así que Odoo
    # SOLO los recalcula como efecto secundario de compute_picking_type_move,
    # el cual solo se dispara cuando algo lee 'detect_move_type' (el
    # único campo que sí declara ese compute). Un picking recién creado
    # que nadie ha abierto todavía trae pick_move/out_move en False
    # aunque su tipo de operación sea el correcto -- confirmado en vivo
    # al probar este método contra un PICK/OUT de prueba recién creados.
    # Leer picking_type_id.sequence_code no tiene ese problema: es un
    # campo real de stock.picking.type, no depende de que algo más lo
    # haya "despertado" antes.
    #
    # Por ahora solo cubre el almacén NWH (igual que pick_move/out_move
    # y relational_moves, ya con ese mismo alcance). Para extender a GDL
    # u otro almacén habría que revisar sus sequence_code o usar
    # warehouse_id.pick_type_id/out_type_id en su lugar.
    # ------------------------------------------------------------------
    def _almx_autolink_related_ids_from_group(self):
        def _seq(p):
            return p.picking_type_id.sequence_code

        candidates = self.filtered(
            lambda p: not isinstance(p.id, models.NewId)
            and p.group_id
            and _seq(p) in ('NWH/PICK/', 'NWH/OUT/')
            and not (p.related_pick_id or p.related_out_id)
        )
        if not candidates:
            return

        group_ids = candidates.group_id.ids
        siblings = self.env['stock.picking'].search([('group_id', 'in', group_ids)])

        by_group = {}
        for p in siblings:
            bucket = by_group.setdefault(p.group_id.id, {'picks': [], 'outs': []})
            seq = _seq(p)
            if seq == 'NWH/PICK/':
                bucket['picks'].append(p)
            elif seq == 'NWH/OUT/':
                bucket['outs'].append(p)

        for group_id in group_ids:
            bucket = by_group.get(group_id, {'picks': [], 'outs': []})
            picks, outs = bucket['picks'], bucket['outs']
            # Conservador: solo el caso inequívoco 1 PICK + 1 OUT.
            if len(picks) != 1 or len(outs) != 1:
                continue
            pick, out = picks[0], outs[0]
            if not out.related_pick_id:
                out.related_pick_id = pick.id
            if not pick.related_out_id:
                pick.related_out_id = out.id

    # ------------------------------------------------------------------
    # ALMX FIX (autoenlace PICK/OUT automáticos, sep 2026 -- por qué
    # existe también un cron, y no solo el hook inmediato de abajo):
    # Se probó primero enganchando esto en stock.picking.create() (igual
    # que _almx_autolink_related_moves). Falló contra un PICK/OUT de
    # prueba recién creados: 'group_id' es un related field a
    # move_ids.group_id -- y en el flujo nativo de Odoo el picking se
    # crea VACÍO primero; los stock.move se le asignan después, con un
    # write() de picking_id sobre el move, ya en otro paso del motor de
    # aprovisionamiento. O sea que dentro del propio create() del
    # picking, group_id casi nunca está disponible todavía.
    #
    # El enlace inmediato real vive ahora en StockMove.write() (más
    # abajo en este archivo), reaccionando exactamente a ese momento --
    # cuando al move se le asigna picking_id. Este cron se deja como
    # RED DE SEGURIDAD, no como mecanismo principal: por si algún
    # picking_id se llegara a escribir por un camino que no pase por
    # StockMove.write() (o si esa lógica llegara a fallar en algún caso
    # puntual y el try/except la absorbe silenciosamente), esto lo
    # alcanza a corregir en un máximo de 10 minutos en vez de quedar
    # huérfano para siempre. Barre solo lo creado en los últimos N días
    # (por default 7) para que cada corrida sea rápida.
    # ------------------------------------------------------------------
    @api.model
    def _cron_almx_autolink_related_ids(self, days=7):
        since = fields.Datetime.subtract(fields.Datetime.now(), days=days)
        candidates = self.search([
            ('picking_type_id.sequence_code', 'in', ('NWH/PICK/', 'NWH/OUT/')),
            ('group_id', '!=', False),
            ('related_pick_id', '=', False),
            ('related_out_id', '=', False),
            ('create_date', '>=', since),
        ])
        candidates._almx_autolink_related_ids_from_group()
        # Con related_pick_id/related_out_id ya llenos, el enlace nativo
        # move_orig_ids/move_dest_ids se dispara solo (sin cambios,
        # desde la 16.0.1.0.7).
        candidates._almx_autolink_related_moves()

    @api.model_create_multi
    def create(self, vals_list):
        pickings = super().create(vals_list)
        pickings._almx_autolink_related_moves()
        return pickings

    def write(self, vals):
        res = super().write(vals)
        # ALMX FIX (hotfix ago 2026): 'move_ids' se quitó de este set.
        # Odoo escribe 'move_ids' internamente como parte de procesar el
        # inverse de 'move_ids_without_package' DURANTE un create() (ver
        # _set_move_without_package en addons/stock/models/stock_picking.py) --
        # reaccionar a ese write interno reintroducía este mismo método
        # mientras el picking/los moves todavía podían ser NewId, causando
        # el crash de psycopg2. 'move_ids_without_package' sigue en la
        # lista porque ese sí es el campo que el formulario realmente
        # escribe cuando el usuario guarda a mano -- y para ese caso ya
        # existe el guard de NewId arriba como red de seguridad adicional.
        trigger_fields = {'related_pick_id', 'related_out_id', 'move_ids_without_package'}
        if trigger_fields & set(vals.keys()):
            self._almx_autolink_related_moves()
        return res

    def action_set_to_draft(self):
        if self.state not in ('draft', 'done'):
            self.action_clear_quantities_to_zero()
            self.do_unreserve()
            move = self.env['stock.move'].search([('picking_id', '=', self.id)])
            for each in move:
                each.state = 'draft'
            self.state = 'draft'

    def action_create_related_out(self):
        self.ensure_one()
        if self.state == 'done':
            # Encuentra el tipo de operación "Delivery Orders"
            picking_type_out = self.env['stock.picking.type'].search([('sequence_code', '=', 'NWH/OUT/'),('warehouse_id', '=', self.picking_type_id.warehouse_id.id)], limit=1)

            # ALMX FIX (changelog 16.0.1.0.1): la ubicación de destino real
            # del OUT es la del cliente -- NO la misma ubicación de destino
            # del PICK. Antes este método copiaba 'location_dest_id'
            # directamente del PICK (p. ej. Almacén 1), dejando el OUT
            # generado como "Almacén 1 -> Almacén 1" en vez de
            # "Almacén 1 -> Cliente". Se usa la ubicación de cliente
            # específica del partner si existe; si no, el destino por
            # defecto configurado en el propio tipo de operación OUT
            # (que normalmente ya es la ubicación de Clientes).
            out_location_dest = (
                self.partner_id.property_stock_customer
                or picking_type_out.default_location_dest_id
                or self.location_dest_id
            )

            picking_vals = {
                'partner_id': self.partner_id.id,
                'picking_type_id': picking_type_out.id,
                # ALMX FIX: el ORIGEN del OUT es el DESTINO del PICK
                # (a donde llegó la mercancía), no su mismo origen.
                'location_id': self.location_dest_id.id,
                'location_dest_id': out_location_dest.id,
                'origin': self.origin,
                'move_type': self.move_type,
                'company_id': self.company_id.id,
                # ALMX FIX: usar el campo que este mismo módulo ya define
                # para esto (antes nunca se llenaba).
                'related_pick_id': self.id,
            }

            picking_out = self.env['stock.picking'].create(picking_vals)
            # ALMX FIX: reflejar también el enlace en el PICK original.
            self.related_out_id = picking_out.id

            # Crear los movimientos
            for move in self.move_ids_without_package:
                new_move = self.env['stock.move'].create({
                    'name': move.name,
                    'product_id': move.product_id.id,
                    'product_uom_qty': move.quantity,
                    'product_uom': move.product_uom.id,
                    'picking_id': picking_out.id,
                    # ALMX FIX (changelog 16.0.1.0.5): el origen del move debe
                    # ser el DESTINO del move del PICK (donde quedó la
                    # mercancía físicamente), igual que ya se hace a nivel de
                    # picking (picking_vals). Antes se copiaba
                    # move.location_id (el origen del PICK, p. ej. Stock
                    # Doppler), donde ya no queda existencia -- por eso
                    # "Comprobar disponibilidad" no encontraba nada que
                    # reservar aunque la mercancía sí estaba disponible en
                    # Almacén 1.
                    'location_id': picking_out.location_id.id,
                    'location_dest_id': picking_out.location_dest_id.id,
                    'company_id': self.company_id.id,
                })
                # ALMX FIX: enlazar de forma NATIVA el movimiento nuevo con
                # el movimiento del PICK que lo originó (move_orig_ids /
                # move_dest_ids). Sin esto, Odoo no tiene manera de saber
                # que este OUT viene de este PICK -- rompe la
                # trazabilidad nativa (de la que dependen, entre otras
                # cosas, las devoluciones para saber a qué ubicación
                # regresar la mercancía).
                new_move.write({'move_orig_ids': [(4, move.id)]})
                move.write({'move_dest_ids': [(4, new_move.id)]})

            return {
                'type': 'ir.actions.act_window',
                'name': 'Salida Generada',
                'res_model': 'stock.picking',
                'res_id': picking_out.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_create_related_int(self):
        self.ensure_one()
        if self.state == 'done':
            # Encuentra el tipo de operación "Delivery Orders"
            picking_type_out = self.env['stock.picking.type'].search([('sequence_code', '=', 'NWH/INT/'), ('warehouse_id', '=', self.picking_type_id.warehouse_id.id)], limit=1)
            # NOTA (changelog 16.0.1.0.1): a diferencia de action_create_related_out,
            # AQUÍ NO se corrigieron las ubicaciones (location_id/location_dest_id
            # siguen copiándose igual que antes, tal cual del picking IN
            # original) porque no está confirmado cuál es el comportamiento
            # esperado de negocio para "Crear INT" -- revisar con el equipo
            # antes de tocarlo.
            picking_vals = {
                'partner_id': self.partner_id.id,
                'picking_type_id': picking_type_out.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'origin': self.origin,
                'move_type': self.move_type,
                'company_id': self.company_id.id,
                # ALMX FIX: mismo enlace visual que en action_create_related_out.
                'related_pick_id': self.id,
            }

            picking_out = self.env['stock.picking'].create(picking_vals)
            self.related_out_id = picking_out.id

            # Crear los movimientos
            for move in self.move_ids_without_package:
                new_move = self.env['stock.move'].create({
                    'name': move.name,
                    'product_id': move.product_id.id,
                    'product_uom_qty': move.quantity,
                    'product_uom': move.product_uom.id,
                    'picking_id': picking_out.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': picking_out.location_dest_id.id,
                    'company_id': self.company_id.id,
                })
                # ALMX FIX: enlace nativo move_orig_ids/move_dest_ids,
                # mismo motivo que en action_create_related_out.
                new_move.write({'move_orig_ids': [(4, move.id)]})
                move.write({'move_dest_ids': [(4, new_move.id)]})

            return {
                'type': 'ir.actions.act_window',
                'name': 'Transferencia Generada',
                'res_model': 'stock.picking',
                'res_id': picking_out.id,
                'view_mode': 'form',
                'target': 'current',
            }


class StockMove(models.Model):
    _inherit = 'stock.move'

    # ------------------------------------------------------------------
    # ALMX FIX (autoenlace PICK/OUT automáticos, sep 2026 -- versión
    # inmediata): este es el mecanismo PRINCIPAL para enlazar
    # related_pick_id/related_out_id cuando el PICK/OUT lo genera el
    # motor de aprovisionamiento nativo (el cron de
    # _cron_almx_autolink_related_ids en stock.py es solo la red de
    # seguridad -- ver el comentario ahí para el detalle completo).
    #
    # 'picking_id' es justo el campo que el motor de aprovisionamiento
    # escribe sobre el move cuando lo asigna a un picking recién creado
    # (ver _assign_picking en el stock nativo de Odoo) -- ese es el
    # instante exacto en que, del lado del picking, 'group_id'
    # (related a move_ids.group_id) pasa a tener el valor real que
    # _almx_autolink_related_ids_from_group necesita para emparejar.
    # Enganchar aquí, en vez de esperar al cron, hace el enlace
    # inmediato en vez de con hasta 10 minutos de rezago.
    #
    # stock.move es un modelo de tráfico mucho más alto que
    # stock.picking (cada reserva, cada cambio de cantidad pasa por su
    # write()) -- por eso el guard de 'picking_id' in vals va PRIMERO y
    # es la única condición que se evalúa en el caso común, para que el
    # costo extra sea prácticamente cero en el resto de los writes que
    # no tocan picking_id. Cuando sí aplica, todo el trabajo real ocurre
    # en estos otros dos métodos, que además YA existen desde antes en
    # este módulo:
    #   - _almx_autolink_related_ids_from_group: emparejamiento
    #     conservador por group_id (nunca sobre False/vacío, nunca más
    #     de 1 PICK o 1 OUT por grupo -- ver su docstring en stock.py).
    #   - _almx_autolink_related_moves: enlaza move_orig_ids/
    #     move_dest_ids una vez que related_pick_id/related_out_id
    #     quedan llenos (existe desde la 16.0.1.0.7, sin cambios).
    #
    # Envuelto en try/except: un fallo aquí es un enlace de trazabilidad
    # que no se hizo, no una razón para tumbar la asignación real del
    # move a su picking (que ya corrió, vía super().write(), antes de
    # llegar a este bloque).
    # ------------------------------------------------------------------
    def write(self, vals):
        res = super().write(vals)
        if vals.get('picking_id'):
            try:
                pickings = self.mapped('picking_id').filtered(
                    lambda p: not isinstance(p.id, models.NewId)
                )
                if pickings:
                    pickings._almx_autolink_related_ids_from_group()
                    pickings._almx_autolink_related_moves()
            except Exception:
                import logging

                logging.getLogger(__name__).exception(
                    "almx_stock_extends: fallo al autoenlazar "
                    "related_pick_id/related_out_id desde "
                    "StockMove.write (picking_id) para %s",
                    self.mapped("picking_id.name"),
                )
        return res
