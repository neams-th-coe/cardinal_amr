import subprocess
import pandas as pd
from pathlib import Path

"""
A simple script that creates 
    1. the union mesh
    2. project the solution to that union mesh
    3. Export element vertex average data to csv files  
"""


class MeshAmalgamationPostProcessor:

    def __init__(self, ref_dir_path: str, test_dir_path: str, variable: str,
                 time_step, executable_path,
                 exodus_file_name="openmc_out.e"):
        """
        ref_dir_path: relative path of the ref dir solution
        test_dir_path: relative path of the test dir solution
        variables_to_export: list of the variables to export in csv files
        time_step: AMR/MA time_step we want to compare
        """

        self.ref_dir_path = Path.cwd() / ref_dir_path
        self.test_dir_path = Path.cwd() / test_dir_path
        self.variable = variable
        self.executable = executable_path
        self.union_mesh_script = "common_mesh.i"
        self.exodus_file_name = "openmc_out.e"

        if time_step != 1:
            exodus_file_name += f"-s{time_step: 03d}"

        self.ref_mesh = self.ref_dir_path / exodus_file_name
        self.test_mesh = self.test_dir_path / exodus_file_name

        self.ref_test_mesh_arguments = [
            f"test_mesh_file_name={self.test_mesh}",
            f"ref_mesh_file_name={self.ref_mesh}",
        ]

    def generate_union_mesh(self):

        print(f"comparing between {self.ref_mesh} and {self.test_mesh}")
        try:
            subprocess.run(
                [
                    self.executable,
                    "-i",
                    self.union_mesh_script,
                    *self.ref_test_mesh_arguments,
                    "--n-threads=28",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            print(
                " ========== Union mesh generation is completed successfully! =========="
            )
            self.set_updated_union_mesh()

        except subprocess.CalledProcessError as e:
            print("STDERR:", e.stderr)

    def set_updated_union_mesh(self):
        """
        now that the union mesh is generated I need to set it.
        """
        prefix = self.union_mesh_script[:-2] + "_out."
        self.union_mesh = (sorted(list(Path.cwd().glob(f"{prefix}*"))))[-1]

    def project_solution_to_union_mesh(self):

        try:
            final_command = [
                self.executable,
                "-i",
                "error_calculator.i",
                "--n-threads=28",
                *self.ref_test_mesh_arguments,
                f"union_mesh_file_name={self.union_mesh}",
                f"tally_variable={self.variable}",
                f"tally_rel_error_variable={self.variable}_rel_error",
            ]

            subprocess.run(
                final_command,
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as e:
            print("STDERR:", e.stderr)

    def read_latest_data_frame(self, time_step: None):
        """
        reads the dataframe with the latest time step. moose outputs the csv data
        as {input_file_name}_{ElementValueSampler_name}_out_{three_digit_time_step}.e
        In our case we are only interested about the 001 th time step.

        If time_step is not given by default it will open the latest time step.
        """
        csv_file_name_prefix = "error_calculator_out_csv_data_extractor_"
        if time_step is not None:
            csv_file_name = csv_file_name_prefix + f"{time_step: 03d}.e"
        else:
            csv_file_name = sorted(list(Path.cwd().glob(f"{csv_file_name_prefix}*")))[-1]
        abs_path = Path.cwd() / csv_file_name
        return pd.read_csv(abs_path)


if __name__ == "__main__":
    pass
