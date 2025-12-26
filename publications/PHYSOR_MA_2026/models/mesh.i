[Mesh]
  [generated_mesh]
     type = GeneratedMeshGenerator
    nx = 20
    ny = 4
    nz = 4
    xmin = 0.0
    xmax = 100.0
    ymin = 0.0
    ymax = 10.0
    zmin = 0.0
    zmax = 10.0
    dim = 3
  []
  [add_eeid_block]
    type = ParsedElementIDMeshGenerator
    extra_element_integer_names = 'same_flux'
    values = '-1'
    input = generated_mesh
  []
[]
