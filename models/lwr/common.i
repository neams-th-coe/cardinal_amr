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

#--------------------------------------------------------------------------------------------------------------------------#
# Assembly geometrical information
#--------------------------------------------------------------------------------------------------------------------------#
# The pitch of a single lattice element.
pitch       = 1.26

# The height of the fuel assemblies from the axial midplane.
core_height = 192.78

# The thickness of the top reflector.
reflector_t = 21.42

# The radius of a fuel pin (same for all pin types).
r_fuel      = 0.4095

# The thickness of the fuel-clad gap.
t_f_c_gap   = 0.0085

# The thickness of the Zr fuel pin cladding.
t_zr_clad   = 0.057

# The radius of the control rod guide tubes and the fission chambers.
r_guide     = 0.3400

# The thickness of the guide tube / fission chamber Al cladding.
t_al_clad   = 0.2
#--------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------#
# Meshing parameters
#--------------------------------------------------------------------------------------------------------------------------#
NUM_SECTORS              = 2
FUEL_RADIAL_DIVISIONS    = 2
BACKGROUND_DIVISIONS     = 1
AXIAL_DIVISIONS          = 5
#--------------------------------------------------------------------------------------------------------------------------#
