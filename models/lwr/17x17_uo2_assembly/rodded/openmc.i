[Mesh]
  [file]
    type = FileMeshGenerator
    file = mesh_in.e
  []
[]

[Problem]
  type = OpenMCCellAverageProblem
  particles = 20000
  inactive_batches = 500
  batches = 10000

  verbose = true
  power = ${fparse 3000e6 / 273}

  normalize_by_global_tally = false
  source_rate_normalization = 'kappa_fission'
  assume_separate_tallies = true

  [Tallies]
    [heat_source]
      type = MeshTally
      score = 'kappa_fission flux fission'
      name = 'heat_source flux fission'
      output = 'unrelaxed_tally_std_dev unrelaxed_tally_rel_error'
    []
  []
[]

[Executioner]
  type = Steady
[]

[Outputs]
  exodus = true
  csv = true
[]
