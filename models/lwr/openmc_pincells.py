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

import openmc
import numpy as np
import openmc_common as geom
from openmc_materials import MATERIALS as mats

#--------------------------------------------------------------------------------------------------------------------------#
# Geometry definitions.
## All of the pincells.
PINCELLS = {}

## The pincells - fuels first
### Common primitives for defining the different fuel regions.
fuel_pin_or = openmc.ZCylinder(r = geom.r_fuel)
fuel_gap_or = openmc.ZCylinder(r = geom.r_fuel + geom.t_f_c_gap)
fuel_zr_or = openmc.ZCylinder(r = geom.r_fuel + geom.t_f_c_gap + geom.t_zr_clad)
fuel_bb = openmc.model.RectangularPrism(width = geom.pitch, height = geom.pitch)

### Regions for the different components of the fuel pincells.
fuel_pin_region   = -fuel_pin_or
fuel_gap_region   = +fuel_pin_or & -fuel_gap_or
fuel_clad_region  = +fuel_gap_or & -fuel_zr_or
fuel_water_region = +fuel_zr_or & -fuel_bb

### Common cells used to define the different fuel pincells.
gap_cell = openmc.Cell(name = 'Pin Gap', region = fuel_gap_region)
zr_clad_cell = openmc.Cell(name = 'Pin Zr Clad', region = fuel_clad_region, fill = mats['ZR_C'])
h2o_bb_cell = openmc.Cell(name = 'Pin Water Bounding Box', region = fuel_water_region, fill = mats['H2O'])

### The entire 4.3% MOX pincell.
mox_4_3_fuel_cell = openmc.Cell(name = '4.3% MOX Fuel Pin', region = fuel_pin_region, fill = mats['MOX_43'])
PINCELLS['MOX43'] = openmc.Universe(cells=[mox_4_3_fuel_cell, gap_cell, zr_clad_cell, h2o_bb_cell])

### The entire 7.0% MOX pincell.
mox_7_0_fuel_cell = openmc.Cell(name = '7.0% MOX Fuel Pin', region = fuel_pin_region, fill = mats['MOX_70'])
PINCELLS['MOX70'] = openmc.Universe(cells=[mox_7_0_fuel_cell, gap_cell.clone(False, False), zr_clad_cell.clone(False, False), h2o_bb_cell.clone(False, False)])

### The entire 8.7% MOX pincell.
mox_8_7_fuel_cell = openmc.Cell(name = '8.7% MOX Fuel Pin', region = fuel_pin_region, fill = mats['MOX_87'])
PINCELLS['MOX87'] = openmc.Universe(cells=[mox_8_7_fuel_cell, gap_cell.clone(False, False), zr_clad_cell.clone(False, False), h2o_bb_cell.clone(False, False)])

### The entire UO2 pincell.
uo2_fuel_cell = openmc.Cell(name = 'UO2 Fuel Pin', region = fuel_pin_region, fill = mats['UO2'])
PINCELLS['UO2'] = openmc.Universe(cells=[uo2_fuel_cell, gap_cell.clone(False, False), zr_clad_cell.clone(False, False), h2o_bb_cell.clone(False, False)])

## Guide tube, control rod, and fission chamber next.
### Common primitives for defining both.
tube_fill_or = openmc.ZCylinder(r = geom.r_guide)
tube_clad_or = openmc.ZCylinder(r = geom.r_guide + geom.t_al_clad)

### Regions for the different components of the guide tube pincells.
guide_tube_fill_region = -tube_fill_or
guide_tube_clad_region = +tube_fill_or & -tube_clad_or
guide_tube_water_region = +tube_clad_or & -fuel_bb

### Common cells used to define the different guide tube pincells.
tube_clad_cell = openmc.Cell(name = 'Guide Tube Cladding', region = guide_tube_clad_region, fill = mats['AL_C'])
guide_tube_h2o_bb_cell = openmc.Cell(name = 'Guide Tube Water Bounding Box', region = guide_tube_water_region, fill = mats['H2O'])

### The guide tube.
tube_fill_cell = openmc.Cell(name = 'Guide Tube Water', region = guide_tube_fill_region, fill = mats['H2O'])
PINCELLS['GTB'] = openmc.Universe(cells=[tube_fill_cell, tube_clad_cell, guide_tube_h2o_bb_cell])

### The control rod.
rod_fill_cell = openmc.Cell(name = 'Control Rod Meat', region = guide_tube_fill_region, fill = mats['BC4'])
PINCELLS['ROD'] = openmc.Universe(cells=[rod_fill_cell, tube_clad_cell.clone(False, False), guide_tube_h2o_bb_cell.clone(False, False)])

### The fission chamber.
fission_chamber_cell = openmc.Cell(name = 'Fission Chamber', region = guide_tube_fill_region, fill = mats['FISS'])
PINCELLS['FIS'] = openmc.Universe(cells=[fission_chamber_cell, tube_clad_cell.clone(False, False), guide_tube_h2o_bb_cell.clone(False, False)])

### An empty water block.
water_cell = openmc.Cell(name = 'Moderator', region = -fuel_bb, fill = mats['H2O'])
PINCELLS['H2O'] = openmc.Universe(cells=[water_cell])
#--------------------------------------------------------------------------------------------------------------------------#
