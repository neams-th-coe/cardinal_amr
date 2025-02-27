!include ../pincells.i

[Mesh]
  [Core_2D]
    type = PatternedCartesianMeshGenerator
    inputs = 'UO2_Pin'
    pattern = '0 0 0;
               0 0 0;
               0 0 0'

    pattern_boundary = 'none'

    external_boundary_id = 0
    external_boundary_name = 'vacuum'

    assign_type = 'cell'
    id_name = 'pin_id'
    generate_core_metadata = false
  []
  [Core_3D]
    type = AdvancedExtruderGenerator
    input = 'Core_2D'
    heights = '${fparse core_height}'
    num_layers = '${AXIAL_DIVISIONS}'
    direction = '0.0 0.0 1.0'

    bottom_boundary = '10001'
    top_boundary = '10000'
  []
  [To_Origin]
    type = TransformGenerator
    input = 'Core_3D'
    transform = TRANSLATE_CENTER_ORIGIN
  []
  [Down]
    type = TransformGenerator
    input = 'To_Origin'
    transform = TRANSLATE
    vector_value = '0.0 0.0 ${fparse core_height / 2.0}'
  []
  [Delete_Gap]
    type = BlockDeletionGenerator
    input = Down
    block = '2'
  []

  final_generator = Delete_Gap
[]
