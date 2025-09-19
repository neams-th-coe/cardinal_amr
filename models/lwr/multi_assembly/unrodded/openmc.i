[Mesh]
  [file]
    type = FileMeshGenerator
    file = mesh_in.e
  []
[]

[Problem]
  type = OpenMCCellAverageProblem
  particles = 20000
  inactive_batches = 500
  batches = 10000

  verbose = true
  power = ${fparse 3000e6 / 273 * 4}

  normalize_by_global_tally = false
  source_rate_normalization = 'kappa_fission'
  assume_separate_tallies = true
[]

# Include common tallies.
!include ../../../mesh_tallies.i

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

[Executioner]
  type = Steady
[]

[Outputs]
  exodus = true
  csv = true
[]
