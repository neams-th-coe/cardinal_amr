import openmc
from models.sfr import common_input as pincell_params
from models.sfr.openmc_materials import make_sfr_material, material_dict

PINCELLS = {}

inner_fuel_material = make_sfr_material(material_dict['inner_fuel'], percent_type='wo')
outer_fuel_material = make_sfr_material(material_dict['outer_fuel'], percent_type='wo')
cladding_material = make_sfr_material(material_dict['cladding'], percent_type='ao')
helium = make_sfr_material(material_dict['helium'], percent_type='ao')
sodium = make_sfr_material(material_dict['sodium'], percent_type='ao')

fuel_or = openmc.ZCylinder(r=pincell_params.r_fuel)
clad_ir = openmc.ZCylinder(r=pincell_params.r_clad_inner)
clad_or = openmc.ZCylinder(r=(pincell_params.r_clad_inner + pincell_params.t_clad))

cladding_cell = openmc.Cell(fill=cladding_material, region=+clad_ir & -clad_or)
gas_gap_cell = openmc.Cell(fill=helium, region=+fuel_or & -clad_ir)
fuel_cell_outer = openmc.Cell(fill=inner_fuel_material, region=-fuel_or)
fuel_cell_inner = openmc.Cell(fill=inner_fuel_material, region=-fuel_or)
sodium_cell = openmc.Cell(fill=sodium, region=+clad_or)

PINCELLS["inner"] = [openmc.Universe(cells=[fuel_cell_inner, gas_gap_cell, cladding_cell, sodium_cell]), openmc.Materials([inner_fuel_material, helium, cladding_material, sodium])]
PINCELLS["outer"] = [openmc.Universe(cells=[fuel_cell_inner, gas_gap_cell, cladding_cell, sodium_cell]), openmc.Materials([outer_fuel_material, helium, cladding_material, sodium])]
