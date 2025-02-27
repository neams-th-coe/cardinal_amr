!include pincells.i

[Mesh]
  [UO2_Assembly]
    type = PatternedCartesianMeshGenerator
    inputs = 'UO2_Pin Guide_Tube_Pin Fission_Chamber_Pin'
    pattern = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 1 0 0 1 0 0 1 0 0 0 0 0;
               0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 1 0 0 1 0 0 2 0 0 1 0 0 1 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0;
               0 0 0 0 0 1 0 0 1 0 0 1 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'

    pattern_boundary = 'none'

    assign_type = 'cell'
    id_name = 'pin_id'
    generate_core_metadata = false
  []
  [UO2_Assembly_Rodded]
    type = PatternedCartesianMeshGenerator
    inputs = 'UO2_Pin Control_Rod_Pin Fission_Chamber_Pin'
    pattern = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 1 0 0 1 0 0 1 0 0 0 0 0;
               0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 1 0 0 1 0 0 2 0 0 1 0 0 1 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0;
               0 0 0 0 0 1 0 0 1 0 0 1 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'

    pattern_boundary = 'none'

    assign_type = 'cell'
    id_name = 'pin_id'
    generate_core_metadata = false
  []
  [MOX_Assembly]
    type = PatternedCartesianMeshGenerator
    inputs = 'MOX_4_3_Pin MOX_7_0_Pin MOX_8_7_Pin Guide_Tube_Pin Fission_Chamber_Pin'
    pattern = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
               0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0;
               0 1 1 1 1 3 1 1 3 1 1 3 1 1 1 1 0;
               0 1 1 3 1 2 2 2 2 2 2 2 1 3 1 1 0;
               0 1 1 1 2 2 2 2 2 2 2 2 2 1 1 1 0;
               0 1 3 2 2 3 2 2 3 2 2 3 2 2 3 1 0;
               0 1 1 2 2 2 2 2 2 2 2 2 2 2 1 1 0;
               0 1 1 2 2 2 2 2 2 2 2 2 2 2 1 1 0;
               0 1 3 2 2 3 2 2 4 2 2 3 2 2 3 1 0;
               0 1 1 2 2 2 2 2 2 2 2 2 2 2 1 1 0;
               0 1 1 2 2 2 2 2 2 2 2 2 2 2 1 1 0;
               0 1 3 2 2 3 2 2 3 2 2 3 2 2 3 1 0;
               0 1 1 1 2 2 2 2 2 2 2 2 2 1 1 1 0;
               0 1 1 3 1 2 2 2 2 2 2 2 1 3 1 1 0;
               0 1 1 1 1 3 1 1 3 1 1 3 1 1 1 1 0;
               0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0;
               0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'

    pattern_boundary = 'none'

    assign_type = 'cell'
    id_name = 'pin_id'
    generate_core_metadata = false
  []
[]
