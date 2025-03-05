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

#--------------------------------------------------------------------------------------------------------------------------#
# Material definitions.
INITIAL_TEMP = 293.15

MATERIAL_COMP = {
  'MOX_43' : {
    'U235' : 5.00e-5,
    'U238' : 2.21e-2,
    'Pu238' : 1.50e-5,
    'Pu239' : 5.80e-4,
    'Pu240' : 2.40e-4,
    'Pu241' : 9.80e-5,
    'Pu242' : 5.40e-5,
    'Am241' : 1.30e-5,
    'O'     : 4.63e-2
  },
  'MOX_70' : {
    'U235' : 5.00e-5,
    'U238' : 2.21e-2,
    'Pu238' : 2.40e-5,
    'Pu239' : 9.30e-4,
    'Pu240' : 3.90e-4,
    'Pu241' : 1.52e-4,
    'Pu242' : 8.40e-5,
    'Am241' : 2.00e-5,
    'O' : 4.63e-2
  },
  'MOX_87' : {
    'U235' : 5.00e-5,
    'U238' : 2.21e-2,
    'Pu238' : 3.00e-5,
    'Pu239' : 1.16e-3,
    'Pu240' : 4.90e-4,
    'Pu241' : 1.90e-4,
    'Pu242' : 1.05e-4,
    'Am241' : 2.50e-5,
    'O' : 4.63e-2
  },
  'UO2' : {
    'U235' : 8.65e-4,
    'U238' : 2.225e-2,
    'O' : 4.622e-2
  },
  'BC4' : {
    'B' : 0.22,
    'C' : 0.055
  },
  'H2O' : {
    'H' : 2.0 * 3.35e-2,
    'O' : 3.35e-2,
    'B' : 2.78e-5
  },
  'FISS' : {
    'H' : 2.0 * 3.35e-2,
    'O' : 3.35e-2,
    'B' : 2.78e-5,
    'U235' : 1.0e-8
  },
  'ZR_C' : {
    'Zr' : 4.30e-2
  },
  'AL_C' : {
    'Al' : 6.0e-2
  }
}

MATERIALS = {}
for mat_name, mat_comp in MATERIAL_COMP.items():
  MATERIALS[mat_name] = openmc.Material(name = mat_name, temperature = INITIAL_TEMP)
  density = np.sum(np.array(list(mat_comp.values())))
  for nuclide, comp in mat_comp.items():
    if nuclide[-1].isdigit():
      MATERIALS[mat_name].add_nuclide(nuclide, comp / density, percent_type = 'ao')
    else:
      MATERIALS[mat_name].add_element(nuclide, comp / density, percent_type = 'ao')
  MATERIALS[mat_name].set_density('atom/cm3', 1.0e24 * density)
#--------------------------------------------------------------------------------------------------------------------------#
