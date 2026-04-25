This directory holds all the necessary input and post-processing scripts to reprouce the results of this paper: 

Ebny Walid Ahammed et al., "Development of Mesh Tally Amalgamation Algorithm for Coupled High Fidelity Multiphysics Simulation", in Proceedings of PHYSOR 2026, Turin, Italy.


# Setup:
Parts of the mesh tally amalgamation algorithm source code are still in the review process. 
1. Clone Cardinal from [this branch](https://github.com/magnoxemo/cardinal/tree/my_testing) 
2. Enter the new Cardinal directory and get dependencies by running `./scripts/get-dependencies.sh`
3. Change the OpenMC submodule upstream to the following remote [https://github.com/magnoxemo/openmc.git](https://github.com/magnoxemo/openmc.git). Then, check out the `mesh_tally_amalgamation` branch.

The remainder of the build process is the same as a normal Cardinal installation. Those instructions can be found [here](https://cardinal.cels.anl.gov/without_conda.html). Alternatively, you can use this [Dockerfile](https://github.com/magnoxemo/custom_scripts/blob/main/cardinal_stuff/Dockerfile). 

# Generating the results from the paper:
1. Generate the `model.xml` file by running `models/make_openmc_model.py`
2. Run `cardinal-opt -i openmc.i` (assuming there is a valid Cardinal executable on your path). If using the suggested Dockerfile, run `~/cardinal-opt -i openmc.i`
3. (Optional) For post-processing you can use `post_processing/post_processing.py` or [this Jupyter notebook](https://github.com/magnoxemo/amr_test_cases_input_files/blob/main/PHYSOR26/notebook.ipynb)


