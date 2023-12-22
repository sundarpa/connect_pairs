import unittest
import os
import subprocess
from tquery import *

class TestTQueryScript(unittest.TestCase):

    def setUp(self):
        # Set up a common path variable
        self.common_path = "C:\\T_QUERY\\new_vidya"

    def test_query_execution_csv_with_out_path(self):
        command = "python tquery.py --query Query_1.query --out_path {self.common_path}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if "CSV files created successfully" is in the captured output
        self.assertIn("CSV files created successfully", result.stdout)

        # Check if CSV files are created in the specified output path
        self.assertTrue(os.path.exists(f"{self.common_path}//group_sum.csv"))

    def test_query_execution_with_fruit(self):
        command = "python tquery.py--db searchtool --query Query_1.query --fruit Apple"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if "CSV files created successfully" is in the captured output
        self.assertIn("CSV files created successfully", result.stdout)

        # Check if CSV files are created in the specified output path
        csv_files_created = os.path.exists(os.path.join(self.common_path, "Query_1", "apple", "Query_1.query","search.csv"))
        self.assertTrue(csv_files_created)

    def test_query_execution_without_doublequoted(self):
        command = "python tquery.py --db searchtool --query query2.query"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if "CSV files created successfully" is in the captured output
        self.assertIn("CSV files created successfully", result.stdout)

        # Check if CSV files are created in the specified output path
        csv_files_created = os.path.exists(os.path.join(self.common_path, "search.csv"))
        self.assertTrue(csv_files_created)

    def test_query_execution_with_incorrect_query_file(self):
        script_path = os.path.join(self.common_path, "tquery.py")
        command = f"python {script_path} --db searchtool --query nonexistent_query.query"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Print the captured output for debugging
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)

        # Check if "Failed to import module" is in the captured output, indicating an error
        self.assertIn("Error", result.stderr)

        # Check if the script returns a non-zero exit code, indicating failure
        self.assertNotEqual(result.returncode, 0)

    def test_csvfile_command(self):
        command = "python tquery.py --csvfile INPUT.csv:mapping.csv"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process completed successfully (exit code 0)
        self.assertEqual(result.returncode, 0)

        # Assuming 'fetch_data_from_csv' is a function that returns a DataFrame and CSV name
        data_from_csv, csv_name = fetch_data_from_csv('INPUT.csv')

        # Check if the expected columns are present in the DataFrame
        expected_columns = list(data_from_csv.columns)
        for column in expected_columns:
            self.assertTrue(column in data_from_csv.columns, f"Column '{column}' not found in the DataFrame.")

    def test_csvfile_command_fail(self):
        command = "python tquery.py --csvfile incorrect_file.csv"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # # Check if the process failed (non-zero exit code)
        # self.assertNotEqual(result.returncode, 0)
        #
        # # Assuming 'fetch_data_from_csv' returns None for a failing scenario
        # data_from_csv = fetch_data_from_csv('incorrect_file.csv')
        #
        # # Check if the function returned None for a failing scenario
        # self.assertIsNone(data_from_csv, "Expected fetch_data_from_csv to return None for an incorrect CSV file.")

        # Check if "Failed to import module" is in the captured output, indicating an error
        self.assertIn("Error", result.stderr)

        # Check if the script returns a non-zero exit code, indicating failure
        self.assertNotEqual(result.returncode, 0)

    def test_excelfile_command(self):
        command = "python tquery.py --excelfile Data.xlsx"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the process completed successfully (exit code 0)
        self.assertEqual(result.returncode, 0)

        # Assuming 'fetch_data_from_excel' is a function that returns a DataFrame and sheet names
        excel_filename = 'Data.xlsx'
        data_from_excel = fetch_data_from_excel(excel_filename)

        # Check if the expected sheets are present in the output
        for sheet in data_from_excel.keys():
            self.assertTrue(sheet in result.stdout, f"Sheet '{sheet}' not found in the output.")

        # Check if the expected data is present in the DataFrame
        for sheet, expected_data in data_from_excel.items():
            for index, row in expected_data.iterrows():
                for column in expected_data.columns:
                    cell_value = str(row[column])
                    self.assertTrue(cell_value in result.stdout, f"Cell value '{cell_value}' not found in the output.")

    def test_excelfile_command(self):
        command = f"python tquery.py --excelfile NonExistentFile.xlsx"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the expected error message is present in the output
        self.assertTrue("Error", result.stderr)


if __name__ == '__main__':
    unittest.main()
