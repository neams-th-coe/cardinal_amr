!include ../../assemblies.i

[Mesh]
  [Delete_Blocks]
    type = BlockDeletionGenerator
    input = UO2_Assembly_Rodded
    # Deleting the gap blocks to avoid erroneous mesh refinement.
    block = '2'
  []
  [To_Origin]
    type = TransformGenerator
    input = 'Delete_Blocks'
    transform = TRANSLATE_CENTER_ORIGIN
  []
  [3D_Core]
    type = AdvancedExtruderGenerator
    input = 'To_Origin'
    heights = '${fparse core_height}'
    num_layers = '${AXIAL_DIVISIONS}'
    direction = '0.0 0.0 1.0'
  []

  final_generator = 3D_Core
[]
