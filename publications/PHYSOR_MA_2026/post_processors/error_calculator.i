union_mesh_file_name = common_mesh_out.e-s004
ref_mesh_file_name = openmc_out.e
test_mesh_file_name = openmc_out.e

tally_variable="flux"
tally_rel_error_variable="flux_rel_error"
variables="${tally_variable} ${tally_rel_error_variable}"

[Mesh]
    [file_mesh_generator]
        type = FileMeshGenerator
        file = ${union_mesh_file_name}
        use_for_exodus_restart = true
    []
[]

[AuxVariables]
    [ref_mean]
        order = CONSTANT
        family = MONOMIAL
    []
    [ref_rel_stat_error]
        order = CONSTANT
        family = MONOMIAL
    []
    [test_mean]
        order = CONSTANT
        family = MONOMIAL
    []
    [test_rel_stat_error]
        order = CONSTANT
        family = MONOMIAL
    []
    [rel_discrepancy_mean]
        order = CONSTANT
        family = MONOMIAL
    []
    [rel_discrepancy_stat_error]
        order = CONSTANT
        family = MONOMIAL
    []
    [z_score]
        order = CONSTANT
        family = MONOMIAL
    []
[]

[AuxKernels]
  [load_ref_sln_mean]
    type= SolutionAux
    solution = ref_sln_user_obj
    variable = ref_mean
    from_variable =${tally_variable}
  []
  [load_ref_sln_stat_error]
    type= SolutionAux
    solution = ref_sln_user_obj
    variable = ref_rel_stat_error
    from_variable = ${tally_rel_error_variable}
  []
  [load_test_sln_mean]
    type= SolutionAux
    solution = test_sln_user_obj
    variable = test_mean
    from_variable = ${tally_variable}
  []
  [load_test_sln_stat_error]
    type= SolutionAux
    solution = test_sln_user_obj
    variable = test_rel_stat_error
    from_variable = ${tally_rel_error_variable}
  []

  [tally_relative_discrepancy_calculation]

    type = ParsedAux
    variable = rel_discrepancy_mean
    coupled_variables = 'test_mean ref_mean'
    expression = '( ref_mean - test_mean )/ ref_mean'

  []

  [tally_error_discrepancy_calculation]
    type = ParsedAux
    variable = rel_discrepancy_stat_error
    coupled_variables = 'ref_rel_stat_error test_rel_stat_error'
    expression = '( test_rel_stat_error - ref_rel_stat_error )/ ref_rel_stat_error'
  []

  [z_score_calculation]
    type = ParsedAux
    variable = z_score
    coupled_variables = 'ref_rel_stat_error rel_discrepancy_mean'
    expression = 'rel_discrepancy_mean / ref_rel_stat_error '
  []

[]

[UserObjects]
    [ref_sln_user_obj]
        type = SolutionUserObject
        mesh = ${ref_mesh_file_name}
        system_variables = ${variables}
    []
    [test_sln_user_obj]
        type = SolutionUserObject
        mesh = ${test_mesh_file_name}
        system_variables =  ${variables}
    []
[]

[VectorPostprocessors]
  [csv_data_extractor]
    type = ElementValueSampler
    sort_by = "x"
    variable = "test_mean ref_mean test_rel_stat_error ref_rel_stat_error z_score"
    execute_on = 'initial timestep_end'
  []
[]

[Problem]
  type = FEProblem
  solve = false
[]

[Executioner]
  type = Steady
  solve = false
[]

[Outputs]
  exodus = true
  csv = true
[]
