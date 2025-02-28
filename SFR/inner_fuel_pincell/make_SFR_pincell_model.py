import openmc
import numpy as np
from argparse import ArgumentParser
import openmc.material
import warnings
from materials import *
warnings.filterwarnings("ignore")

def make_sfr_material(material_dict, density: float, percent_type: str):
  material = openmc.Material()
  for nuclide, material_info in material_dict.items():
    material.add_nuclide(nuclide, percent=material_info["percent"], percent_type=percent_type)

  return material

def settings(shannon_entropy:bool,height:float):
  pitch = 1.25984
  lower_left = (-pitch/2, -pitch/2, 0.0)
  upper_right = (pitch/2, pitch/2, height)
  uniform_dist = openmc.stats.Box(lower_left, upper_right)
  settings = openmc.Settings()
  settings.source = openmc.IndependentSource(space=uniform_dist)
  settings.batches = 200
  settings.inactive = 40
  settings.particles = 20000

  if shannon_entropy:
    entropy_mesh = openmc.RegularMesh()
    entropy_mesh.lower_left = lower_left
    entropy_mesh.upper_right = upper_right
    entropy_mesh.dimension = (10, 10, 20)
    settings.entropy_mesh = entropy_mesh

  settings.temperature = { "default": 280.0 + 273.15,"method": "interpolation","range": (294.0, 3000.0),"tolerance": 1000.0}
  settings.export_to_xml()

def main():
  ap = ArgumentParser(description="SFR Pincell Model Generator")
  ap.add_argument("-n",dest="n_axial",type=int,default=1,help="Number of cells in the Z direction",)
  ap.add_argument( "-e", "--shannon_entropy", action="store_true", help="Add Shannon entropy mesh")
  ap.add_argument("--height",dest="height_of_the_core", type=float,default=30.0,help="Height of the reactor core")

  arguments = ap.parse_args()
  arguments = ap.parse_args()

  N = arguments.n_axial
  height = arguments.height_of_the_core
  shannon_entropy = arguments.shannon_entropy

  inner_fuel_material = make_sfr_material(material_dict=inner_fuel_material_dict, density=10.0, percent_type="wo")
  cladding_material = make_sfr_material(material_dict=cladding_material_dict, density=10, percent_type="ao")
  helium =make_sfr_material(material_dict =heilum_material_dict, density =0.001598 ,percent_type ='ao')
  sodium  =make_sfr_material(material_dict =sodium_material_dict, density =0.96 ,percent_type ='ao')
  materials = openmc.Materials([inner_fuel_material, sodium, helium, cladding_material])
  materials.export_to_xml()

  fuel_or = openmc.ZCylinder(r=0.943/2)
  clad_ir = openmc.ZCylinder(r=0.973/2)
  clad_or = openmc.ZCylinder(r=1.073/2)

  z_plane=[openmc.ZPlane(z0=i) for i in np.linspace(-height/2,height/2,N+1)]


  top=z_plane[-1]
  bottom=z_plane[0]
  top.boundary_type='vacuum'
  bottom.boundary_type='vacuum'

  inner_cells = {'fuel': [],'gas_gap': [],'clad': [],'sodium': []}
  all_inner_cells = []

  for i in range(N):

    layer = +z_plane[i] & -z_plane[i+1]
    inner_cells['fuel'].append(openmc.Cell(fill=inner_fuel_material, region=layer & -fuel_or))
    inner_cells['gas_gap'].append(openmc.Cell(fill=helium, region=layer & +fuel_or & -clad_ir))
    inner_cells['clad'].append(openmc.Cell(fill=cladding_material, region=layer & +clad_ir & -clad_or))
    inner_cells['sodium'].append(openmc.Cell(fill=sodium, region=+clad_or & layer))

    all_inner_cells.extend([inner_cells['fuel'][i], inner_cells['gas_gap'][i], inner_cells['clad'][i], inner_cells['sodium'][i]])


  geometry = openmc.Geometry(all_cells)
  geometry.export_to_xml()

  settings(shannon_entropy = False,height= height)

if __name__ == "__main__":
  main()