# The number of refinement cycles.
num_cycles = 10

# The upper error fraction. Elements are sorted from highest to lowest error,
# and then the elements with the largest error that sum to r_error_fraction
# multiplied by the total error are refined. This refinement scheme assumes
# error is well approximated by the jump discontinuity in the neutron current.
r_error_fraction = 0.3

# The upper limit of statistical relative error - elements with a relative error larger
# then r_stat_error will not be refined.
r_stat_error = 1e-2

# The lower limit of statistical relative error - elements with a relative error larger
# then c_stat_error will be coarsened.
c_stat_error = 1e-1

[AuxVariables]
  [current]
    family = MONOMIAL_VEC
    order = CONSTANT
  []
  [current_mag]
    family = MONOMIAL
    order = CONSTANT
  []
[]

[AuxKernels]
  [current]
    type = ParsedVectorAux
    variable = current
    coupled_variables = 'flux_l1_mneg1 flux_l1_mpos0 flux_l1_mpos1'
    expression_x = 'flux_l1_mpos1'
    expression_y = 'flux_l1_mneg1'
    expression_z = 'flux_l1_mpos0'
  []
  [current_mag]
    type = VectorVariableMagnitudeAux
    variable = current_mag
    vector_variable = current
  []
[]

[Adaptivity]
  marker = error_combo
  steps = ${num_cycles}

  [Markers]
    [error_frac]
      type = ErrorFractionMarker
      indicator = current_mag
      refine = ${r_error_fraction}
      coarsen = 0.0
    []
    [rel_error]
      type = ValueThresholdMarker
      invert = true
      coarsen = ${c_stat_error}
      refine = ${r_stat_error}
      variable = flux_l0_mpos0_rel_error
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
