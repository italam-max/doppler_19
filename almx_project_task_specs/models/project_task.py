from odoo import api, fields, models

# IDs de los proyectos donde se muestra la pestaña "Características del Proyecto"
PROJECT_FEATURES_PROJECT_IDS = [31,135]

YES_NO = [('yes', 'Sí'), ('no', 'No')]

class ProjectTask(models.Model):
    _inherit = 'project.task'

    show_project_features = fields.Boolean(
        string='Mostrar características del proyecto',
        compute='_compute_show_project_features',
    )

    @api.depends('project_id')
    def _compute_show_project_features(self):
        for task in self:
            task.show_project_features = task.project_id.id in PROJECT_FEATURES_PROJECT_IDS

    # ------------------------------------------------------------------
    # Configuración general
    # ------------------------------------------------------------------
    plan_delivery_date = fields.Date(string='Fecha estimada de entrega del plano')
    installation_type = fields.Selection(
        [
            ('residential', 'Residencial'),
            ('commercial', 'Comercial'),
            ('government', 'Gobierno'),
            ('hospital', 'Hospital'),
        ],
        string='Tipo de Instalación',
    )
    existing_building = fields.Selection(YES_NO, string='Edificio Existente')
    elevator_model = fields.Selection(
        [
            ('mr', 'Con cuarto de Máquina (MR)'),
            ('mrl_l', 'Sin cuarto de Máquina (MRL-L)'),
            ('mrl_g', 'Sin cuarto de Máquinas (MRL-G)'),
            ('hyd', 'Hidráulico (HyD)'),
            ('platform', 'Plataforma'),
            ('car_stacker', 'Apila Autos'),
            ('home_lift', 'Home lift'),
            ('stairlift', 'Salva escaleras'),
            ('moving_walkway', 'Aceras móviles'),
            ('escalator', 'Escaleras eléctricas'),
            ('dumbwaiter', 'Montaplatos'),
            ('wheelchair_platform', 'Plataforma Vertical Silla de Ruedas'),
            ('car_platform_scissor', 'Plataforma para Autos Tijera'),
            ('car_platform_4post', 'Plataforma para Autos 4 postes'),
        ],
        string='Modelo del Elevador',
    )
    group_type = fields.Selection(
        [
            ('simplex', 'Simplex'),
            ('duplex', 'Duplex'),
            ('triplex', 'Triplex'),
            ('quadruplex', 'Cuadruplex'),
        ],
        string='Tipo de Grupo',
    )
    group_type_other = fields.Char(string='Otro tipo de Grupo')
    applied_standard = fields.Selection(
        [
            ('en81_2050', 'EN 81-20/50'),
            ('en81_1', 'EN 81-1'),
            ('en81_2', 'EN 81-2'),
            ('en81_70', 'EN 81-70 disabled person'),
            ('en81_72', 'EN 81-72 fire elevator'),
            ('en81_77', 'EN 81-77 sismic'),
            ('nom_53', 'Nom 53'),
            ('na', 'N/A'),
        ],
        string='Norma Aplicada',
    )
    installation = fields.Selection(YES_NO, string='Instalación')

    # ------------------------------------------------------------------
    # Especificaciones técnicas
    # ------------------------------------------------------------------
    speed = fields.Float(string='Velocidad (m/s)')
    traction_system = fields.Char(string='Sistema de Tracción')
    capacity = fields.Integer(string='Capacidad (Kg)')
    stops_count = fields.Integer(string='N° de paradas')
    supply_voltage = fields.Selection(
        [('110', '110'), ('220', '220'), ('380', '380'), ('440', '440')],
        string='Voltaje de alimentación (Volts)',
    )
    supply_type = fields.Selection(
        [
            ('single_phase', 'Monofásico'),
            ('two_phase', 'Bifásico'),
            ('three_phase', 'Trifásico'),
        ],
        string='Tipo de alimentación',
    )
    counterweight_governor = fields.Selection(
        YES_NO, string='Regulador de Velocidad en Contrapeso')
    control_type = fields.Selection(
        [
            ('type_02', 'Tipo 02'),
            ('type_02s', 'Tipo 02S'),
            ('smart', 'Inteligente'),
            ('alam_drive', 'Alam Drive'),
        ],
        string='Tipo de control',
    )

    # ------------------------------------------------------------------
    # Cubo y foso
    # ------------------------------------------------------------------
    shaft_width = fields.Integer(string='Ancho del Cubo (mm)')
    shaft_depth = fields.Integer(string='Profundidad del Cubo (mm)')
    pit_depth = fields.Integer(string='Foso (mm)')
    travel = fields.Integer(string='Recorrido (mm)')
    overhead = fields.Integer(string='Sobre paso (mm)')
    shaft_type = fields.Selection(
        [
            ('concrete', 'Concreto'),
            ('steel_structure', 'Estructura Metálica'),
            ('no_construction', 'Sin Construcción'),
            ('brick_concrete_beams', 'Ladrillo y Vigas de concreto'),
            ('mixed', 'Mixto'),
        ],
        string='Tipo de Cubo',
    )
    shaft_construction = fields.Selection(
        [('required', 'Requerido'), ('not_required', 'No requerido')],
        string='Construcción del Cubo',
    )

    # ------------------------------------------------------------------
    # Puertas y entradas
    # ------------------------------------------------------------------
    front_rear_floors = fields.Char(string='Pisos Frontal y Posterior')
    entrance_width = fields.Integer(string='Ancho de Entrada (mm)')
    entrance_height = fields.Integer(string='Alto de Entrada (mm)')
    cabin_door_finish = fields.Selection(
        [
            ('inox', 'Inox / Acero Inoxidable Mate 304'),
            ('mirror_st', 'Mirror St / Acero Inoxidable Espejo 304'),
            ('ral', 'Ral / Pintada Epóxica'),
            ('glass', 'Glass / Panorámica Vidrio'),
            ('decorative', 'Decorativa st. / Decorativa'),
            ('gold', 'Dorada'),
            ('no_doors', 'Sin puertas'),
        ],
        string='Acabado de Puerta de Cabina',
    )
    door_fire_resistance = fields.Selection(
        [
            ('none', 'No'),
            ('standard', 'Estandar'),
            ('e60', 'E60'),
            ('e120', 'E120'),
            ('e160', 'E160'),
        ],
        string='Resistencia de Puerta al Fuego',
    )

    # ------------------------------------------------------------------
    # Cabina y piso
    # ------------------------------------------------------------------
    cabin_type = fields.Char(string='Tipo de Cabina')
    floor_nomenclature = fields.Char(string='Nomenclatura de Piso')
    lop_type = fields.Selection(
        [('touch', 'Touch'), ('normal', 'Normal')],
        string='Modelo LOP',
    )
    handrail_type = fields.Selection(
        [('square', 'Cuadrado'), ('round', 'Redondo')],
        string='Tipo de Pasamanos',
    )
    lop_model = fields.Char(string='Modelo de LOP')
    floor_height = fields.Integer(string='Altura de Piso (mm)')
    floor_type = fields.Selection(
        [
            ('granite', 'Granito'),
            ('non_slip', 'Antiderrapante'),
            ('recess_6', 'Receso de 6 mm'),
            ('recess_25', 'Receso de 25 mm'),
        ],
        string='Tipo de Piso',
    )

    # ------------------------------------------------------------------
    # Documentos
    # ------------------------------------------------------------------
    zoho_url = fields.Char(string='URL Zoho')