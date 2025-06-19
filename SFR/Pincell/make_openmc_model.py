import openmc
from argparse import ArgumentParser
from SFR.materials import make_sfr_material, material_dict
from SFR import common_input as pincell_params


def simulation_settings():
    setting = openmc.Settings()
    setting.source = openmc.IndependentSource(space=openmc.stats.Point((0, 0, pincell_params.height / 2)), angle=openmc.stats.Isotropic())
    setting.batches = 200
    setting.inactive = 40
    setting.particles = 2000
    setting.temperature = {"default": 553.15, "method": "interpolation", "range": (290.0, 3000.0)}
    return setting


def argument_parser():
    ap = ArgumentParser(description="SFR Pincell Model Generator")
    ap.add_argument("-n", dest="n_axial", type=int, default=1, help="Number of cells in the Z direction")
    ap.add_argument("-p", dest="pincell_type", type=str, choices=["inner", "outer"], default="inner", help="Material composition of the pincell fuel material")

    return ap.parse_args()


def get_pincell_universe(arguments):
    fuel_mat_name = f'{arguments.pincell_type}_fuel'

    fuel_material = make_sfr_material(material_dict[fuel_mat_name], percent_type='wo')
    cladding_material = make_sfr_material(material_dict['cladding'], percent_type='ao')
    helium = make_sfr_material(material_dict['helium'], percent_type='ao')
    sodium = make_sfr_material(material_dict['sodium'], percent_type='ao')

    fuel_or = openmc.ZCylinder(r=pincell_params.r_fuel)
    clad_ir = openmc.ZCylinder(r=pincell_params.r_clad_inner)
    clad_or = openmc.ZCylinder(r=(pincell_params.r_clad_inner + pincell_params.t_clad))

    cladding_cell = openmc.Cell(fill=cladding_material, region=+clad_ir & -clad_or)
    gas_gap_cell = openmc.Cell(fill=helium, region=+fuel_or & -clad_ir)
    fuel_cell = openmc.Cell(fill=fuel_material, region=-fuel_or)
    sodium_cell = openmc.Cell(fill=sodium, region=+clad_or)

    return openmc.Universe(cells=[cladding_cell, gas_gap_cell, fuel_cell, sodium_cell]), openmc.Materials([fuel_material, helium, cladding_material, sodium])


def generate_pincell_model(arguments):
    pincell_universe, material = get_pincell_universe(arguments)

    fuel_bb = openmc.model.HexagonalPrism(edge_length=pincell_params.edge_length, boundary_type="reflective", orientation='y')
    top = openmc.ZPlane(z0=pincell_params.height, boundary_type="reflective")
    bottom = openmc.ZPlane(z0=0, boundary_type="reflective")

    sodium = make_sfr_material(material_dict['sodium'], percent_type='ao')
    material.append(sodium)

    pincell_lattice = openmc.HexLattice()
    pincell_lattice.center = (0.0, 0.0, 0.0)
    pincell_lattice.orientation = "y"
    pincell_lattice.outer = openmc.Universe(cells=[openmc.Cell(fill=sodium)])
    pincell_lattice.pitch = (pincell_params.pitch, pincell_params.height / pincell_params.AXIAL_DIVISIONS)
    pincell_lattice.universes = [[[pincell_universe]] for i in range(arguments.n_axial)]
    pincell_universe_base = openmc.Universe(cells=[openmc.Cell(fill=pincell_lattice, region=-fuel_bb & +bottom & - top)])

    return pincell_universe_base, material


if __name__ == "__main__":
    args = argument_parser()
    root_universe, materials = generate_pincell_model(args)
    openmc.model.Model(openmc.Geometry(root=root_universe), materials, simulation_settings()).export_to_model_xml()
