# Cardinal AMR

This repository houses a series of test cases for Adaptive Mesh Refinement (AMR) on unstructured mesh tallies in Cardinal-OpenMC.
The models can be found in `/models/*`; each consists of the following files:

- A script which uses the OpenMC Python API to generate a Constructive Solid Geometry (CSG) model for a particular reactor type (`make_openmc_model.py`).
- A Cardinal input file to generate the initial unstructured mesh for fission power / flux tallies (`mesh.i`).
- A Cardinal input file which creates an unstructured mesh tally using the initial mesh and runs OpenMC (`openmc.i`).

The Python files include a command line arguement (`-n`) to specify the number of fuel axial subdivisions in the CSG geometry. This can be used to investigate the impact of AMR on temperature/density feedback that is applied to the underlying OpenMC geometry.

At present this repository contains the following models:

- Light Water Reactor (`/models/lwr/*`)
  - Single PWR pincell;
  - 3 pin x 3 pin PWR bundle;
  - 17 pin x 17 pin unrodded / rodded UO2 PWR assemblies;
  - 4 assembly x 4 assembly unrodded / rodded UO2/MOX PWR lattices;

-  Sodium Cooled Fast Reactor (`/models/sfr/*`)
   - pincell model with two types of material composition ( inner and outer region of the reactor);
   - assembly model with two types of material composition ( inner and outer region of the reactor);

In addition to these models, this repository also contains a series of AMR algorithms - these can be found in `/amr_strategies/*`. To apply one of these AMR strategies to a test model in this repository, follow the steps below:

1. Add an `!include STRATEGY_NAME` to the beginning of the `openmc.i` file in one of the model sub directories, where `STRATEGY_NAME` is the name of a file in `amr_strategies`.
2. Run `python make_openmc_model.py`.
3. Run `cardinal-opt -i mesh.i --mesh-only`.
4. Run `mpiexec -n NUM_PROC cardinal-opt openmc.i --n-threads=NUM_THREADS`, replacing `NUM_PROC` with the number of MPI processors and `NUM_THREADS` with the number of OpenMP threads.

As an example, here we apply a relative error-aware refinement scheme to the LWR pincell case. First, we modify `models/lwr/pincell/openmc.i` to include the following on the first line:

```
!include ../../../amr_strategies/value_jump_rel_error.i
```
Then, we run the following:

```bash
cd ./models/lwr/pincell
python make_openmc_model.py
cardinal-opt -i mesh.i --mesh-only
mpiexec -n 2 cardinal-opt -i openmc.i --num-threads=2
```

Please note that some model/strategy combinations will require substantial computing power due to the size of the OpenMC model and the number of mesh tally bins.
