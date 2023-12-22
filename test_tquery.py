from tquery import *
import unittest
import os
import pandas as pd
import json

class TestTQuery(unittest.TestCase):

    def setUp(self):
        # Set up any preconditions for the tests, e.g., create temporary files or directories
        self.temp_csv_file = 'test_data.csv'

    def tearDown(self):
        # Clean up any resources created during the tests
        if os.path.exists(self.temp_csv_file):
            os.remove(self.temp_csv_file)

    def test_fetch_data_from_csv(self):
        # Create a sample CSV file for testing
        csv_data = "col1,col2\n1,2\n3,4"
        with open(self.temp_csv_file, 'w') as file:
            file.write(csv_data)

        # Test the fetch_data_from_csv function
        df, _ = fetch_data_from_csv(self.temp_csv_file)

        # Check if the DataFrame has the expected values
        expected_df = pd.DataFrame({'col1': [1, 3], 'col2': [2, 4]})
        pd.testing.assert_frame_equal(df, expected_df)


    def test_convert_dataframe_to_json(self):
        # Create a sample DataFrame for testing
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        # Test the convert_dataframe_to_json function
        json_str = convert_dataframe_to_json(df)

        # Check if the JSON string has the expected values
        expected_json_str = '[{"col1": 1, "col2": 3}, {"col1": 2, "col2": 4}]'
        self.assertEqual(json.loads(json_str), json.loads(expected_json_str))

    def test_valid_excel_file(self):
        excel_filename = "Data.xlsx"
        data_dict = fetch_data_from_excel(excel_filename)
        # Verify that data_dict contains two DataFrames for each sheet
        self.assertIn("Things", data_dict)
        self.assertIn("Data", data_dict)
        self.assertIsInstance(data_dict["Things"], pd.DataFrame)
        self.assertIsInstance(data_dict["Data"], pd.DataFrame)


    def test_nonexistent_excel_file(self):
        excel_filename = "nonexistent_data.xlsx"

        # Try to fetch data from the non-existent file
        data_dict = fetch_data_from_excel(excel_filename)
        self.assertIsNone(data_dict)

    def test_invalid_csv_file(self):
        result = fetch_data_from_csv("invalid_data.txt")
        self.assertIsNone(result)

    def test_nonexistent_csv_file(self):
        result = fetch_data_from_csv("nonexistent_data.csv")
        self.assertIsNone(result)

    def test_exception_case(self):
        with self.assertRaises(Exception):  # Replace Exception with the specific exception type you expect
            df, filename = fetch_data_from_csv(12345)
            self.assertIsNone(df)
            self.assertIsNone(filename)

    def test_valid_module(self):
        module_name = "connect_pairs"
        imported_module = import_module(module_name)
        self.assertIsNotNone(imported_module)
        if imported_module:
            self.assertTrue(hasattr(imported_module, 'main'))  # Check if the module has a specific function

    def test_invalid_module(self):
        module_name = "nonexistent_module"
        imported_module = import_module(module_name)
        self.assertIsNone(imported_module)

if __name__ == '__main__':
    unittest.main()

