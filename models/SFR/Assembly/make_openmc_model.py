import openmc
import numpy as np
from argparse import ArgumentParser
from models.SFR import common_input as assembly_geometric_params
from models.SFR.pincell import *


def argument_parser():
    ap = ArgumentParser(description="SFR assembly Model Generator")
    ap.add_argument("-n", dest="n_axial", type=int, default=assembly_geometric_params.AXIAL_DIVISIONS,
                    help="Number of cells in the Z direction")
    ap.add_argument("-p", dest="pincell_type", type=str, choices=["inner", "outer"], default="inner",
                    help="Material composition of the assembly fuel material")

    return ap.parse_args()


def simulation_settings():
    setting = openmc.Settings()
    setting.source = openmc.IndependentSource(
        space=openmc.stats.CylindricalIndependent(r=openmc.stats.Uniform(a=0, b=assembly_geometric_params.edge_length),
                                                  phi=openmc.stats.Uniform(a=0, b=np.pi * 2),
                                                  z=openmc.stats.Uniform(a=0, b=assembly_geometric_params.height / 2)))
    setting.batches = 200
    setting.inactive = 40
    setting.particles = 2000
    setting.temperature = {"default": 553.15, "method": "interpolation", "range": (290.0, 3000.0)}
    return setting


def make_hexagonal_ring_lists(number_of_ring: int, universe: openmc.Universe):
    return [[universe] if i == 1 else [universe] * (i - 1) * 6 for i in range(number_of_ring, 0, -1)]


def generate_assembly_model(arguments):
    pincell_universe, material = PINCELLS[arguments.pincell_type]

    top = openmc.ZPlane(z0=assembly_geometric_params.height, boundary_type="vacuum")
    bottom = openmc.ZPlane(z0=0, boundary_type="vacuum")

    lattice = openmc.HexLattice()
    lattice.center = (0.0, 0.0, 0.0)
    lattice.orientation = "y"
    lattice.outer = openmc.Universe(cells=(openmc.Cell(fill=sodium),))
    lattice.pitch = (assembly_geometric_params.lattice_pitch, assembly_geometric_params.height / arguments.n_axial)
    lattice.universes = [make_hexagonal_ring_lists(9, pincell_universe)] * arguments.n_axial

    outer_in_surface = openmc.model.HexagonalPrism(edge_length=assembly_geometric_params.edge_length, orientation="y", boundary_type='vacuum')
    main_in_assembly = openmc.Cell(fill=lattice, region=-outer_in_surface & +bottom & -top)
    main_in_u = openmc.Universe(cells=[main_in_assembly])

    return main_in_u, material


if __name__ == "__main__":
    args = argument_parser()
    settings = simulation_settings()
    root_universe, materials = generate_assembly_model(args)
    openmc.model.Model(openmc.Geometry(root_universe), materials, settings).export_to_model_xml()
