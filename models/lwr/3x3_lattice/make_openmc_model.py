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
fuel_center = openmc.ZPlane(z0 = 0.0, boundary_type = 'reflective')
fuel_top = openmc.ZPlane(z0 = geom.core_height)
assembly_bb = openmc.model.RectangularPrism(width = pins_per_axis * geom.pitch, height = pins_per_axis * geom.pitch, origin = (0.0, 0.0), boundary_type = 'reflective')

core_assembly = openmc.RectLattice(name='Fuel Assembly')
core_assembly.pitch = (geom.pitch, geom.pitch, geom.core_height / args.n_axial)
core_assembly.lower_left = (-pins_per_axis * geom.pitch / 2.0, -pins_per_axis * geom.pitch / 2.0, 0.0)
core_assembly.universes = [ [
  [pins['UO2'], pins['UO2'], pins['UO2']],
  [pins['UO2'], pins['UO2'], pins['UO2']],
  [pins['UO2'], pins['UO2'], pins['UO2']]
] for i in range(args.n_axial) ]
core_assembly_cell = openmc.Cell(name = 'UO2 Pincell Lattice Cell', region = -assembly_bb & +fuel_center & -fuel_top, fill = core_assembly)

## Add the top axial water reflector.
refl_top = openmc.ZPlane(z0 = geom.core_height + geom.reflector_t, boundary_type = 'vacuum')
refl_cell = openmc.Cell(name='Axial Reflector Cell', fill = mats['H2O'], region=-assembly_bb & -refl_top & +fuel_top)
#--------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------#
# Setup the model.
mult_pincell_model = openmc.Model(geometry = openmc.Geometry(openmc.Universe(cells = [core_assembly_cell, refl_cell])), materials = openmc.Materials([mats['UO2'], mats['H2O'], mats['ZR_C']]))

## The simulation settings.
mult_pincell_model.settings.source = [openmc.IndependentSource(space = openmc.stats.Box(lower_left = (-pins_per_axis * geom.pitch / 2.0, -pins_per_axis * geom.pitch / 2.0, 0.0),
                                                                                        upper_right = (pins_per_axis * geom.pitch / 2.0,  pins_per_axis * geom.pitch / 2.0, geom.core_height)))]

mult_pincell_model.settings.batches = 100
mult_pincell_model.settings.generations_per_batch = 10
mult_pincell_model.settings.inactive = 10
mult_pincell_model.settings.particles = 1000

mult_pincell_model.settings.temperature = {'default': 293.15,
                                           'method': 'interpolation',
                                           'range': (294.0, 3000.0),
                                           'tolerance': 1000.0}

mult_pincell_model.export_to_model_xml()
#--------------------------------------------------------------------------------------------------------------------------#
