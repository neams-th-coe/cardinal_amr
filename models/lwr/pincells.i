!include common.i

[Mesh]
  [UO2_Pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides = 4
    num_sectors_per_side = '${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS}'
    ring_radii = '${r_fuel} ${fparse r_fuel + t_f_c_gap} ${fparse r_fuel + t_f_c_gap + t_zr_clad}'
    ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1 1'
    polygon_size = ${fparse pitch / 2.0}

    ring_block_ids = '0 1 2 3'
    ring_block_names = 'uo2_center uo2 gap_1 zr_clad'
    background_block_ids = '17'
    background_block_names = 'water'
    background_intervals = ${BACKGROUND_DIVISIONS}

    flat_side_up = true
    quad_center_elements = false
    preserve_volumes = true

    create_outward_interface_boundaries = false
  []
  [MOX_4_3_Pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides = 4
    num_sectors_per_side = '${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS}'
    ring_radii = '${r_fuel} ${fparse r_fuel + t_f_c_gap} ${fparse r_fuel + t_f_c_gap + t_zr_clad}'
    ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1 1'
    polygon_size = ${fparse pitch / 2.0}

    ring_block_ids = '4 5 2 3'
    ring_block_names = 'mox_43_center mox_43 gap_1 zr_clad'
    background_block_ids = '17'
    background_block_names = 'water'
    background_intervals = ${BACKGROUND_DIVISIONS}

    flat_side_up = true
    quad_center_elements = false
    preserve_volumes = true

    create_outward_interface_boundaries = false
  []
  [MOX_7_0_Pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides = 4
    num_sectors_per_side = '${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS}'
    ring_radii = '${r_fuel} ${fparse r_fuel + t_f_c_gap} ${fparse r_fuel + t_f_c_gap + t_zr_clad}'
    ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1 1'
    polygon_size = ${fparse pitch / 2.0}

    ring_block_ids = '6 7 2 3'
    ring_block_names = 'mox_70_center mox_70 gap_1 zr_clad'
    background_block_ids = '17'
    background_block_names = 'water'
    background_intervals = ${BACKGROUND_DIVISIONS}

    flat_side_up = true
    quad_center_elements = false
    preserve_volumes = true

    create_outward_interface_boundaries = false
  []
  [MOX_8_7_Pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides = 4
    num_sectors_per_side = '${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS}'
    ring_radii = '${r_fuel} ${fparse r_fuel + t_f_c_gap} ${fparse r_fuel + t_f_c_gap + t_zr_clad}'
    ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1 1'
    polygon_size = ${fparse pitch / 2.0}

    ring_block_ids = '8 9 2 3'
    ring_block_names = 'mox_87_center mox_87 gap_1 zr_clad'
    background_block_ids = '17'
    background_block_names = 'water'
    background_intervals = ${BACKGROUND_DIVISIONS}

    flat_side_up = true
    quad_center_elements = false
    preserve_volumes = true

    create_outward_interface_boundaries = false
  []
  [Guide_Tube_Pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides = 4
    num_sectors_per_side = '${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS}'
    ring_radii = '${r_guide} ${fparse r_guide + t_al_clad}'
    ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1'
    polygon_size = ${fparse pitch / 2.0}

    ring_block_ids = '10 11 12'
    ring_block_names = 'guide_center guide al_clad'
    background_block_ids = '17'
    background_block_names = 'water'
    background_intervals = ${BACKGROUND_DIVISIONS}

    flat_side_up = true
    quad_center_elements = false
    preserve_volumes = true

    create_outward_interface_boundaries = false
  []
  [Control_Rod_Pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides = 4
    num_sectors_per_side = '${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS}'
    ring_radii = '${r_guide} ${fparse r_guide + t_al_clad}'
    ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1'
    polygon_size = ${fparse pitch / 2.0}

    ring_block_ids = '13 14 12'
    ring_block_names = 'cr_center cr al_clad'
    background_block_ids = '17'
    background_block_names = 'water'
    background_intervals = ${BACKGROUND_DIVISIONS}

    flat_side_up = true
    quad_center_elements = false
    preserve_volumes = true

    create_outward_interface_boundaries = false
  []
  [Fission_Chamber_Pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides = 4
    num_sectors_per_side = '${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS}'
    ring_radii = '${r_guide} ${fparse r_guide + t_al_clad}'
    ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1'
    polygon_size = ${fparse pitch / 2.0}

    ring_block_ids = '15 16 12'
    ring_block_names = 'fission_center fission al_clad'
    background_block_ids = '17'
    background_block_names = 'water'
    background_intervals = ${BACKGROUND_DIVISIONS}

    flat_side_up = true
    quad_center_elements = false
    preserve_volumes = true

    create_outward_interface_boundaries = false
  []
[]
