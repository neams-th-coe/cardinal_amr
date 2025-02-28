outer_fuel_material_dict = {
    "U235": {"density": 10.0, "percent": 0.0018},
    "U238": {"density": 10, "percent": 0.73},
    "Pu238": {"density": 10, "percent": 0.0053},
    "Pu239": {"density": 10, "percent": 0.0711},
    "Pu240": {"density": 10, "percent": 0.0445},
    "Pu241": {"density": 10, "percent":  0.0124},
    "Pu242": {"density": 10, "percent":  0.0156},
    "Am241": {"density": 10, "percent": 0.0017},
    "O16": {"density": 10, "percent": 0.1176},
}  # fuel material data in weight percentage and density in g/cm3
inner_fuel_material_dict = {
    "U235": {"density": 10.0, "percent": 0.0019},
    "U238": {"density": 10, "percent": 0.7509},
    "Pu238": {"density": 10, "percent": 0.0046},
    "Pu239": {"density": 10, "percent": 0.0612},
    "Pu240": {"density": 10, "percent": 0.0383},
    "Pu241": {"density": 10, "percent": 0.0106},
    "Pu242": {"density": 10, "percent": 0.0134},
    "Am241": {"density": 10, "percent": 0.001},
    "O16": {"density": 10, "percent": 0.1181},
}  # fuel material data in weight percentage and density in g/cm3

cladding_material_dict = {
    "Cu63": {"density": 10.0, "percent": 0.9907996814341512},
    "O16": {"density": 10.0, "percent": 0.005507056396711977},
    "O17": {"density": 10.0, "percent": 2.0921524418740345e-6},
    "O18": {"density": 10.0, "percent": 1.1042590355474455e-5},
    "Al27": {"density": 10.0, "percent": 0.00368012742633955},
}  # cladding data in atom percentage and density in g/cm3

sodium_material_dict = {"Na23": {"density": 0.96, "percent": 1}}# sodium in atom percentage and density in g/cm3
heilum_material_dict = {
    "He3": {"density": 0.001598, "percent": 4.8088e-10},
    "He4": {"density": 0.001598, "percent": 0.00024043951912},
}# heilum in atom percentage and density in g/cm3
