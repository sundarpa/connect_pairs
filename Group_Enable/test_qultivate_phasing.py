import unittest
import subprocess
import os
import pandas as pd
import shutil
import re

class TestQultivatePhasingPullCommand(unittest.TestCase):

    def setUp(self):
        # Set up a common path variable
        self.common_path = "C:\\T_QUERY\\new_vidya\\Group_Enable"

    def test_basic_functionality_pull(self):
        # Test the basic functionality of the "pull" command
        phasing_csv_path = f"{self.common_path}/phasing.csv"
        sku_definition_csv_path = f"{self.common_path}/sku_definition.csv"

        if not os.path.exists(phasing_csv_path):
            # Create a dummy phasing.csv file
            with open(phasing_csv_path, 'w') as dummy_file:
                dummy_file.write("phasing_id,pattern_name,pattern_type,qultivate_enable,qultivate_value_encoded\n"
                                 "1.0,V_1,PROD,Y,9\n"
                                 "2.0,X_2,PROD,Y,3\n"
                                 "3.0,Y_3,PROD,N,0\n")

        if not os.path.exists(sku_definition_csv_path):
            # Create a dummy sku_definition.csv file
            with open(sku_definition_csv_path, 'w') as dummy_file:
                dummy_file.write("sku_mcn,sku_short_name,featuring\n"
                                 "QBIN_1,Modem,NO_MODEM\n"
                                 "QBIN_2,AI,NO_AI\n"
                                 "QBIN3,YZ,NO_AIE\n"
                                 "SKU_1,XY,\"NO_MODEM,NO_AI\"\n")

        command = f"python qultivate_phasing.py -out_path {self.common_path} -pull"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process completed successfully (exit code 0)
        self.assertEqual(result.returncode, 0)

        # Check if the data is not equal to zero
        self.assertNotEqual(len(result.stdout), 0)

        # Check if the output files were created
        output_path = f"{self.common_path}/qultivate_phasing.xlsx"
        self.assertTrue(os.path.exists(output_path))

        golden_output_path = f'{self.common_path}/golden_qultivate_phasing.xlsx'
        self.assertTrue(os.path.exists(golden_output_path))

        #Read data from output file and golden file
        generated_df = pd.read_excel(output_path)
        golden_df = pd.read_excel(golden_output_path)

        #check if dataframes are equal
        pd.testing.assert_frame_equal(generated_df, golden_df)
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
        sku_definition_csv_path = f"{self.common_path}/sku_definition.csv"
        if not os.path.exists(sku_definition_csv_path):
            # Create a dummy sku_definition.csv file
            with open(sku_definition_csv_path, 'w') as dummy_file:
                dummy_file.write("sku_mcn,sku_short_name,featuring\n"
                                 "QBIN_1,Modem,NO_MODEM\n"
                                 "QBIN_2,AI,NO_AI\n"
                                 "QBIN3,YZ,NO_AIE\n"
                                 "SKU_1,XY,\"NO_MODEM,NO_AI\"\n")

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
        sku_definition_csv_path = f"{self.common_path}/sku_definition.csv"
        if not os.path.exists(sku_definition_csv_path):
            # Create a dummy sku_definition.csv file
            with open(sku_definition_csv_path, 'w') as dummy_file:
                dummy_file.write("sku_mcn,sku_short_name,featuring\n"
                                 "QBIN_1,Modem,NO_MODEM\n"
                                 "QBIN_2,AI,NO_AI\n"
                                 "QBIN3,YZ,NO_AIE\n"
                                 "SKU_1,XY,\"NO_MODEM,NO_AI\"\n")
        # Run the remove_sku command
        remove_command = f"python your_script.py -out_path {self.common_path} -remove_sku -featuring NO_MODEM"
        result = subprocess.run(remove_command, capture_output=True, text=True, shell=True)

        # Extract the featuring value from the command
        args = remove_command.split()
        featuring_index = args.index('-featuring')
        featuring_value = args[featuring_index + 1]

        # Read the original CSV file
        df_original = pd.read_csv(sku_definition_csv_path)

        # Check if the featuring value is not present in the updated DataFrame
        df_updated = df_original[df_original['featuring'] != featuring_value]

        # Write the updated DataFrame to a new CSV file
        new_csv_path = f"{self.common_path}/sku_definition_updated.csv"
        df_updated.to_csv(new_csv_path, index=False)

        # Print the content of the 'featuring' column in the updated CSV
        print("Content of the 'featuring' column in updated CSV:")
        print(df_updated['featuring'].values)

        # Check if the featuring value is present in the original CSV file
        self.assertIn(featuring_value, df_original['featuring'].values,
                      f"{featuring_value} not present in the original CSV")

        # Assert that the featuring value is not present in the updated CSV file
        self.assertNotIn(featuring_value, df_updated['featuring'].values,
                         f"{featuring_value} still present in the updated CSV")

        # Assert that the featuring value is removed from qultivate_phasing.xlsx
        excel_file_path = f"{self.common_path}/qultivate_phasing.xlsx"
        if os.path.exists(excel_file_path):
            df_qultivate_phasing = pd.read_excel(excel_file_path, sheet_name='qultivate_phasing')
            self.assertNotIn(featuring_value, df_qultivate_phasing.columns,
                             f"{featuring_value} still present in qultivate_phasing.xlsx")

    def test_missing_out_path_remove_sku(self):
        # Test if an error is raised when out_path is missing
        command = "python qultivate_phasing.py -remove_sku"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process did not complete successfully (exit code not 0)
        self.assertNotEqual(result.returncode, 0)

        # Check if there is an error message in the output
        self.assertIn("Error", result.stderr)

if __name__ == '__main__':
    unittest.main()

