[Mesh]
  [file]
    type = FileMeshGenerator
    file = mesh_in.e
  []
[]

[Adaptivity]
  marker = error_combo
  steps = 10

  [Indicators/error]
    type = ValueJumpIndicator
    variable = heat_source
  []
  [Markers]
    [error_frac]
      type = ErrorFractionMarker
      indicator = error
      refine = 0.7
      coarsen = 0.0
    []
    [rel_error]
      type = ValueThresholdMarker
      invert = true
      coarsen = 2e-1
      refine = 1e-2
      variable = heat_source_rel_error
      third_state = DO_NOTHING
    []
    [error_combo]
      type = BooleanComboMarker
      refine_markers = 'rel_error error_frac'
      coarsen_markers = 'rel_error'
      boolean_operator = and
    []
  []
[]

[Problem]
  type = OpenMCCellAverageProblem
  particles = 20000
  inactive_batches = 40
  batches = 250

  verbose = true
  power = ${fparse 3000e6 / 273 / (17 * 17)}
  cell_level = 1
  normalize_by_global_tally = false

  [Tallies]
    [heat_source]
      type = MeshTally
      score = 'kappa_fission'
      name = heat_source
      output = 'unrelaxed_tally_rel_error'
    []
  []
[]

[Executioner]
  type = Steady
[]

[Postprocessors]
  [num_active]
    type = NumElems
    elem_filter = active
  []
  [num_total]
    type = NumElems
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
