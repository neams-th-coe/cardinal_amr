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

import openmc
import openmc_common as geom
from openmc_pincells import PINCELLS as pins

#--------------------------------------------------------------------------------------------------------------------------#
# Geometry definitions.
## The assemblies.
pins_per_axis = 17.0
ASSEMBLIES = {}
ASSEMBLY_UNIVERSES = {}
assembly_bb = openmc.model.RectangularPrism(width = pins_per_axis * geom.pitch, height = pins_per_axis * geom.pitch)

### Different assembly maps.
ASSEMBLY_MAPS = {
  'UO2' : [
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 1
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 2
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 3
    ['UO2', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'UO2'], # 4
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 5
    ['UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2'], # 6
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 7
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 8
    ['UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'FIS', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2'], # 9
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 10
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 11
    ['UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2'], # 12
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 13
    ['UO2', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'UO2'], # 14
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'GTB', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 15
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2'], # 16
    ['UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2', 'UO2']  # 17
  ],# 1      2      3      4      5      6      7      8      9      10     11     12     13     14     15     16     17
  'MOX' : [
    ['MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43'], # 1
    ['MOX43', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX43'], # 2
    ['MOX43', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'GTB',   'MOX70', 'MOX70', 'GTB',   'MOX70', 'MOX70', 'GTB',   'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX43'], # 3
    ['MOX43', 'MOX70', 'MOX70', 'GTB',   'MOX70', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX70', 'GTB',   'MOX70', 'MOX70', 'MOX43'], # 4
    ['MOX43', 'MOX70', 'MOX70', 'MOX70', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX70', 'MOX70', 'MOX70', 'MOX43'], # 5
    ['MOX43', 'MOX70', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX70', 'MOX43'], # 6
    ['MOX43', 'MOX70', 'MOX70', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX70', 'MOX70', 'MOX43'], # 7
    ['MOX43', 'MOX70', 'MOX70', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX70', 'MOX70', 'MOX43'], # 8
    ['MOX43', 'MOX70', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX87', 'MOX87', 'FIS',   'MOX87', 'MOX87', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX70', 'MOX43'], # 9
    ['MOX43', 'MOX70', 'MOX70', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX70', 'MOX70', 'MOX43'], # 10
    ['MOX43', 'MOX70', 'MOX70', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX70', 'MOX70', 'MOX43'], # 11
    ['MOX43', 'MOX70', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX87', 'MOX87', 'GTB',   'MOX70', 'MOX43'], # 12
    ['MOX43', 'MOX70', 'MOX70', 'MOX70', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX70', 'MOX70', 'MOX70', 'MOX43'], # 13
    ['MOX43', 'MOX70', 'MOX70', 'GTB',   'MOX70', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX87', 'MOX70', 'GTB',   'MOX70', 'MOX70', 'MOX43'], # 14
    ['MOX43', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'GTB',   'MOX70', 'MOX70', 'GTB',   'MOX70', 'MOX70', 'GTB',   'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX43'], # 15
    ['MOX43', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX70', 'MOX43'], # 16
    ['MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43', 'MOX43']  # 17
  ],# 1        2        3        4        5        6        7        8        9        10       11       12       13       14       15       16       17
  'REF' : [
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 1
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 2
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 3
    ['H2O', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'H2O'], # 4
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 5
    ['H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O'], # 6
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 7
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 8
    ['H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O'], # 9
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 10
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 11
    ['H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O'], # 12
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 13
    ['H2O', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'H2O'], # 14
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'GTB', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 15
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O'], # 16
    ['H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O', 'H2O']  # 17
  ]#  1      2      3      4      5      6      7      8      9      10     11     12     13     14     15     16     17
}

#### Replace all guide tubes with control rods for the rodded assembly.
ASSEMBLY_MAPS['UO2_ROD'] = [ [ pin_type.replace('GTB', 'ROD') for pin_type in row ] for row in ASSEMBLY_MAPS['UO2'] ]

#### Replace all guide tubes with control rods for the rodded reflector, other than the central guide tube.
ASSEMBLY_MAPS['REF_ROD'] = [ [ pin_type.replace('GTB', 'ROD') for pin_type in row ] for row in ASSEMBLY_MAPS['REF'] ]
ASSEMBLY_MAPS['REF_ROD'][8][8] = 'GTB'

### The assembly cells.
for name, map in ASSEMBLY_MAPS.items():
  assembly = openmc.RectLattice(name = name)
  assembly.pitch = (geom.pitch, geom.pitch)
  assembly.lower_left = (-pins_per_axis * geom.pitch / 2.0, -pins_per_axis * geom.pitch / 2.0)
  assembly.universes = [ [ pins[pin_type] for pin_type in row] for row in map ]
  ASSEMBLIES[name] = openmc.Cell(name = name + ' Lattice Cell', region = -assembly_bb, fill = assembly)
  ASSEMBLY_UNIVERSES[name] = openmc.Universe(name = name + ' Lattice Universe', cells=[ASSEMBLIES[name]])
#--------------------------------------------------------------------------------------------------------------------------#
