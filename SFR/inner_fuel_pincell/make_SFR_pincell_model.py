import openmc 
import numpy as np
from argparse import ArgumentParser
import openmc.material 


# Create the argument parser
ap = ArgumentParser(description="SFR Pincell Model Generator")
ap.add_argument('-n', dest='n_axial', type=int, default=100, help='Number of cells in the Z direction')
ap.add_argument('-e', '--shanon_entropy', action='store_true', help='Add Shannon entropy mesh')
ap.add_argument('--height', dest='height_of_the_core', type=float, default=30.0, help='Height of the reactor core')

# Parse the arguments
arguments = ap.parse_args()

arguments=ap.parse_args()

N=arguments.n_axial
height=arguments.height_of_the_core


###################################################################
##########################   Materials     ########################
###################################################################

u235 = openmc.Material(name='U235')
u235.add_nuclide('U235', 1.0)
u235.set_density('g/cm3', 10.0)

u238 = openmc.Material(name='U238')
u238.add_nuclide('U238', 1.0)
u238.set_density('g/cm3', 10.0)

pu238 = openmc.Material(name='Pu238')
pu238.add_nuclide('Pu238', 1.0)
pu238.set_density('g/cm3', 10.0)

pu239 = openmc.Material(name='U235')
pu239.add_nuclide('Pu239', 1.0)
pu239.set_density('g/cm3', 10.0)

pu240 = openmc.Material(name='Pu240')
pu240.add_nuclide('Pu240', 1.0)
pu240.set_density('g/cm3', 10.0)

pu241 = openmc.Material(name='Pu241')
pu241.add_nuclide('Pu241', 1.0)
pu241.set_density('g/cm3', 10.0)

pu242 = openmc.Material(name='Pu242')
pu242.add_nuclide('Pu242', 1.0)
pu242.set_density('g/cm3', 10.0)

am241 = openmc.Material(name='Am241')
am241.add_nuclide('Am241', 1.0)
am241.set_density('g/cm3', 10.0)

o16 = openmc.Material(name='O16')
o16.add_nuclide('O16', 1.0)
o16.set_density('g/cm3', 10.0)

sodium = openmc.Material(name='Na')
sodium.add_nuclide('Na23', 1.0)
sodium.set_density('g/cm3', 0.96)

cu63 = openmc.Material(name='Cu63')
cu63.set_density('g/cm3', 10.0)
cu63.add_nuclide('Cu63', 1.0)

Al2O3 = openmc.Material(name='Al2O3')
Al2O3.set_density('g/cm3', 10.0)
Al2O3.add_element('O', 3.0)
Al2O3.add_element('Al', 2.0)

helium = openmc.Material(name='Helium for gap')
helium.set_density('g/cm3', 0.001598)
helium.add_element('He', 2.4044e-4)

#Material mixtures

inner_fuel_material= openmc.Material.mix_materials([u235, u238, pu238, pu239, pu240, pu241, pu242, am241, o16],[0.0019, 0.7509, 0.0046, 0.0612, 0.0383, 0.0106, 0.0134, 0.001, 0.1181],'wo')
cladding_material = openmc.Material.mix_materials([cu63,Al2O3], [0.997,0.003], 'wo')

materials=openmc.Materials([inner_fuel_material,sodium,helium,cladding_material])
materials.export_to_xml()


###############################################################################
# Define problem geometry

# Create cylindrical surfaces

fuel_or = openmc.ZCylinder(surface_id=1, r=0.943/2) 
clad_ir = openmc.ZCylinder(surface_id=2, r=0.973/2) 
clad_or = openmc.ZCylinder(surface_id=3, r=1.073/2) 

# Create a region represented as the inside of a rectangular prism
pitch = 1.25984
box = openmc.model.RectangularPrism(pitch, pitch, boundary_type='reflective')

# Create cells, mapping materials to regions - split up the axial height
planes = np.linspace(0.0, height, N + 1)
plane_surfaces = []
for i in range(N + 1):
  plane_surfaces.append(openmc.ZPlane(z0=planes[i]))

# set the boundary condition on the topmost and bottommost planes to vacuum
plane_surfaces[0].boundary_type = 'reflective'
plane_surfaces[-1].boundary_type = 'vacuum'

fuel_cells = []
clad_cells = []
gap_cells = []
sodium_cells = []
all_cells = []

for i in range(N):
  layer = +plane_surfaces[i] & -plane_surfaces[i + 1]
  fuel_cells.append(openmc.Cell(fill=inner_fuel_material, region=-fuel_or & layer, name='Fuel{:n}'.format(i)))
  gap_cells.append(openmc.Cell(fill=helium, region=+fuel_or & -clad_ir & layer, name='Gap{:n}'.format(i)))
  clad_cells.append(openmc.Cell(fill=cladding_material, region=+clad_ir & -clad_or & layer, name='Clad{:n}'.format(i)))
  sodium_cells.append(openmc.Cell(fill=sodium, region=+clad_or & layer & -box, name='Sodium{:n}'.format(i)))
  all_cells.append(fuel_cells[i])
  all_cells.append(gap_cells[i])
  all_cells.append(clad_cells[i])
  all_cells.append(sodium_cells[i])

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

if (arguments.shanon_entropy):
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

