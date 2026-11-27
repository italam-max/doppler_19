from . import models
from . import wizard
from .models.hr_employee import seed_contract_types, seed_psico_from_applicants


def post_init_hook(env):
    seed_psico_from_applicants(env)
    seed_contract_types(env)
