num_cycles = 10
r_error_fraction = 0.2
r_stat_error = 0.05
c_stat_error = 1e-1

[Adaptivity]
  marker = error_combo
  steps = ${num_cycles}

  [Indicators/error]
    type = ValueJumpIndicator
    variable = flux
  []
  [Markers]
    [error_frac]
      type = ErrorFractionMarker
      indicator = error
      refine = ${r_error_fraction}
      coarsen = 0.0
    []
    [rel_error]
      type = ValueThresholdMarker
      invert = true
      coarsen = ${c_stat_error}
      refine = ${r_stat_error}
      variable = flux_rel_error
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

