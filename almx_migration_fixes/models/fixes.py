import logging

from odoo import api, models

_logger = logging.getLogger(__name__)

# Tipos de vista que Odoo no puede generar por defecto sin campos específicos.
VIEW_TYPES_NEEDING_ARCH = ('gantt', 'cohort', 'calendar', 'map', 'grid')

# (modelo del reporte, nombres posibles del grupo en 19/16) -> lectura
REPORT_ACCESS = [
    ('purchase.report', 390, ['Report - Compras', 'Report']),
    ('stock.report', 388, ['Report - Inventario', 'Report']),
]


class AlmxMigrationFixes(models.AbstractModel):
    _name = 'almx.migration.fixes'
    _description = 'Correcciones post-migración Alamex'

    @api.model
    def run_all(self):
        self._fix_window_actions()
        self._fix_menu_icons()
        self._fix_report_access()
        return True

    @api.model
    def _fix_window_actions(self):
        Views = self.env['ir.ui.view'].sudo().with_context(active_test=False)
        actions = self.env['ir.actions.act_window'].sudo().search([])
        for action in actions:
            if not action.res_model or action.res_model not in self.env:
                continue
            modes = [m.strip() for m in (action.view_mode or '').split(',') if m.strip()]
            bad = [m for m in modes if m in VIEW_TYPES_NEEDING_ARCH
                   and not Views.search_count([('model', '=', action.res_model), ('type', '=', m)], limit=1)]
            if not bad:
                continue
            action.view_ids.filtered(lambda v: v.view_mode in bad and not v.view_id).unlink()
            action.view_mode = ','.join(m for m in modes if m not in bad)
            _logger.info('almx_migration_fixes: acción %s (%s) sin vista %s -> quitado de view_mode',
                         action.id, action.res_model, bad)

    @api.model
    def _fix_menu_icons(self):
        menus = self.env['ir.ui.menu'].sudo().with_context(active_test=False).search(
            [('parent_id', '=', False), ('web_icon', '!=', False)])
        for menu in menus.filtered(lambda m: not m.web_icon_data):
            menu.write({'web_icon': menu.web_icon})  # write() regenera web_icon_data
            _logger.info('almx_migration_fixes: ícono regenerado para el menú %s', menu.name)

    @api.model
    def _fix_report_access(self):
        Groups = self.env['res.groups'].sudo()
        Access = self.env['ir.model.access'].sudo()
        for model_name, group_id, names in REPORT_ACCESS:
            model = self.env['ir.model'].sudo().search([('model', '=', model_name)], limit=1)
            group = Groups.browse(group_id).exists() or Groups.search([('name', 'in', names)], limit=1)
            if not (model and group):
                continue
            if not Access.search_count([('model_id', '=', model.id), ('group_id', '=', group.id), ('perm_read', '=', True)]):
                Access.create({'name': '%s read (%s)' % (model_name, group.name), 'model_id': model.id,
                               'group_id': group.id, 'perm_read': True})
                _logger.info('almx_migration_fixes: lectura de %s para el grupo %s', model_name, group.name)
