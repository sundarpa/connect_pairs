import pandas as pd
import unittest
import io
import datetime

# Sample data for innermost.csv
innermost_data = {
    'id': [1, 2, 3, 4, 5],
    'column1': ['innermost1', 'innermost2', 'innermost3', 'innermost4', 'innermost5'],
    'column2': [1, 2, 3, 4, 5],
    'updated_timestamp': [
        '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'
    ]
}

innermost_df = pd.DataFrame(innermost_data)

# Sample data for third_level.csv
third_level_data = {
    'id': [1, 2, 3, 4, 5],
    'innermost_id': [1, 2, 3, 4, 5],
    'column1': ['third1', 'third2', 'third3', 'third4', 'third5'],
    'column2': [1, 2, 3, 4, 5],
    'updated_timestamp': [
        '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'
    ]
}

third_level_df = pd.DataFrame(third_level_data)

# Sample data for second_level.csv
second_level_data = {
    'id': [1, 2, 3, 4, 5],
    'third_level_id': [1, 2, 3, 4, 5],
    'column1': ['second1', 'second2', 'second3', 'second4', 'second5'],
    'column2': [1, 2, 3, 4, 5],
    'updated_timestamp': [
        '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'
    ]
}

second_level_df = pd.DataFrame(second_level_data)

# Save the DataFrames as CSV files
innermost_df.to_csv('innermost.csv', index=False)
third_level_df.to_csv('third_level.csv', index=False)
second_level_df.to_csv('second_level.csv', index=False)

# Define your data processing function here (modify as needed)
def process_data(innermost_csv, third_level_csv, second_level_csv):
    last_run_timestamp = innermost_csv['updated_timestamp'].max()
    current_time = datetime.datetime(2023, 9, 15, 12, 0)

    return {
        "Last Run Timestamp in Outermost": last_run_timestamp,
        "Current Time": current_time,
    }

class TestDataProcessing(unittest.TestCase):
    def test_data_processing(self):
        # Load the CSV files as DataFrames
        innermost_df = pd.read_csv('innermost.csv')
        third_level_df = pd.read_csv('third_level.csv')
        second_level_df = pd.read_csv('second_level.csv')

        # Call your data processing function and obtain actual results
        actual_results = process_data(innermost_df, third_level_df, second_level_df)

        # Define expected results based on the test data
        expected_results = {
            "Last Run Timestamp in Outermost": '2023-01-05',
            "Current Time": datetime.datetime(2023, 9, 15, 12, 0),
        }

        # Compare actual results with expected results
        self.assertEqual(actual_results, expected_results)

if __name__ == '__main__':
    unittest.main()
