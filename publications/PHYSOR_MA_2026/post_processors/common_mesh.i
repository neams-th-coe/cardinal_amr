ref_mesh_file_name=gt.e-s011
test_mesh_file_name=hex_same_flux_high_err_ma.e-s010

!include ../models/mesh.i

[AuxVariables]
    [ref_solution_hierarchy]
        order = CONSTANT
        family = MONOMIAL
    []
    [test_solution_hierarchy]
        order = CONSTANT
        family = MONOMIAL
    []
    [max_elemental_hierarchy]
        order = CONSTANT
        family = MONOMIAL
    []
    [adaptive_hierarchy]
        order = CONSTANT
        family = MONOMIAL
    []
    [element_refinement_step]
        order = CONSTANT
        family = MONOMIAL
    []
[]

[AuxKernels]
  [load_ref_sln_hierarchy]
    type= SolutionAux
    solution = ref_solution_hierarchy_user_object
    variable = ref_solution_hierarchy
  []
  [load_test_sln_hierarchy]
    type= SolutionAux
    solution = test_solution_hierarchy_user_object
    variable = test_solution_hierarchy
  []
  [calc_max_element_hierarchy]
    type = ParsedAux
    variable = max_elemental_hierarchy
    coupled_variables = 'test_solution_hierarchy ref_solution_hierarchy'
    expression = 'max(test_solution_hierarchy, ref_solution_hierarchy)'
  []
  [adaptive_hierarchy_aux]
    type=ElementAdaptivityLevelAux
    variable=adaptive_hierarchy
    level='h'
  []
  [calc_remaining_refinement_steps]
    type = ParsedAux
    variable = element_refinement_step
    coupled_variables = 'adaptive_hierarchy max_elemental_hierarchy'
    expression = 'abs(max_elemental_hierarchy - adaptive_hierarchy)'
  []
[]

[Adaptivity]
    marker = marker
    steps = 1

  [Markers]
    [marker]
      # for an element  We should be
      # refining untill the element_refinement_step is zero
      type = ValueThresholdMarker
      coarsen = -2
      refine = 0.7
      variable = element_refinement_step
    []

  []
[]

[UserObjects]
    [ref_solution_hierarchy_user_object]
        type = SolutionUserObject
        mesh = ${ref_mesh_file_name}
        system_variables = hierarchy
        timestep = 1
    []

   [test_solution_hierarchy_user_object]
        type = SolutionUserObject
        mesh = ${test_mesh_file_name}
        system_variables = hierarchy
        timestep = 1
    []
[]

[Problem]
  type = FEProblem
  solve = false
[]

[Executioner]
  type = Transient
  solve = false
  dt = 1
  num_steps = 4
[]

[Outputs]
  exodus = true
[]
