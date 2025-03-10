material_dict = {
    'outer_fuel': {
        'density': 10.0,
        'composition': {
            "U235": 0.0018,
            "U238": 0.73,
            "Pu238": 0.0053,
            "Pu239": 0.0711,
            "Pu240": 0.0445,
            "Pu241": 0.0124,
            "Pu242": 0.0156,
            "Am241": 0.0017,
            "O16": 0.1176,
        }
    },
    'inner_fuel': {
        'density': 10.0,
        'composition': {
            "U235": 0.0019,
            "U238": 0.7509,
            "Pu238": 0.0046,
            "Pu239": 0.0612,
            "Pu240": 0.0383,
            "Pu241": 0.0106,
            "Pu242": 0.0134,
            "Am241": 0.001,
            "O16": 0.1181,
        }
    },
    'cladding': {
        'density': 10.0,
        'composition': {
            "Cu63": 0.9907996814341512,
            "O16": 0.005507056396711977,
            "O17": 2.0921524418740345e-6,
            "O18": 1.1042590355474455e-5,
            "Al27": 0.00368012742633955,
        }
    },
    'sodium': {
        'density': 0.96,
        'composition': {
            "Na23": 1.0,
        }
    },
    'helium': {
        'density': 0.001598,
        'composition': {
            "He3": 4.8088e-10,
            "He4": 0.00024043951912,
        }
    }
}

def make_sfr_material(material_dict, percent_type: str):
    material = openmc.Material()
    material.set_density('g/cm3', material_dict['density'])

    for nuclide, percent in material_dict['composition'].items():
        material.add_nuclide(
            nuclide, percent=percent, percent_type=percent_type
        )

    return material
