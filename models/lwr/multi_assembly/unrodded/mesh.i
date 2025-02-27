!include ../../assemblies.i

[Mesh]
  [2D_Core]
    type = PatternedCartesianMeshGenerator
    inputs = 'UO2_Assembly MOX_Assembly'
    pattern = '0 1;
               1 0'

    pattern_boundary = 'none'
    external_boundary_name = 'reflector_interface'

    assign_type = 'cell'
    id_name = 'pin_id'
    generate_core_metadata = true
  []
  [Delete_Blocks]
    type = BlockDeletionGenerator
    input = 2D_Core
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
