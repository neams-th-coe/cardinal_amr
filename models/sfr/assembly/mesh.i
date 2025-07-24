!include ../pincell.i
[Mesh]
    [Assembly_2D]
        type = PatternedHexMeshGenerator
        inputs = 'Pin'
        pattern =        "0 0 0 0 0 0 0 0 0;
                         0 0 0 0 0 0 0 0 0 0;
                        0 0 0 0 0 0 0 0 0 0 0;
                       0 0 0 0 0 0 0 0 0 0 0 0;
                      0 0 0 0 0 0 0 0 0 0 0 0 0;
                     0 0 0 0 0 0 0 0 0 0 0 0 0 0;
                    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
                   0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
                  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
                   0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
                    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
                     0 0 0 0 0 0 0 0 0 0 0 0 0 0;
                      0 0 0 0 0 0 0 0 0 0 0 0 0;
                       0 0 0 0 0 0 0 0 0 0 0 0;
                        0 0 0 0 0 0 0 0 0 0 0;
                         0 0 0 0 0 0 0 0 0 0;
                          0 0 0 0 0 0 0 0 0"

         hexagon_size = '${fparse edge_length}'
    []
    [Assembly_3D]
        type = AdvancedExtruderGenerator
        input = 'Assembly_2D'
        heights = '${fparse height}'
        num_layers = '${AXIAL_DIVISIONS}'
        direction = '0.0 0.0 1.0'

      []
      [To_Origin]
        type = TransformGenerator
        input = 'Assembly_3D'
        transform = TRANSLATE_CENTER_ORIGIN
      []
      [Down]
        type = TransformGenerator
        input = 'To_Origin'
        transform = TRANSLATE
        vector_value = '0.0 0.0 ${fparse height / 2.0}'
      []

[]
