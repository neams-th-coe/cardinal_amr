# The number of refinement cycles.
num_cycles = 10

# The upper error fraction. Elements are sorted from highest to lowest error,
# and then the elements with the largest error that sum to r_error_fraction
# multiplied by the total error are refined. This refinement scheme assumes
# error is well approximated by the jump discontinuity in the tally gradients
# (computed with finite differences).
r_error_fraction = 0.3

# The upper limit of statistical relative error - elements with a relative error larger
# then r_stat_error will not be refined.
r_stat_error = 1e-2

# The lower limit of statistical relative error - elements with a relative error larger
# then c_stat_error will be coarsened.
c_stat_error = 1e-1

[AuxVariables]
  [grad_kappa_fission]
    family = MONOMIAL_VEC
    order = CONSTANT
  []
[]

[AuxKernels]
  [grad_kappa_fission]
    type = FDTallyGradAux
    variable = grad_kappa_fission
    score = 'kappa_fission'
  []
[]

[Adaptivity]
  marker = error_combo
  steps = ${num_cycles}

  [Indicators/error]
    type = VectorValueJumpIndicator
    variable = grad_kappa_fission
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
