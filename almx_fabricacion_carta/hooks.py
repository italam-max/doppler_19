def post_init_hook(env):
    """Configura las etapas del proyecto Instalaciones como estaban fijas en el código de 16.

    260 PROYECTOS NUEVOS -> 229 EN FABRICACION : Carta de Fabricación (ANX-07)
    229 EN FABRICACION   -> 23  CHECK Y ALMACEN : Carta de Llegada a Almacén (ANX-09)
    La etapa 2270 TERMINO DE FABRICACION (ANX-08) ya no existe en 16 ni en 19: se configura
    a mano en la etapa si se vuelve a crear.
    """
    Stage = env['project.task.type']
    config = [
        (229, 'fabricacion', [260]),
        (23, 'llegada_almacen', [229]),
    ]
    for dest_id, code, origin_ids in config:
        dest = Stage.browse(dest_id).exists()
        origins = Stage.browse(origin_ids).exists()
        if dest and origins:
            dest.write({'almx_carta_code': code, 'almx_carta_origin_stage_ids': [(6, 0, origins.ids)]})
