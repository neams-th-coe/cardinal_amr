#--------------------------------------------------------------------------------------------------------------------------#
# This is based on the C5G7 reactor physics benchmark problem extension case as described in:                              #
# "Benchmark on Deterministic Transport Calculations Without Spatial Homogenisation: MOX Fuel Assembly 3-D Extension Case" #
# [NEA/NSC/DOC(2005)16]                                                                                                    #
# https://www.oecd-nea.org/upload/docs/application/pdf/2019-12/nsc-doc2005-16.pdf                                          #
#                                                                                                                          #
# The original C5G7 benchmark is defined with multi-group cross sections. To account for                                   #
# continuous energy spectral effects, we chose to use the material properties provided in:                                 #
# "Proposal for a Second Stage of the Benchmark on Power Distributions Within Assemblies"                                  #
# [NEA/NSC/DOC(96)2]                                                                                                       #
# https://www.oecd-nea.org/upload/docs/application/pdf/2020-01/nsc-doc96-02-rev2.pdf                                       #
#--------------------------------------------------------------------------------------------------------------------------#

import sys
sys.path.append("../")

import numpy as np
from argparse import ArgumentParser

import openmc
import openmc_common as geom
from openmc_materials import MATERIALS as mats
from openmc_pincells import PINCELLS as pins

ap = ArgumentParser()
ap.add_argument('-n', dest='n_axial', type=int, default=1,
                help='Number of axial cell divisions')
args = ap.parse_args()

#--------------------------------------------------------------------------------------------------------------------------#
# Geometry definitions.
pins_per_axis = 3.0
core_z_planes = [ openmc.ZPlane(z0=z) for z in np.linspace(0.0, geom.core_height, args.n_axial + 1) ]
core_z_planes[0].boundary_type = 'reflective'

assembly = openmc.RectLattice(name='Fuel Assembly')
assembly.pitch = (geom.pitch, geom.pitch)
assembly.lower_left = (-pins_per_axis * geom.pitch / 2.0, -pins_per_axis * geom.pitch / 2.0)
assembly.universes = [
  [pins['UO2'], pins['UO2'], pins['UO2']],
  [pins['UO2'], pins['UO2'], pins['UO2']],
  [pins['UO2'], pins['UO2'], pins['UO2']]
]
assembly_bb = openmc.model.RectangularPrism(width = pins_per_axis * geom.pitch, height = pins_per_axis * geom.pitch, origin = (0.0, 0.0), boundary_type = 'reflective')

all_cells = []
for layer_idx, planes in enumerate(zip(core_z_planes[:-1], core_z_planes[1:])):
  all_cells.append(openmc.Cell(name = f'UO2 Assembly Cell {layer_idx}', region = -assembly_bb & +planes[0] & -planes[1], fill = assembly))

## Add the top axial water reflector.
refl_top = openmc.ZPlane(z0 = geom.core_height + geom.reflector_t, boundary_type = 'vacuum')
all_cells.append(openmc.Cell(name='Axial Reflector Cell', fill = mats['H2O'], region=-assembly_bb & -refl_top & +core_z_planes[-1]))
#--------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------#
# Setup the model.
mult_pincell_model = openmc.Model(geometry = openmc.Geometry(openmc.Universe(cells = all_cells)), materials = openmc.Materials([mats['UO2'], mats['H2O'], mats['ZR_C']]))

## The simulation settings.
mult_pincell_model.settings.source = [openmc.IndependentSource(space = openmc.stats.Box(lower_left = (-pins_per_axis * geom.pitch / 2.0, -pins_per_axis * geom.pitch / 2.0, 0.0),
                                                                                        upper_right = (pins_per_axis * geom.pitch / 2.0,  pins_per_axis * geom.pitch / 2.0, geom.core_height)))]

mult_pincell_model.settings.batches = 100
mult_pincell_model.settings.generations_per_batch = 10
mult_pincell_model.settings.inactive = 10
mult_pincell_model.settings.particles = 1000

mult_pincell_model.export_to_model_xml()
#--------------------------------------------------------------------------------------------------------------------------#
