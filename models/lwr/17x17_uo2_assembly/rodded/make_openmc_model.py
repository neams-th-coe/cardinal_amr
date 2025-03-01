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
sys.path.append("../../")

import numpy as np
from argparse import ArgumentParser

import openmc
import openmc_common as geom
from openmc_materials import MATERIALS as mats
from openmc_assemblies import ASSEMBLIES as asmb
from openmc_assemblies import assembly_bb, pins_per_axis

ap = ArgumentParser()
ap.add_argument('-n', dest='n_axial', type=int, default=1,
                help='Number of axial core divisions')
args = ap.parse_args()

#--------------------------------------------------------------------------------------------------------------------------#
# Geometry definitions.
assembly_bb.boundary_type = 'reflective'
fuel_center = openmc.ZPlane(z0 = 0.0, boundary_type = 'reflective')
fuel_top = openmc.ZPlane(z0 = geom.core_height)

asmb['UO2_ROD'].fill.pitch = (geom.pitch, geom.pitch, geom.core_height / args.n_axial)
asmb['UO2_ROD'].fill.lower_left = (-pins_per_axis * geom.pitch / 2.0, -pins_per_axis * geom.pitch / 2.0, 0.0)
asmb['UO2_ROD'].fill.universes = [ asmb['UO2_ROD'].fill.universes for i in range(args.n_axial) ]
asmb['UO2_ROD'].region = asmb['UO2_ROD'].region & +fuel_center & -fuel_top

refl_top = openmc.ZPlane(z0 = geom.core_height + geom.reflector_t, boundary_type = 'vacuum')
asmb['REF_ROD'].region = asmb['REF'].region & -refl_top & +fuel_top

#--------------------------------------------------------------------------------------------------------------------------#
# Setup the model.
c5g7_model = openmc.Model(geometry = openmc.Geometry(openmc.Universe(cells = [asmb['UO2_ROD'], asmb['REF_ROD']])), materials = openmc.Materials([mats['UO2'], mats['H2O'], mats['FISS'], mats['ZR_C'], mats['AL_C'], mats['BC4']]))

## The simulation settings.
c5g7_model.settings.source = [openmc.IndependentSource(space = openmc.stats.Box(lower_left = (-pins_per_axis * geom.pitch / 2.0, -pins_per_axis * geom.pitch / 2.0, 0.0),
                                                                                upper_right = (pins_per_axis * geom.pitch / 2.0,  pins_per_axis * geom.pitch / 2.0, geom.core_height)))]
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
