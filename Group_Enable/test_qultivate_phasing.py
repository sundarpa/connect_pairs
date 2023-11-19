import unittest
import subprocess
import os
import pandas as pd

class TestQultivatePhasingPullCommand(unittest.TestCase):

    def setUp(self):
        # Set up a common path variable
        self.common_path = "C:\\T_QUERY\\new_vidya\\Group_Enable"

    def test_basic_functionality_pull(self):
        # Test the basic functionality of the "pull" command
        command = f"python qultivate_phasing.py -out_path {self.common_path} -pull"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process completed successfully (exit code 0)
        self.assertEqual(result.returncode, 0)

        # Check if the data is not equal to zero
        self.assertNotEqual(len(result.stdout), 0)

        # Check if the output files were created
        self.assertTrue(os.path.exists(f"{self.common_path}//qultivate_phasing.xlsx"))

    def test_missing_out_path_pull(self):
        # Test if an error is raised when out_path is missing
        command = "python qultivate_phasing.py -pull"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process did not complete successfully (exit code not 0)
        self.assertNotEqual(result.returncode, 0)

        # Check if there is an error message in the output
        self.assertIn("Error", result.stderr)

    def test_basic_functionality_push(self):
        # Check whether qultivate_phasing.xlsx exists or not
        self.assertTrue(os.path.exists(f"{self.common_path}//qultivate_phasing.xlsx"))
        # Test the basic functionality of the "push" command
        command = f"python qultivate_phasing.py -pushfile {self.common_path} -push"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process completed successfully (exit code 0)
        self.assertEqual(result.returncode, 0)

        # Check if the data count is not equal to zero
        self.assertNotEqual(len(result.stdout), 0)

        # Check if the output files were created
        self.assertTrue(os.path.exists(f"{self.common_path}//phasing.csv"))

    def test_missing_pushfile_path(self):
        # Test if an error is raised when out_path is missing
        command = "python qultivate_phasing.py -push"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process did not complete successfully (exit code not 0)
        self.assertNotEqual(result.returncode, 0)

        # Check if there is an error message in the output
        self.assertIn("Error", result.stderr)

    def test_get_sku_data(self):
        # Test the "get_sku" command with a valid out_path
        command = f"python qultivate_phasing.py -out_path {self.common_path} -get_sku"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process completed successfully (exit code 0)
        self.assertEqual(result.returncode, 0)

        # Check if the data count is not equal to zero
        self.assertNotEqual(len(result.stdout), 0)

        # Check if there is an indication of success in the output
        self.assertTrue("successfully" in result.stdout.lower())

    def test_missing_out_path_get_sku(self):
        # Test if an error is raised when out_path is missing
        command = "python qultivate_phasing.py -get_sku"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process did not complete successfully (exit code not 0)
        self.assertNotEqual(result.returncode, 0)

        # Check if there is an error message in the output
        self.assertIn("Error", result.stderr)

    def test_remove_sku_command(self):
        # Run the remove_sku command
        remove_command = f"python qultivate_phasing.py -out_path {self.common_path} -remove_sku -featuring NO_AIE"
        result = subprocess.run(remove_command, capture_output=True, text=True, shell=True)

        # Check if the process completed successfully (exit code 0)
        self.assertEqual(result.returncode, 0)

        # Extract the featuring value from the command
        featuring_value = next((arg.split()[-1] for arg in remove_command.split() if arg.startswith('-featuring')), None)

        # Check if featuring is not present in the updated CSV file
        updated_sku_file = os.path.join(self.common_path, 'sku_definition_1.csv')
        df_updated = pd.read_csv(updated_sku_file)
        self.assertNotIn(featuring_value, df_updated['featuring'].values)

    def test_missing_out_path_remove_sku(self):
        # Test if an error is raised when out_path is missing
        command = "python qultivate_phasing.py -remove"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process did not complete successfully (exit code not 0)
        self.assertNotEqual(result.returncode, 0)

        # Check if there is an error message in the output
        self.assertIn("Error", result.stderr)

if __name__ == '__main__':
    unittest.main()

