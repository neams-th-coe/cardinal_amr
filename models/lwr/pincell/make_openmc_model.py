#********************************************************************/
#*                  SOFTWARE COPYRIGHT NOTIFICATION                 */
#*                             Cardinal                             */
#*                                                                  */
#*                  (c) 2021 UChicago Argonne, LLC                  */
#*                        ALL RIGHTS RESERVED                       */
#*                                                                  */
#*                 Prepared by UChicago Argonne, LLC                */
#*               Under Contract No. DE-AC02-06CH11357               */
#*                With the U. S. Department of Energy               */
#*                                                                  */
#*             Prepared by Battelle Energy Alliance, LLC            */
#*               Under Contract No. DE-AC07-05ID14517               */
#*                With the U. S. Department of Energy               */
#*                                                                  */
#*                 See LICENSE for full restrictions                */
#********************************************************************/

import openmc
import numpy as np
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('-n', dest='n_axial', type=int, default=40,
                help='Number of axial cell divisions')
ap.add_argument('-s', '--entropy', action='store_true',
                help='Whether to add a Shannon entropy mesh')
args = ap.parse_args()

N = args.n_axial # Number of axial cells to build in the solid to receive feedback
height = 192.78  # Total height of pincell

# Some geometric properties that can be modified to change the model.
## The radius of a fuel pin (same for all pin types).
r_fuel = 0.4095

## The thickness of the fuel-clad gap.
t_f_c_gap = 0.0085

## The thickness of the Zr fuel pin cladding.
t_zr_clad = 0.057

## The thickness of the axial reflector above the lattice.
reflector_t = 21.42

###############################################################################
# Create materials for the problem

## UO2 for the fuel.
uo2_comp = 1.0e24 * np.array([8.65e-4, 2.225e-2, 4.622e-2])
uo2_frac = uo2_comp / np.sum(uo2_comp)
uo2 = openmc.Material(name = 'UO2 Fuel', temperature = 293.15)
uo2.add_nuclide('U235', uo2_frac[0], percent_type = 'ao')
uo2.add_nuclide('U238', uo2_frac[1], percent_type = 'ao')
uo2.add_element('O', uo2_frac[2], percent_type = 'ao')
uo2.set_density('atom/cm3', np.sum(uo2_comp))

## Pure Zirconium for the cladding.
zr = openmc.Material(name = 'Zr Cladding', temperature = 293.15)
zr.add_element('Zr', 1.0, percent_type = 'ao')
zr.set_density('atom/cm3', 1.0e24 * 4.30e-2)

## Borated water.
h2o_comp = 1.0e24 * np.array([3.35e-2, 2.78e-5])
h2o_frac = h2o_comp / np.sum(h2o_comp)
h2o = openmc.Material(name = 'H2O Moderator', temperature = 293.15)
h2o.add_element('H', 2.0 * h2o_frac[0], percent_type = 'ao')
h2o.add_element('O', h2o_frac[0], percent_type = 'ao')
h2o.add_element('B', h2o_frac[1], percent_type = 'ao')
h2o.set_density('atom/cm3', np.sum(h2o_comp))
h2o.add_s_alpha_beta('c_H_in_H2O')

# Collect the materials together and export to XML
materials = openmc.Materials([uo2, zr, h2o])
materials.export_to_xml()

###############################################################################
# Define problem geometry

# Create cylindrical surfaces
fuel_or = openmc.ZCylinder(r = r_fuel, name = 'Fuel Outer Radius')
clad_ir = openmc.ZCylinder(r = r_fuel + t_f_c_gap, name = 'Clad Inner Radius')
clad_or = openmc.ZCylinder(r = r_fuel + t_f_c_gap + t_zr_clad, name = 'Clad Outer Radius')

# Create a region represented as the inside of a rectangular prism
pitch = 1.26
box = openmc.model.RectangularPrism(pitch, pitch, boundary_type='reflective')

# Create cells, mapping materials to regions - split up the axial height
planes = np.linspace(0.0, height, N + 1)
plane_surfaces = []
for i in range(N + 1):
  plane_surfaces.append(openmc.ZPlane(z0=planes[i]))

# set the boundary condition on the topmost and bottommost planes to vacuum
plane_surfaces[0].boundary_type = 'reflective'

fuel_cells = []
clad_cells = []
gap_cells = []
water_cells = []
all_cells = []
for i in range(N):
  layer = +plane_surfaces[i] & -plane_surfaces[i + 1]
  fuel_cells.append(openmc.Cell(fill=uo2, region=-fuel_or & layer, name='Fuel{:n}'.format(i)))
  gap_cells.append(openmc.Cell(fill=None, region=+fuel_or & -clad_ir & layer, name='Gap{:n}'.format(i)))
  clad_cells.append(openmc.Cell(fill=zr, region=+clad_ir & -clad_or & layer, name='Clad{:n}'.format(i)))
  water_cells.append(openmc.Cell(fill=h2o, region=+clad_or & layer & -box, name='Water{:n}'.format(i)))
  all_cells.append(fuel_cells[i])
  all_cells.append(gap_cells[i])
  all_cells.append(clad_cells[i])
  all_cells.append(water_cells[i])

# Add the top axial water reflector.
refl_top = openmc.ZPlane(z0 = height + reflector_t, boundary_type = 'vacuum')
all_cells.append(openmc.Cell(name='Axial Reflector Cell', fill = h2o, region=-box & -refl_top & +plane_surfaces[-1]))

# Create a geometry and export to XML
geometry = openmc.Geometry(all_cells)
geometry.export_to_xml()

###############################################################################
# Define problem settings

# Indicate how many particles to run
settings = openmc.Settings()
settings.batches = 1500
settings.inactive = 500
settings.particles = 20000

# Create an initial uniform spatial source distribution over fissionable zones
lower_left = (-pitch/2, -pitch/2, 0.0)
upper_right = (pitch/2, pitch/2, height)
uniform_dist = openmc.stats.Box(lower_left, upper_right)
settings.source = openmc.IndependentSource(space=uniform_dist)

if (args.entropy):
  entropy_mesh = openmc.RegularMesh()
  entropy_mesh.lower_left = lower_left
  entropy_mesh.upper_right = upper_right
  entropy_mesh.dimension = (10, 10, 20)
  settings.entropy_mesh = entropy_mesh

settings.temperature = {'default': 280.0 + 273.15,
                        'method': 'interpolation',
                        'range': (294.0, 3000.0),
                        'tolerance': 1000.0}

settings.export_to_xml()

# create some plots to look at the geometry for the sake of the tutorial
plot1          = openmc.Plot()
plot1.filename = 'plot1'
plot1.width    = (pitch, pitch)
plot1.basis    = 'xy'
plot1.origin   = (0.0, 0.0, height/2.0)
plot1.pixels   = (1000, 1000)
plot1.color_by = 'cell'

plot2          = openmc.Plot()
plot2.filename = 'plot2'
plot2.width    = (pitch, height)
plot2.basis    = 'xz'
plot2.origin   = (0.0, 0.0, height/2.0)
plot2.pixels   = (100, int(100 * (height/2.0/pitch)))
plot2.color_by = 'cell'

plots = openmc.Plots([plot1, plot2])
plots.export_to_xml()

