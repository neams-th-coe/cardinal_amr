import openmc
import numpy as np
from SFR.materials import make_sfr_material, material_dict
from SFR import common_input as geometric_params
from SFR.Pincell.make_openmc_model import get_pincell_universe, argument_parser, simulation_settings


def make_hexagonal_ring_lists(number_of_ring: int, universe: openmc.Universe):
    return [[universe] if i == 1 else [universe] * (i - 1) * 6 for i in range(number_of_ring, 0, -1)]


def generate_assembly_model(arguments):
    pincell_universe, materials = get_pincell_universe(arguments)

    top = openmc.ZPlane(z0=geometric_params.height, boundary_type="vacuum")
    bottom = openmc.ZPlane(z0=0, boundary_type="vacuum")
    sodium = make_sfr_material(material_dict['sodium'], percent_type='ao')
    materials.append(sodium)

    sodium_mod_cell = openmc.Cell(fill=sodium)
    sodium_mod_u = openmc.Universe(cells=(sodium_mod_cell,))
    lattice = openmc.HexLattice()
    lattice.center = (0.0, 0.0, 0.0)
    lattice.orientation = "y"
    lattice.outer = sodium_mod_u
    lattice.pitch = (geometric_params.lattice_pitch, geometric_params.height / geometric_params.AXIAL_DIVISIONS)
    lattice.universes = [make_hexagonal_ring_lists(9, pincell_universe)] * geometric_params.AXIAL_DIVISIONS

    outer_in_surface = openmc.model.HexagonalPrism(edge_length=geometric_params.edge_length, orientation="y")
    main_in_assembly = openmc.Cell(fill=lattice, region=-outer_in_surface & +bottom & -top)
    out_in_assembly = openmc.Cell(fill=sodium, region=+outer_in_surface & +bottom & -top)
    main_in_u = openmc.Universe(cells=[main_in_assembly, out_in_assembly])

    setting = simulation_settings()
    setting.source = openmc.IndependentSource(space=openmc.stats.CylindricalIndependent(r=openmc.stats.Uniform(a=0, b=geometric_params.edge_length), phi=openmc.stats.Uniform(a=0, b=np.pi * 2), z=openmc.stats.Uniform(a=0, b=geometric_params.height / 2)))

    return materials, main_in_u, setting


if __name__ == "__main__":
    args = argument_parser()
    materials, root_universe, settings = generate_assembly_model(args)
    openmc.model.Model(openmc.Geometry(root_universe), materials, settings).export_to_model_xml()
