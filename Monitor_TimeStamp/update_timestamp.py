import pandas as pd
import psycopg2
from datetime import datetime

# Define a switch to select the data source (CSV or MySQL)
use_mysql = True  # Set to True to use MySQL, or False to use CSV

# Define dataframes to hold data
outermost_df = None
second_level_df = None
third_level_df = None
innermost_df = None

if use_mysql:
    # Database connection parameters
    db_params = {
        'host': 'your_mysql_host',
        'database': 'your_mysql_database',
        'user': 'your_mysql_user',
        'password': 'your_mysql_password'
    }

    # Establish a connection to the MySQL database
    conn = psycopg2.connect(**db_params)

    # Create a cursor
    cur = conn.cursor()

    # Define your SQL queries to fetch data from each table

    # Fetch data from the outermost table
    outermost_query = "SELECT * FROM outermost_table"
    cur.execute(outermost_query)
    outermost_data = cur.fetchall()

    # Fetch data from the second_level table
    second_level_query = "SELECT * FROM second_level_table"
    cur.execute(second_level_query)
    second_level_data = cur.fetchall()

    # Fetch data from the third_level table
    third_level_query = "SELECT * FROM third_level_table"
    cur.execute(third_level_query)
    third_level_data = cur.fetchall()

    # Fetch data from the innermost table
    innermost_query = "SELECT * FROM innermost_table"
    cur.execute(innermost_query)
    innermost_data = cur.fetchall()

    # Create pandas DataFrames from the fetched data
    outermost_df = pd.DataFrame(outermost_data, columns=['column1', 'column2', 'updated_timestamp'])
    second_level_df = pd.DataFrame(second_level_data, columns=['column1', 'column2', 'updated_timestamp'])
    third_level_df = pd.DataFrame(third_level_data, columns=['column1', 'column2', 'updated_timestamp'])
    innermost_df = pd.DataFrame(innermost_data, columns=['column1', 'column2', 'updated_timestamp'])

    # Close the cursor and connection
    cur.close()
    conn.close()
else:
    # Define file paths for CSV files
    outermost_path = 'outermost.csv'
    second_level_path = 'second_level.csv'
    third_level_path = 'third_level.csv'
    innermost_path = 'innermost.csv'

    # Read data from CSV files into dataframes
    outermost_df = pd.read_csv(outermost_path)
    second_level_df = pd.read_csv(second_level_path)
    third_level_df = pd.read_csv(third_level_path)
    innermost_df = pd.read_csv(innermost_path)

# Now, regardless of the data source, you can process the data using dataframes
# Process data using DataFrames (outermost_df, second_level_df, third_level_df, innermost_df)

# Get the last run timestamp from the outermost dataframe
last_run_timestamp = outermost_df['updated_timestamp'].max()

# Compare the last run timestamp with the current time
current_time = datetime.now()
print(f"Last Run Timestamp in Outermost: {last_run_timestamp}")
print(f"Current Time: {current_time}")

# Search for recently updated rows in each inner dataframe using joins
recently_updated_innermost = innermost_df.merge(
    third_level_df, left_on='third_level_id', right_on='id', how='left'
).merge(
    second_level_df, left_on='second_level_id', right_on='id', how='left'
)

recently_updated_innermost = recently_updated_innermost[
    (recently_updated_innermost['second_level_updated'] >= last_run_timestamp) |
    (recently_updated_innermost['updated_timestamp'] >= last_run_timestamp)
]

print("Recently Updated Rows in Innermost:")
print(recently_updated_innermost)
