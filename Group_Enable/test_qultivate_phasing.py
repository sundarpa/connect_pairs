import unittest
import subprocess
import os

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

        # Check if the expected success message is present in the output
        expected_message = f"Data loaded from {self.common_path}//phasing.csv to {self.common_path}//qultivate_populates.xlsx successfully."
        self.assertIn(expected_message, result.stdout)

        # Check if the output files were created
        self.assertTrue(os.path.exists(f"{self.common_path}//phasing.csv"))
        self.assertTrue(os.path.exists(f"{self.common_path}//qultivate_populates.xlsx"))
        self.assertTrue(os.path.exists(f"{self.common_path}//qultivate_phasing.xlsx"))

    def test_basic_functionality_push(self):
        # Check whether qultivate_phasing.xlsx exists or not
        self.assertTrue(os.path.exists(f"{self.common_path}//qultivate_phasing.xlsx"))
        # Test the basic functionality of the "push" command
        command = f"python qultivate_phasing.py -pushfile {self.common_path} -push"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process completed successfully (exit code 0)
        self.assertEqual(result.returncode, 0)

        # Check if the expected success message is present in the output
        expected_message = "Qultivate data successfully updated"
        self.assertIn(expected_message, result.stdout)

        # Check if the output files were created
        self.assertTrue(os.path.exists(f"{self.common_path}//phasing.csv"))

if __name__ == '__main__':
    unittest.main()

