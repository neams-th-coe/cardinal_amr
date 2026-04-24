This directory holds all the necessary input and post-processing scripts to reprouce the results of this paper: 

Ebny Walid Ahammed et al., "Development of Mesh Tally Amalgamation Algorithm for Coupled High Fidelity Multiphysics Simulation", in Proceedings of PHYSOR 2026, Turin, Italy.


# setup:
Parts of mesh tally amalgamation algorithm source code are still in the review process. 
1. Clone cardinal from a [branch](https://github.com/magnoxemo/cardinal/tree/my_testing) 
2. Goto the cardinal dir and get dependencies by runing ``./scripts/get-dependencies.sh``
3. Change openmc submodule upstream to this branch [mesh_tally_amalgamation](https://github.com/magnoxemo/openmc/tree/mesh_tally_amalgamation), fetch it and check out that branch.

Rest fo the build process same as in the [cardinal](https://cardinal.cels.anl.gov/without_conda.html) website. Also, To save you the trouble, use this [Dockerfile](https://github.com/magnoxemo/custom_scripts/blob/main/cardinal_stuff/Dockerfile). 

# Actual simulation:
1. Generate the model.xml
2. `~/cardinal-opt -i openmc.i Adaptivity/Indicators/error/variable=flux Adaptivity/Markers/rel_error/variable=flux_rel_error`
3. (Optional) for postprocessing use the `post_processing/post_processing.py` or you can look at this
notebook [post_processing_notebook](https://github.com/magnoxemo/amr_test_cases_input_files/blob/main/PHYSOR26/notebook.ipynb)


