!include common_input.i
[Mesh]
  [Pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides ='${NUM_SIDES}'
    num_sectors_per_side = "${NUM_SECTORS_PER_SIDE}"
    ring_radii = '${r_fuel} ${fparse r_clad_inner} ${fparse r_fuel + t_gap + t_clad}'
    ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1 1'
    polygon_size = ${fparse lattice_pitch/ 2.0}

    ring_block_ids = '0 1 2 3'
    ring_block_names = 'fuel_center fuel gap cladding'
    background_block_ids = '4'
    background_block_names = 'sodium'
    background_intervals = ${BACKGROUND_DIVISIONS}

    flat_side_up = false
    quad_center_elements = false
    preserve_volumes = true
    create_outward_interface_boundaries = false
  []
[]
