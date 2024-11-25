import openmc 
import numpy as np
from argparse import ArgumentParser
import openmc.material 
import warnings
warnings.filterwarnings('ignore')


# Create the argument parser
ap = ArgumentParser(description="SFR Pincell Model Generator")
ap.add_argument('-n', dest='n_axial', type=int, default=100, help='Number of cells in the Z direction')
ap.add_argument('-e', '--shannon_entropy', action='store_true', help='Add Shannon entropy mesh')
ap.add_argument('--height', dest='height_of_the_core', type=float, default=30.0, help='Height of the reactor core')

# Parse the arguments
arguments = ap.parse_args()

arguments=ap.parse_args()

N=arguments.n_axial
height=arguments.height_of_the_core
shannon_entropy=arguments.shannon_entropy


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

outer_fuel_material= openmc.Material.mix_materials([u235, u238, pu238, pu239, pu240, pu241, pu242, am241, o16],[0.0018, 0.73, 0.0053, 0.0711, 0.0445, 0.0124, 0.0156, 0.0017, 0.1176],'wo')
cladding_material = openmc.Material.mix_materials([cu63,Al2O3], [0.997,0.003], 'wo')

materials=openmc.Materials([outer_fuel_material,sodium,helium,cladding_material])
materials.export_to_xml()


###############################################################################
# Define problem geometry

# Create cylindrical surfaces



# Create cylindrical surfacesfuel_or = openmc.ZCylinder(surface_id=1, r=0.943/2) 

fuel_or = openmc.ZCylinder(surface_id=1, r=0.943/2) 
clad_ir = openmc.ZCylinder(surface_id=2, r=0.973/2) 
clad_or = openmc.ZCylinder(surface_id=3, r=1.073/2) 



z_co_ordinates=np.linspace(-height/2,height/2,N+1)
z_plane=[]
for i in range (len(z_co_ordinates)):
    z_plane.append(openmc.ZPlane(z0=z_co_ordinates[i]))


#set BCs
z_plane[0].boundary_type='vacuum'
z_plane[-1].boundary_type='vacuum'
top=z_plane[-1]
bottom=z_plane[0]

outer_fuel_cells=[]
outer_gas_gap_cells=[]
outer_clad_cells=[]
outer_sodium_cells=[]

all_outer_cells=[]

outer_fuel_cells=[]
outer_gas_gap_cells=[]
outer_clad_cells=[]
outer_sodium_cells=[]

for i in range (N):
    
    layer=+z_plane[i]&-z_plane[i+1]
    
    outer_fuel_cells.append(openmc.Cell( fill=outer_fuel_material,region=layer & -fuel_or))
    outer_gas_gap_cells.append(openmc.Cell( fill=helium,region=layer & +fuel_or &-clad_ir))
    outer_clad_cells.append(openmc.Cell(fill=cladding_material,region= layer& +clad_ir &-clad_or))
    outer_sodium_cells.append(openmc.Cell(fill=sodium,region= +clad_or & layer))
    
    all_outer_cells.append(outer_fuel_cells[i])
    all_outer_cells.append(outer_gas_gap_cells[i])
    all_outer_cells.append(outer_clad_cells[i])
    all_outer_cells.append(outer_sodium_cells[i])
    
    
outer_u = openmc.Universe(cells=(all_outer_cells))

sodium_mod_cell = openmc.Cell(cell_id=6, fill=sodium)
sodium_mod_u = openmc.Universe(universe_id=3, cells=(sodium_mod_cell,))

# Define a lattice for outer assemblies
out_lat = openmc.HexLattice(lattice_id=1, name='outer assembly')
out_lat.center = (0., 0.)
out_lat.pitch = (21.08/17,)
out_lat.orientation = 'y'
out_lat.outer = sodium_mod_u

# Create rings of fuel universes that will fill the lattice
outone = [outer_u]*48
outtwo = [outer_u]*42
outthree = [outer_u]*36
outfour = [outer_u]*30
outfive = [outer_u]*24
outsix = [outer_u]*18
outseven = [outer_u]*12
outeight = [outer_u]*6
outnine = [outer_u]*1
out_lat.universes = [outone,outtwo,outthree,outfour,outfive,outsix,outseven,outeight,outnine]
print (out_lat)
# Create the prism that will contain the lattice
outer_surface = openmc.model.hexagonal_prism(edge_length=12.1705, orientation='y')

# Fill a cell with the lattice. This cell is filled with the lattice and contained within the prism.
main_out_assembly = openmc.Cell(cell_id=7, fill=out_lat, region=outer_surface & -top & +bottom)

# Fill a cell with a material that will surround the lattice
out_assembly  = openmc.Cell(cell_id=8, fill=sodium, region=~outer_surface & -top & +bottom)

# Create a universe that contains both 
main_out_u = openmc.Universe(universe_id=4, cells=[main_out_assembly, out_assembly])

# Create a geometry and export to XML
geometry = openmc.Geometry(main_out_u)
geometry.export_to_xml()

###############################################################################
# Define problem settings


# settings 
settings=openmc.Settings()
settings.batches=1000
settings.inactive=400
settings.particles=10000


if (shannon_entropy):
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

