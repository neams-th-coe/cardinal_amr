[Mesh]
  [file]
    type = FileMeshGenerator
    file = mesh_in.e
  []
[]

[Problem]
  type = OpenMCCellAverageProblem
  particles = 20000
  inactive_batches = 50
  batches = 150

  verbose = true
  power = ${fparse 3000e6/3000}
  cell_level = 1
  normalize_by_global_tally = false
[]

# Include common tallies.
!include ../../mesh_tallies.i

[Executioner]
  type = Steady
[]

[Postprocessors]
  [num_active]
    type = NumElements
    elem_filter = active
  []
  [num_total]
    type = NumElements
    elem_filter = total
  []
  [max_rel_err]
    type = TallyRelativeError
    value_type = max
    tally_score = kappa_fission
  []
[]

[Outputs]
  exodus = true
  csv = true
[]
