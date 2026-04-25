!include mesh.i
!include clustering.i
!include amr_strategies.i

[AuxVariables]
  [aux_same_flux]
      order = CONSTANT
      family = MONOMIAL
  []
    [hierarchy]
        order = CONSTANT
        family = MONOMIAL
    []
[]

[AuxKernels]
  [hierarchy_aux_kernel]
    type=ElementAdaptivityLevelAux
    variable=hierarchy
    level='h'
  []
  [store_same_flux]
      type = ExtraElementIDAux
      extra_id_name = same_flux
      variable = aux_same_flux
  []
[]

[Problem]
    type = OpenMCCellAverageProblem
    particles = 35000
    inactive_batches = 500
    batches = 1500
    reset_seed=true

    verbose = true
    power = ${fparse 3000e6 / 273}

    normalize_by_global_tally = false
    source_rate_normalization = 'kappa_fission'
    assume_separate_tallies = true

    [Tallies]
        [heat_source]
            type = MeshTally
            score = 'kappa_fission scatter flux fission'
            name = 'kappa_fission scatter flux fission'
            mesh_tally_amalgamation = true
            clustering_name = same_flux
            output = 'unrelaxed_tally_rel_error'
        []
    []
[]

[Postprocessors]
    [num_active]
        type = NumElements
        elem_filter = active
    []
    [num_total]
        type = NumElements
        elem_filter = total
    []
    [max_rel_err]
        type = TallyRelativeError
        value_type = max
        tally_score = scatter
    []

[]

[Executioner]
    type = Steady
[]

[Outputs]
  [out]
    type = Exodus
    execute_on = timestep_end
    output_extra_element_ids = true
    extra_element_ids_to_output = 'same_flux'
  []
[]
