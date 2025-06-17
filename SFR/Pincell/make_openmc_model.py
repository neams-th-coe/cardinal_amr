import openmc
import numpy as np
from argparse import ArgumentParser
import openmc.material

from SFR.materials import make_sfr_material, material_dict
from SFR import common_input as pincell_params


def simulation_settings(shannon_entropy: bool, height: float):
    fuel_radius = pincell_params.r_fuel
    lower_left = (-fuel_radius, -fuel_radius, 0.0)
    upper_right = (fuel_radius, fuel_radius, height)

    setting = openmc.Settings()
    setting.source = openmc.IndependentSource(
        space=openmc.stats.Point((0, 0, pincell_params.height / 2)),
        angle=openmc.stats.Isotropic())
    setting.batches = 200
    setting.inactive = 40
    setting.particles = 20000

    if shannon_entropy:
        entropy_mesh = openmc.RegularMesh()
        entropy_mesh.lower_left = lower_left
        entropy_mesh.upper_right = upper_right
        entropy_mesh.dimension = (10, 10, 20)
        setting.entropy_mesh = entropy_mesh

    setting.temperature = {
        "default": 553.15,
        "method": "interpolation",
        "range": (290.0, 3000.0)
    }
    return setting


def argument_parser():
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
    ap.add_argument("-p", dest="pincell_type", type=str, choices=["inner", "outer"],
                    default="inner",
                    help="Material composition of the pincell fuel material")

    return ap.parse_args()


def model_generate(arguments):
    """
    :return:
    a pincell universe,
    openmc.Materials class,
    openmc.Geometry class,
    openmc.Settings class

    the universe class is mostly for reuse if we want to create an assembly
    """
    fuel_mat_name = f'{arguments.pincell_type}_fuel'
    fuel_material = make_sfr_material(material_dict[fuel_mat_name], percent_type='wo')
    cladding_material = make_sfr_material(material_dict['cladding'], percent_type='ao')
    sodium = make_sfr_material(material_dict['sodium'], percent_type='ao')
    helium = make_sfr_material(material_dict['helium'], percent_type='ao')

    fuel_or = openmc.ZCylinder(r=pincell_params.r_fuel)
    clad_ir = openmc.ZCylinder(r=pincell_params.r_clad_inner)
    clad_or = openmc.ZCylinder(r=(pincell_params.r_clad_inner + pincell_params.t_clad))
    fuel_bb = openmc.model.RectangularPrism(width=pincell_params.pitch,
                                            height=pincell_params.height / arguments.n_axial,
                                            boundary_type="reflective")
    top = openmc.ZPlane(z0=pincell_params.height, boundary_type="reflective")
    bottom = openmc.ZPlane(z0=0, boundary_type="vacuum")

    cladding_cell = openmc.Cell(fill=cladding_material, region=+clad_ir & -clad_or)
    gas_gap_cell = openmc.Cell(fill=helium, region=+fuel_or & -clad_ir)
    fuel_cell = openmc.Cell(fill=fuel_material, region=-fuel_or)
    sodium_cell = openmc.Cell(region=+clad_or & -fuel_bb & +bottom & - top, fill=sodium)
    pincell_universe = openmc.Universe(cells=[cladding_cell, gas_gap_cell, fuel_cell])

    pincell_lattice = openmc.RectLattice()
    pincell_lattice.pitch = (
        pincell_params.pitch, pincell_params.pitch,
        pincell_params.height / arguments.n_axial)
    pincell_lattice.lower_left = (
        -pincell_params.pitch / 2.0, -pincell_params.pitch / 2.0, 0.0)
    pincell_lattice.universes = [[[pincell_universe]] for i in range(arguments.n_axial)]

    return pincell_universe, openmc.Materials(
        [fuel_material, sodium, helium, cladding_material]), openmc.Geometry(
        [openmc.Cell(fill=pincell_lattice, region=-fuel_bb & +bottom & - top), sodium_cell]), simulation_settings(
        arguments.shannon_entropy, height=pincell_params.height)


if __name__ == "__main__":
    args = argument_parser()
    _, mat, geometry, settings = model_generate(args)
    openmc.model.Model(geometry, mat, settings).export_to_model_xml()
