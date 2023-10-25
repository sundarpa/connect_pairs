import pandas as pd

# Define the paths to the CSV files
conditions_csv_file = r"C:\Users\Dell\Downloads\Conditions.csv"
input_csv_file = r"C:\Users\Dell\Downloads\Input.csv"
output_csv_file = r"C:\Users\Dell\Downloads\Output.csv"

# Load the conditions and input CSV data into DataFrames
conditions_df = pd.read_csv(conditions_csv_file, delimiter=',')
input_df = pd.read_csv(input_csv_file, delimiter=',')

# Define a function to update 'Enable' column based on conditions
def update_enable_column(row):
    enable_value = None  # Initialize with None

    for column in row.index[1:]:
        if row[column] == 'Y':
            enable_value = 'Y'
            break
        elif row[column] == 'N':
            enable_value = 'N'

    if enable_value is None:
        enable_value = 'NIL'  # Set to 'NIL' if no 'Y' or 'N' is found

    # Update 'Enable' column
    row['Enable'] = enable_value
    return row

# Apply the 'Enable' function to the input DataFrame
input_df = input_df.apply(update_enable_column, axis=1)

# Define a function to update S columns based on the conditions
def update_s_columns(row):
    for column in input_df.columns[1:]: # Exclude the 'Enable' column
        if column.startswith('S'):
            condition = conditions_df[conditions_df['column'] == column]['condition'].values[0]
            condition_columns = condition.split(':')

            if any(row[condition_columns] == 'Y'):
                row[column] = 'Y'
            elif any(row[condition_columns] == 'N'):
                row[column] = 'N'
            else:
                row[column] = 'NIL'

    return row

# Apply the 'S' function to the input DataFrame
input_df = input_df.apply(update_s_columns, axis=1)

# Write the updated columns back to the original input CSV file
input_df.to_csv(output_csv_file, index=False, sep=',', mode='w')

# Print the updated DataFrame
print(input_df)
