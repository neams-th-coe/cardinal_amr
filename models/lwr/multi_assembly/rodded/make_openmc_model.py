#--------------------------------------------------------------------------------------------------------------------------#
# This is a modified version of the C5G7 reactor physics benchmark problem extension case as described in:                 #
# "Benchmark on Deterministic Transport Calculations Without Spatial Homogenisation: MOX Fuel Assembly 3-D Extension Case" #
# [NEA/NSC/DOC(2005)16]                                                                                                    #
# https://www.oecd-nea.org/upload/docs/application/pdf/2019-12/nsc-doc2005-16.pdf                                          #                                                                                                                     #
#                                                                                                                          #
# The original C5G7 benchmark is defined with multi-group cross sections. To account for                                   #
# continuous energy spectral effects, we chose to use the material properties provided in:                                 #
# "Proposal for a Second Stage of the Benchmark on Power Distributions Within Assemblies"                                  #
# [NEA/NSC/DOC(96)2]                                                                                                       #
# https://www.oecd-nea.org/upload/docs/application/pdf/2020-01/nsc-doc96-02-rev2.pdf                                       #
#--------------------------------------------------------------------------------------------------------------------------#

import sys
sys.path.append("../../")

import numpy as np
from argparse import ArgumentParser

import openmc
import openmc_common as geom
from openmc_materials import MATERIALS as mats
from openmc_assemblies import ASSEMBLY_UNIVERSES as asmb
from openmc_assemblies import pins_per_axis

ap = ArgumentParser()
ap.add_argument('-n', dest='n_axial', type=int, default=1,
                help='Number of axial core divisions')
args = ap.parse_args()

#--------------------------------------------------------------------------------------------------------------------------#
# Geometry definitions.
all_cells = []
## The core region.
core_center = openmc.ZPlane(z0 = 0.0, boundary_type = 'reflective')
core_top = openmc.ZPlane(z0 = geom.core_height)
core_front = openmc.YPlane(y0 = pins_per_axis * geom.pitch, boundary_type = 'reflective')
core_left = openmc.XPlane(x0 = -pins_per_axis * geom.pitch, boundary_type = 'reflective')
core_right = openmc.XPlane(x0 = pins_per_axis * geom.pitch)
core_back = openmc.YPlane(y0 = -pins_per_axis * geom.pitch)
core_bb_xy = -core_front & +core_back & +core_left & -core_right

core_cells = [
  [asmb['UO2_ROD'], asmb['MOX']],
  [asmb['MOX'],     asmb['UO2']]
]
core_assembly = openmc.RectLattice(name = 'Core Assembly')
core_assembly.pitch = (pins_per_axis * geom.pitch, pins_per_axis * geom.pitch, geom.core_height / args.n_axial)
core_assembly.lower_left = (-pins_per_axis * geom.pitch, -pins_per_axis * geom.pitch, 0.0)
core_assembly.universes = [ core_cells for i in range(args.n_axial)]
all_cells.append(openmc.Cell(name = 'Core Assembly Cell', fill = core_assembly, region = core_bb_xy & +core_center & -core_top))

## The reflector region.
refl_right = openmc.XPlane(x0 = pins_per_axis * geom.pitch + geom.reflector_t, boundary_type = 'vacuum')
refl_back = openmc.YPlane(y0 = -pins_per_axis * geom.pitch - geom.reflector_t, boundary_type = 'vacuum')
refl_top = openmc.ZPlane(z0 = geom.core_height + geom.reflector_t, boundary_type = 'vacuum')

### The portion of the reflector above the core (penetrated by control rods and guide tubes).
upper_refl_assembly = openmc.RectLattice(name = 'Upper Reflector Assembly')
upper_refl_assembly.pitch = (pins_per_axis * geom.pitch, pins_per_axis * geom.pitch)
upper_refl_assembly.lower_left = (-pins_per_axis * geom.pitch, -pins_per_axis * geom.pitch)
upper_refl_assembly.universes = [
  [asmb['REF'], asmb['REF']],
  [asmb['REF'], asmb['REF']]
]
all_cells.append(openmc.Cell(name = 'Upper Reflector Cell', region = +core_top & -refl_top & core_bb_xy, fill = upper_refl_assembly))

### The remainder of the reflector.
refl_region = -core_front & +refl_back & +core_left & -refl_right & -refl_top & +core_center & ~(core_bb_xy & +core_center & -refl_top)
all_cells.append(openmc.Cell(name = 'Water Reflector', fill = mats['H2O'], region = refl_region))
#--------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------#
# Setup the model.
c5g7_model = openmc.Model(geometry = openmc.Geometry(openmc.Universe(cells = all_cells)), materials = openmc.Materials([mats['MOX_43'], mats['MOX_70'], mats['MOX_87'], mats['UO2'], mats['H2O'], mats['FISS'], mats['ZR_C'], mats['AL_C'], mats['BC4']]))

## The simulation settings.
c5g7_model.settings.source = [openmc.IndependentSource(space = openmc.stats.Box(lower_left = (-pins_per_axis * geom.pitch, -pins_per_axis * geom.pitch, 0.0),
                                                                                upper_right = (pins_per_axis * geom.pitch, pins_per_axis * geom.pitch, geom.core_height)))]
c5g7_model.settings.batches = 100
c5g7_model.settings.generations_per_batch = 10
c5g7_model.settings.inactive = 10
c5g7_model.settings.particles = 1000

c5g7_model.settings.temperature = {'default': 293.15,
                                   'method': 'interpolation',
                                   'range': (294.0, 3000.0),
                                   'tolerance': 1000.0}

c5g7_model.export_to_model_xml()
#--------------------------------------------------------------------------------------------------------------------------#
