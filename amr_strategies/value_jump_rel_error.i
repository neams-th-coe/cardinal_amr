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
      refine = 0.3
      coarsen = 0.0
    []
    [rel_error]
      type = ValueThresholdMarker
      invert = true
      coarsen = 1e-1
      refine = 1e-2
      variable = heat_source_rel_error
      third_state = DO_NOTHING
    []
    [error_combo]
      type = BooleanComboMarker
      # Only refine iff the relative error is sufficiently low AND there is a large enough
      # jump discontinuity in the solution.
      refine_markers = 'rel_error error_frac'
      # Coarsen based exclusively on relative error. Jump discontinuities in the solution
      # from large relative errors causes the 'error_frac' marker to erroneously mark elements
      # for refinement.
      coarsen_markers = 'rel_error'
      boolean_operator = and
    []
  []
[]
