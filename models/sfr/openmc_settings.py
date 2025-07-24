import openmc

INITIAL_TEMP = 293.15
COMMON_SETTINGS = openmc.Settings()

COMMON_SETTINGS.batches = 100
COMMON_SETTINGS.generations_per_batch = 10
COMMON_SETTINGS.inactive = 10
COMMON_SETTINGS.particles = 1000

COMMON_SETTINGS.temperature = {'default': INITIAL_TEMP,
                               'method': 'interpolation',
                               'range': (INITIAL_TEMP, 3000.0),
                               'tolerance': 1000.0}
