import openmc
import numpy as np
import common_input as pincell_params
from openmc_materials import MATERIALS as sfr_mats

PINCELLS = {}

sodium = sfr_mats['sodium']

fuel_or = openmc.ZCylinder(r=pincell_params.r_fuel)
clad_ir = openmc.ZCylinder(r=pincell_params.r_clad_inner)
clad_or = openmc.ZCylinder(r=(pincell_params.r_clad_inner + pincell_params.t_clad))

cladding_cell = openmc.Cell(fill=sfr_mats['cladding'], region=+clad_ir & -clad_or)
gas_gap_cell = openmc.Cell(fill=sfr_mats['helium'], region=+fuel_or & -clad_ir)
sodium_cell = openmc.Cell(fill=sodium, region=+clad_or)

# Concentric, equal-area radial subdivision of the fuel meat, matching the MOOSE mesh's
# FUEL_RADIAL_DIVISIONS so that the radial power/temperature profile can be resolved.
fuel_ring_ors = [openmc.ZCylinder(r=pincell_params.r_fuel * np.sqrt(i / pincell_params.FUEL_RADIAL_DIVISIONS))
                 for i in range(1, pincell_params.FUEL_RADIAL_DIVISIONS)] + [fuel_or]

def fuel_ring_cells(material):
  cells = []
  inner_or = None
  for i, outer_or in enumerate(fuel_ring_ors):
    region = -outer_or if inner_or is None else (+inner_or & -outer_or)
    cells.append(openmc.Cell(name=f'Fuel Ring {i + 1}', fill=material, region=region))
    inner_or = outer_or
  return cells

PINCELLS["inner"] = [
  openmc.Universe(cells=fuel_ring_cells(sfr_mats['inner_fuel']) + [gas_gap_cell, cladding_cell, sodium_cell]),
  openmc.Materials([sfr_mats['inner_fuel'], sfr_mats['helium'], sfr_mats['cladding'], sodium])
]
PINCELLS["outer"] = [
  openmc.Universe(cells=fuel_ring_cells(sfr_mats['outer_fuel']) + [gas_gap_cell.clone(False, False), cladding_cell.clone(False, False), sodium_cell.clone(False, False)]),
  openmc.Materials([sfr_mats['outer_fuel'], sfr_mats['helium'], sfr_mats['cladding'], sodium])
]
