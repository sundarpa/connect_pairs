import unittest
import mysql.connector
import csv

class TestSQLQuery(unittest.TestCase):

    def setUp(self):
        # Connect to the offline MySQL database
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='QWE#44#rtyuio',
            database='tquery',
            port=3306
        )
        self.cursor = self.connection.cursor()

    def tearDown(self):
        # Close the database connection after the test
        self.cursor.close()
        self.connection.close()

    def read_query_from_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def read_csv_from_file(self, file_path):
        with open(file_path, 'r') as file:
            # Create a CSV reader
            reader = csv.reader(file)
            # Skip the header row
            next(reader, None)

            # Convert the remaining rows to tuples, converting numeric values to integers
            return [tuple(int(value) if value.isdigit() else value for value in row) for row in reader]

    def test_sql_query(self):
        # Read SQL query from .query file
        query_file_path = r'C:\T_QUERY\new_vidya\group_sum.query'
        sql_query = self.read_query_from_file(query_file_path)

        # Execute the SQL query
        self.cursor.execute(sql_query)
        actual_results = self.cursor.fetchall()
        print("Actual:", actual_results)

        # Read expected results from CSV file (skipping the header)
        csv_file_path = r'C:\T_QUERY\new_vidya\Results\group_sum.csv'
        expected_results = self.read_csv_from_file(csv_file_path)
        print("expected:", expected_results)

        # Compare the actual and expected results
        self.assertListEqual(actual_results, expected_results, "Data mismatch in the query results")


if __name__ == '__main__':
    unittest.main()