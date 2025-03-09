import sys
sys.path.append("../..")

import openmc
import numpy as np
from argparse import ArgumentParser
import openmc.material
from materials import *
import common_input as geom

def make_hexagonal_ring_lists(number_of_ring: int, universe: openmc.Universe):
    ring_list = []
    for i in range(number_of_ring, 0, -1):
        if i == 1:
            ring = [universe]
        else:
            ring = [universe] * (i - 1) * 6
        ring_list.append(ring)
    return ring_list

def settings(shannon_entropy: bool, height: float):
    pitch = geom.pitch
    lower_left = (-pitch / 2, -pitch / 2, 0.0)
    upper_right = (pitch / 2, pitch / 2, height)
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

    settings.temperature = {
        "default": 280.0 + 273.15,
        "method": "interpolation",
        "range": (294.0, 3000.0),
        "tolerance": 1000.0,
    }
    settings.export_to_xml()

def main():
    ap = ArgumentParser(description="SFR Pincell Model Generator")
    ap.add_argument(
        "-n",
        dest="n_axial",
        type=int,
        default=1,
        help="Number of cells in the Z direction",
    )
    ap.add_argument(
        "-e",
        "--shannon_entropy",
        action="store_true",
        help="Add Shannon entropy mesh"
    )

    arguments = ap.parse_args()
    N = arguments.n_axial
    shannon_entropy = arguments.shannon_entropy
    height = geom.height

    outer_fuel_material = make_sfr_material(material_dict['outer_fuel'], percent_type='wo')
    cladding_material = make_sfr_material(material_dict['cladding'], percent_type='ao')
    sodium = make_sfr_material(material_dict['sodium'], percent_type='ao')
    helium = make_sfr_material(material_dict['helium'], percent_type='ao')
    materials = openmc.Materials(
        [outer_fuel_material, sodium, helium, cladding_material]
    )
    materials.export_to_xml()

    fuel_or = openmc.ZCylinder(r=geom.r_fuel)
    clad_ir = openmc.ZCylinder(r=geom.r_clad_inner)
    clad_or = openmc.ZCylinder(r=geom.r_clad_inner + geom.t_clad)

    top = openmc.ZPlane(z0=height / 2)
    bottom = openmc.ZPlane(z0=-height / 2)
    top.boundary_type = "vacuum"
    bottom.boundary_type = "vacuum"

    fuel_cell = openmc.Cell(
        region=-fuel_or & +bottom & -top,
        fill=outer_fuel_material
    )
    gas_gap_cell = openmc.Cell(
        region=+fuel_or & -clad_ir & +bottom & -top,
        fill=helium
    )
    clad_cell = openmc.Cell(
        region=+clad_ir & -clad_or & +bottom & -top,
        fill=cladding_material
    )
    sodium_cell = openmc.Cell(
        region=+clad_or & +bottom & -top,
        fill=sodium
    )

    inner_u = openmc.Universe(cells=[fuel_cell, gas_gap_cell, clad_cell, sodium_cell])

    sodium_mod_cell = openmc.Cell(fill=sodium)
    sodium_mod_u = openmc.Universe(cells=(sodium_mod_cell,))

    in_lat = openmc.HexLattice(name="inner assembly")
    in_lat.center = (0.0, 0.0)
    in_lat.pitch = (geom.lattice_pitch,)
    in_lat.orientation = "y"
    in_lat.outer = sodium_mod_u
    in_lat.universes = make_hexagonal_ring_lists(9, inner_u)

    axial_pitch = height / N
    lattice = openmc.RectLattice(name="3D lattice")
    lattice.lower_left = (-geom.pitch / 2, -geom.pitch / 2, -height / 2)
    lattice.pitch = (geom.pitch, geom.pitch, axial_pitch)
    lattice.universes = [[[inner_u] * N]]

    outer_in_surface = openmc.model.hexagonal_prism(
        edge_length= geom.edge_length, orientation="y"
    )
    main_in_assembly = openmc.Cell(
        fill=lattice, region=outer_in_surface & +bottom & -top
    )
    out_in_assembly = openmc.Cell(
        fill=sodium, region=~outer_in_surface & +bottom & -top
    )
    main_in_u = openmc.Universe(cells=[main_in_assembly, out_in_assembly])
    geometry = openmc.Geometry(main_in_u)
    geometry.export_to_xml()

    settings(shannon_entropy=False, height=height)

if __name__ == "__main__":
    main()