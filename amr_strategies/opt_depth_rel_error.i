[Adaptivity]
  marker = error_combo
  steps = 10

  [Indicators/optical_depth]
    type = ElementOpticalDepthIndicator
    rxn_rate = 'fission'
  []
  [Markers]
    [depth_marker]
      type = ValueThresholdMarker
      variable = 'optical_depth'
      coarsen = 0.0 # Not coarsening based on optical depth, just refining.
      refine = 5e-2
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
      # Only refine iff the relative error is sufficiently low AND the optical depth is
      # sufficiently large.
      refine_markers = 'rel_error depth_marker'
      # Coarsen based exclusively on relative error.
      coarsen_markers = 'rel_error'
      boolean_operator = and
    []
  []
[]
