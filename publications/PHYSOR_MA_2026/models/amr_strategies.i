!include ../../../../amr_strategies/value_jump_rel_error.i

R_ERROR_FRACTION := 0.2
R_STAT_ERROR := 0.05
[Adaptivity]
  [Indicators/error]
    variable := 'flux'
  []
  [Markers/rel_error]
    variable := 'flux_rel_error'
  []
[]

