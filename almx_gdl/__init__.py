# -*- coding: utf-8 -*-
from . import models


def pre_init_hook(env):
    """El grupo 'Acceso Multi-Almacén GDL' (id 603) existía en 16 con un xmlid
    creado a mano vía RPC bajo un módulo ficticio (doppler_custom), y llegó así
    a 19 con sus miembros. Se reasigna ese xmlid a este módulo ANTES de cargar
    security.xml, para que la declaración del grupo actualice el registro
    existente (conservando a sus usuarios) en lugar de crear uno nuevo."""
    env.cr.execute("""
        UPDATE ir_model_data
           SET module = 'almx_gdl'
         WHERE module = 'doppler_custom'
           AND name = 'group_acceso_multialmacen_gdl'
           AND model = 'res.groups'
           AND NOT EXISTS (
               SELECT 1 FROM ir_model_data
                WHERE module = 'almx_gdl' AND name = 'group_acceso_multialmacen_gdl')
    """)
