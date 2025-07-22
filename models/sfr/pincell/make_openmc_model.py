import openmc
from numpy import sqrt
from argparse import ArgumentParser
from models.sfr import common_input as pincell_params
import models.sfr.openmc_pincells as pins
from models.lwr.openmc_settings import COMMON_SETTINGS


def argument_parser():
    ap = ArgumentParser(description="SFR Pincell Model Generator")
    ap.add_argument("-n", dest="n_axial", type=int, default=2, help="Number of cells in the Z direction")
    ap.add_argument("-p", dest="pincell_type", type=str, choices=["inner", "outer"], default="inner",
                    help="Material composition of the pincell fuel material")

    return ap.parse_args()


def generate_pincell_model(arguments):
    pincell_universe, material = pins.PINCELLS[arguments.pincell_type]
    fuel_bb = openmc.model.HexagonalPrism(edge_length=pincell_params.lattice_pitch / (sqrt(3)),
                                          boundary_type="reflective", orientation="x")
    top = openmc.ZPlane(z0=pincell_params.height, boundary_type="reflective")
    bottom = openmc.ZPlane(z0=0, boundary_type="reflective")

    pincell_lattice = openmc.HexLattice()
    pincell_lattice.center = (0.0, 0.0, 0.0)
    pincell_lattice.pitch = (pincell_params.lattice_pitch, pincell_params.height / arguments.n_axial)
    pincell_lattice.universes = [[[pincell_universe]] for i in range(arguments.n_axial)]

    pincell_universe_base = openmc.Universe(
        cells=[openmc.Cell(fill=pincell_lattice, region=-fuel_bb & +bottom & - top)])

    return pincell_universe_base, material


if __name__ == "__main__":
    args = argument_parser()
    root_universe, materials = generate_pincell_model(args)
    settings = COMMON_SETTINGS
    settings.source = openmc.IndependentSource(space=openmc.stats.Point((0, 0, pincell_params.height / 2)),
                                               angle=openmc.stats.Isotropic())
    openmc.model.Model(openmc.Geometry(root=root_universe), materials, settings)
