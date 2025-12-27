import numpy as np
from utilities import *


def make_model():
    args = argument_parser()

    bc_map = {
        "left": ['vacuum', 'transmission', 'reflective', 'vacuum', 'reflective', 'reflective'],
        "middle": ['transmission', 'transmission', 'reflective', 'vacuum', 'reflective', 'reflective'],
        "right": ['transmission', 'vacuum', 'reflective', 'vacuum', 'reflective', 'reflective'],
    }

    x_pos = np.linspace(args.x_min, args.x_max, args.Nx + 1)

    fuel = make_materials(material_dict['UO2'], percent_type='ao')
    b4c = make_materials(material_dict['Boron Carbide'], percent_type='ao')
    materials = [fuel, b4c]

    cells = []
    x_uo2_right = (args.x_max - args.x_min)*args.fuel_percentage
    for i in range(args.Nx):

        material = fuel if x_pos[i] < x_uo2_right else b4c
        boundary_conditions = bc_map["left" if i == 0 else "right" if i == args.Nx - 1 else "middle"]
        region = make_box(x_dim=[x_pos[i], x_pos[i + 1]], y_dim=[args.y_min, args.y_max], z_dim=[args.z_min, args.z_max], boundary_conditions=boundary_conditions)
        cells.append(openmc.Cell(region=region, fill=material))

    model = openmc.Model()
    model.geometry = openmc.Geometry(openmc.Universe(cells=cells))
    model.materials = openmc.Materials(materials)
    model.settings = simulation_settings(args, space_dist=openmc.stats.Box(lower_left=(args.x_min, args.y_min, args.z_min), upper_right=(args.x_max, args.y_max, args.z_max)))

    return model


if __name__ == "__main__":
    make_model().export_to_model_xml()
