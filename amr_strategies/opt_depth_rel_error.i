# The number of refinement cycles.
num_cycles = 10

# The upper error fraction. Elements are sorted from highest to lowest error,
# and then the elements with the largest error that sum to r_error_fraction
# multiplied by the total error are refined. This refinement scheme assumes
# error is well approximated by the optical depth.
r_error_fraction = 0.3

# The upper limit of statistical relative error - elements with a relative error larger
# then r_stat_error will not be refined.
r_stat_error = 1e-2

# The lower limit of statistical relative error - elements with a relative error larger
# then c_stat_error will be coarsened.
c_stat_error = 1e-1

[Adaptivity]
  marker = error_combo
  steps = ${num_cycles}

  [Indicators/optical_depth]
    type = ElementOpticalDepthIndicator
    rxn_rate = 'fission'
    h_type = 'cube_root'
  []
  [Markers]
    [depth_frac]
      type = ErrorFractionMarker
      indicator = optical_depth
      refine = ${r_error_fraction}
      coarsen = 0.0
    []
    [rel_error]
      type = ValueThresholdMarker
      invert = true
      coarsen = ${c_stat_error}
      refine = ${r_stat_error}
      variable = heat_source_rel_error
      third_state = DO_NOTHING
    []
    [error_combo]
      type = BooleanComboMarker
      # Only refine iff the relative error is sufficiently low AND the optical depth is
      # sufficiently large.
      refine_markers = 'rel_error depth_frac'
      # Coarsen based exclusively on relative error.
      coarsen_markers = 'rel_error'
      boolean_operator = and
    []
  []
[]
