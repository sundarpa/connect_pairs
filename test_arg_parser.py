import unittest
from arg_parser import parse_argv
from tquery import *
from openpyxl import Workbook

class TestParseArgv(unittest.TestCase):

    def test_with_key_value(self):
        argv = ["--name", "Kushi", "--age", "25"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"name": "Kushi", "age": "25"})

    def test_without_value(self):
        argv = ["--h","--help"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"h": None, "help":None })

    def test_multiple_key_values(self):
        argv = ["--h", "help", "--help", "h"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"h": "help", "help": "h"})

    def test_invalid_argument(self):
        argv = ["help"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"Error: Invalid argument help {}"})

    def test_empty_keys(self):
        argv = ["--"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"": None})

    def test_empty_input(self):
        argv = []
        opts = parse_argv(argv)
        self.assertEqual(opts, {})

    def test_valid_csv(self):
        csv_filename = "INPUT.csv"
        df, filename = fetch_data_from_csv(csv_filename)
        self.assertIsNotNone(df)
        self.assertEqual(filename, csv_filename)

    def test_nonexistent_csv(self):
        csv_filename = "nonexistent_data.csv"
        df, filename = fetch_data_from_csv(csv_filename)
        self.assertIsNone(df)
        self.assertIsNone(filename)

    def test_empty_csv(self):
        csv_filename = "empty_data.csv"
        df, filename = fetch_data_from_csv(csv_filename)
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 0)
        self.assertEqual(filename, csv_filename)

    def test_invalid_csv(self):
        csv_filename = "invalid_data.csv"
        df, filename = fetch_data_from_csv(csv_filename)
        self.assertIsNone(df)
        self.assertIsNone(filename)

    def test_valid_module(self):
        module_name = "connect_pairs"
        imported_module = import_module(module_name)
        self.assertIsNotNone(imported_module)
        self.assertTrue(hasattr(imported_module, 'main'))  # Check if the module has a specific function

    def test_invalid_module(self):
        module_name = "nonexistent_module"
        imported_module = import_module(module_name)
        self.assertIsNone(imported_module)

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

if __name__ == "__main__":
    unittest.main()