from . import models
from .models.hr_employee import seed_psico_from_applicants


def post_init_hook(env):
    seed_psico_from_applicants(env)
