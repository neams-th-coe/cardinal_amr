[UserObjects]
    [value_difference]
        type = ValueDifferenceHeuristicUserObject
        metric_variable_name = flux
        tolerance = 0.1
        execute_on = TIMESTEP_BEGIN
    []
    [high_relative_error]
        type = ValueFractionHeuristicUserObject
        metric_variable_name = flux_rel_error
        upper_fraction = 0.4
        lower_fraction = 0
        execute_on = TIMESTEP_BEGIN
    []
    [clustering]
        type = BooleanComboClusteringUserObject
        id_name = "same_flux"
        expression = "( value_difference and high_relative_error )"
        execute_on = TIMESTEP_BEGIN
    []
[]
