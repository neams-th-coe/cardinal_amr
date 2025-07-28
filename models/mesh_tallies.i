[Problem]
  [Tallies]
    [heat_source]
      type = MeshTally
      score = 'kappa_fission fission'
      name = 'heat_source fission'
      output = 'unrelaxed_tally_std_dev unrelaxed_tally_rel_error'
    []
    [flux]
      type = MeshTally
      score = 'flux'
      output = 'unrelaxed_tally_std_dev unrelaxed_tally_rel_error'
      filters = 'SH'
    []
  []

  [Filters/SH]
    type = SphericalHarmonicsFilter
    order = 1
  []
[]
