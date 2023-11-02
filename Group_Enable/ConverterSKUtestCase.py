#! /pkg/qct/software/python/sles12/3.9.4/bin/python3

import pandas as pd

import unittest
import pandas as pd
from ConverterSKU import convert_to_binary_and_int
 
class TestConvertToBinaryAndInt(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        data = {
            'col1': ['Y', 'N', 'Y', 'N', 'Y'],
            'col2': ['N', 'Y', 'Y', 'N', 'Y'],
            'col3': ['Y', 'Y', 'N', 'N', 'Y'],
        }
        self.df = pd.DataFrame(data)
 
    def test_convert_to_binary_and_int(self):
        # Define the headings to be converted
        headings = ['col1', 'col2', 'col3']
 
        # Call the function to be tested
        result_df = convert_to_binary_and_int(self.df, headings)
 
        # Define the expected result
        expected_data = {
            'qultivate_value_encoded': [5, 3, 6, 0, 7]
        }
        expected_df = pd.DataFrame(expected_data)
 
        # Compare the actual and expected DataFrames
        pd.testing.assert_frame_equal(result_df, expected_df)
 
if __name__ == '__main__':
    unittest.main()
    