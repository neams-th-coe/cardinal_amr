#--------------------------------------------------------------------------------------------------------------------------#
# This is a modified version of the C5G7 reactor physics benchmark problem as described in:                                #
# "Benchmark on Deterministic Transport Calculations Without Spatial Homogenisation: A 2-D/3-D MOX Fuel Assembly Benchmark"#
# [NEA/NSC/DOC(2003)16]                                                                                                    #
# https://www.oecd-nea.org/upload/docs/application/pdf/2019-12/nsc-doc2003-16.pdf                                          #                                                                                                                          #
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
from openmc_assemblies import ASSEMBLIES as asmb
from openmc_assemblies import pins_per_axis

ap = ArgumentParser()
ap.add_argument('-n', dest='n_axial', type=int, default=1,
                help='Number of axial core divisions')
args = ap.parse_args()

#--------------------------------------------------------------------------------------------------------------------------#
# Geometry definitions.
## The core region.
core_front = openmc.YPlane(y0 = pins_per_axis * geom.pitch, boundary_type = 'reflective')
core_left = openmc.XPlane(x0 = -pins_per_axis * geom.pitch, boundary_type = 'reflective')
core_right = openmc.XPlane(x0 = pins_per_axis * geom.pitch)
core_back = openmc.YPlane(y0 = -pins_per_axis * geom.pitch)
core_bb_xy = -core_front & +core_back & +core_left & -core_right

core_assembly = openmc.RectLattice(name = 'Core Assembly')
core_assembly.pitch = (pins_per_axis * geom.pitch, pins_per_axis * geom.pitch)
core_assembly.lower_left = (-pins_per_axis * geom.pitch, -pins_per_axis * geom.pitch)
core_assembly.universes = [
  [asmb['UO2'], asmb['MOX']],
  [asmb['MOX'],     asmb['UO2']]
]

core_z_planes = [ openmc.ZPlane(z0=z) for z in np.linspace(0.0, geom.core_height, args.n_axial + 1) ]
core_z_planes[0].boundary_type = 'reflective'

all_cells = []
for layer_idx, planes in enumerate(zip(core_z_planes[:-1], core_z_planes[1:])):
  all_cells.append(openmc.Cell(name = f'Core Assembly Cell {layer_idx}', region = core_bb_xy & +planes[0] & -planes[1], fill = core_assembly))

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
all_cells.append(openmc.Cell(name = 'Upper Reflector Cell', region = +core_z_planes[-1] & -refl_top & core_bb_xy, fill = upper_refl_assembly))

### The remainder of the reflector.
refl_region = -core_front & +refl_back & +core_left & -refl_right & -refl_top & +core_z_planes[0] & ~(core_bb_xy & +core_z_planes[0] & -refl_top)
refl_cell = openmc.Cell(name = 'Water Reflector')
refl_cell.region = refl_region
refl_cell.fill = mats['H2O']
all_cells.append(refl_cell)

## The entire geometry.
model_uni = openmc.Universe(cells = all_cells)
#--------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------#
# Setup the model.
c5g7_model = openmc.Model(geometry = openmc.Geometry(model_uni), materials = openmc.Materials([mats['MOX_43'], mats['MOX_70'], mats['MOX_87'], mats['UO2'], mats['H2O'], mats['FISS'], mats['ZR_C'], mats['AL_C']]))

## The simulation settings.
c5g7_model.settings.source = [openmc.IndependentSource(space = openmc.stats.Box(lower_left = (-pins_per_axis * geom.pitch, -pins_per_axis * geom.pitch, 0.0),
                                                                                upper_right = (pins_per_axis * geom.pitch, pins_per_axis * geom.pitch, geom.core_height)))]
c5g7_model.settings.batches = 100
c5g7_model.settings.generations_per_batch = 10
c5g7_model.settings.inactive = 10
c5g7_model.settings.particles = 1000

c5g7_model.export_to_model_xml()
#--------------------------------------------------------------------------------------------------------------------------#
