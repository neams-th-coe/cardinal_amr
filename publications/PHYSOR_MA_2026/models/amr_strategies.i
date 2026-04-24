!include ../../../../amr_strategies/value_jump_rel_error.i

R_ERROR_FRACTION := 0.2
R_STAT_ERROR := 0.05


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

