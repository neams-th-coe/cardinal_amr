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
import openmc_pincells as pins
from openmc_settings import COMMON_SETTINGS as settings

ap = ArgumentParser()
ap.add_argument('-n', dest='n_axial', type=int, default=1,
                help='Number of axial cell divisions')
args = ap.parse_args()

#--------------------------------------------------------------------------------------------------------------------------#
# Geometry definitions.
pins.fuel_bb.boundary_type = 'reflective'
fuel_center = openmc.ZPlane(z0 = 0.0, boundary_type = 'reflective')
fuel_top = openmc.ZPlane(z0 = geom.core_height)

core_assembly = openmc.RectLattice(name = 'UO2 Pincell Lattice')
core_assembly.pitch = (geom.pitch, geom.pitch, geom.core_height / args.n_axial)
core_assembly.lower_left = (-geom.pitch / 2.0, -geom.pitch / 2.0, 0.0)
core_assembly.universes = [ [ [pins.PINCELLS['UO2'] ] ] for i in range(args.n_axial) ]
core_assembly_cell = openmc.Cell(name = 'UO2 Pincell Lattice Cell', region = -pins.fuel_bb & +fuel_center & -fuel_top, fill = core_assembly)

## Add the top axial water reflector.
## Set the boundary condition on the topmost plane to vacuum.
refl_top = openmc.ZPlane(z0 = geom.core_height + geom.reflector_t, boundary_type = 'vacuum')
refl_cell = openmc.Cell(name='Axial Reflector Cell', fill = mats['H2O'], region=-pins.fuel_bb & -refl_top & +fuel_top)
#--------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------#
# Setup the model.
pincell_model = openmc.Model(geometry = openmc.Geometry(openmc.Universe(cells = [core_assembly_cell, refl_cell])))

## The simulation settings.
pincell_model.settings = settings
pincell_model.settings.source = [openmc.IndependentSource(space = openmc.stats.Box(lower_left = (-geom.pitch / 2.0, -geom.pitch / 2.0, 0.0),
                                                                                   upper_right = (geom.pitch / 2.0, geom.pitch / 2.0, geom.core_height)))]

pincell_model.export_to_model_xml()
#--------------------------------------------------------------------------------------------------------------------------#
