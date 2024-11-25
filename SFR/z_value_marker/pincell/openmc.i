[Mesh]
  [file]
    type = FileMeshGenerator
    file = mesh_in.e
  []
[]

[AuxVariables]
  [n_elements]
  []
  [mean_heat_source]
    order = CONSTANT
    family = MONOMIAL

  []
  [std_heat_source]
    order = CONSTANT
    family = MONOMIAL
  []
  [z_scores]
    order = CONSTANT
    family = MONOMIAL
  []
[]

[AuxKernels]

  [std_heat_source]
    type=ParsedAux
    variable=std_heat_source
    coupled_variables = 'heat_source mean_heat_source n_elements'
    expression='sqrt((heat_source-mean_heat_source)*(heat_source-mean_heat_source)/n_elements)'
    execute_on = 'TIMESTEP_END'
    order=1
  []
  [z_scores]
    type = ParsedAux
    variable = z_scores
    coupled_variables = 'heat_source mean_heat_source std_heat_source'
    expression = '(heat_source - mean_heat_source) / std_heat_source'
    execute_on = 'TIMESTEP_END'
    order=2

  []
[]

[Problem]
  type = OpenMCCellAverageProblem
  particles = 2000
  inactive_batches = 50
  batches = 150

  verbose = true
  power = ${fparse 3000e6 / 273 / (17 * 17)}
  cell_level = 1
  normalize_by_global_tally = false

  [Tallies]
    [heat_source]
      type = MeshTally
      score = 'kappa_fission'
      name = heat_source
      output = 'unrelaxed_tally_rel_error'
    []
  []
[]


[Adaptivity]
  marker = z_score_marker
  steps = 10

  [Markers]
    [z_score_marker]
      type = ValueRangeMarker
      variable = z_scores
      lower_bound = -10.0
      upper_bound = 10.0
      third_state = DO_NOTHING
    []
  []
[]

[Postprocessors]
  [n_elements]
    type = NumElements
    execute_on = 'TIMESTEP_END'
  []

  [mean_heat_source]
    type=ElementAverageValue
    variable=heat_source
    execute_on = 'TIMESTEP_END'
  []
[]
[Executioner]
  type = Steady
[]

[Outputs]
  exodus = true
  csv = true
  console = true
[]
