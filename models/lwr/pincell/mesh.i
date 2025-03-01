!include ../pincells.i

[Mesh]
  [Pin_3D]
    type = AdvancedExtruderGenerator
    input = 'UO2_Pin'
    heights = '${fparse core_height}'
    num_layers = '${AXIAL_DIVISIONS}'
    direction = '0.0 0.0 1.0'
  []
  [To_Origin]
    type = TransformGenerator
    input = 'Pin_3D'
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
