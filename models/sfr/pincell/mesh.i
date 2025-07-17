!include ../pincell.i
[Mesh]
  [Pin_3D]
    type = AdvancedExtruderGenerator
    input = 'Pin'
    heights = '${fparse height}'
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
    vector_value = '0.0 0.0 ${fparse height / 2.0}'
  []

[]
