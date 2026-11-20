# -*- coding: utf-8 -*-
{
    'name': 'ALMX Candado de chatter',
    'version': '19.0.1.0.0',
    'summary': 'Nadie edita ni elimina mensajes del chatter (ni sus adjuntos), salvo el grupo autorizado.',
    'description': """
ALMX Candado de chatter
=========================

Política de Dirección: no se puede eliminar nada del sistema, incluidos los
comentarios del chatter. Solo los usuarios del grupo "Chatter: puede editar
y eliminar mensajes" (Hamdi y Sammer) quedan exentos.

Qué bloquea (en el chatter de cualquier registro; NO en chats de Conversaciones):
- Editar el texto de un mensaje o nota (también evita "borrar" dejando un punto).
- Eliminar un mensaje o nota.
- Quitar adjuntos de un mensaje ya publicado.
- unlink directo de mail.message por RPC.

Qué NO toca:
- Seguidores (agregar/quitar sigue igual).
- Reacciones, marcar como leído, destacar.
- Quitar un adjunto en el editor ANTES de publicar.
- Procesos internos de Odoo que corren con sudo (p. ej. borrar un registro
  con su historial).

Changelog
----------
- 19.0.1.0.0: Versión inicial.
""",
    'author': 'Irving Sammer González Correa',
    'category': 'Productivity/Discuss',
    'depends': ['mail'],
    'data': [
        'security/security.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'almx_chatter_lock/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
