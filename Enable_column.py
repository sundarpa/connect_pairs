import pandas as pd

# Define the paths to the CSV files
conditions_csv_file = r"C:\Users\Dell\Downloads\Conditions.csv"
input_csv_file = r"C:\Users\Dell\Downloads\INPUT.csv"

# Load the conditions and input CSV data into DataFrames
conditions_df = pd.read_csv(conditions_csv_file, delimiter=',')
input_df = pd.read_csv(input_csv_file, delimiter=',')

# Define a function to update 'Enable' column based on conditions
def update_enable_column(row):
    enable_value = ''

    for index, condition in conditions_df.iterrows():
        condition_columns = condition['condition'].split(':')

        # Check if any column in the condition is 'Y'
        if any(row[column] == 'Y' for column in condition_columns):
            enable_value = 'Y'
            break

        if any(row[column] == 'N' for column in condition_columns):
            enable_value = 'N'
        else:
            enable_value = 'NIL'

    # Update 'Enable' column
    row['Enable'] = enable_value

    return row

# Apply the 'Enable' function to the input DataFrame
input_df = input_df.apply(update_enable_column, axis=1)

# Define a function to update 'S1', 'S2', 'S3', 'S4' columns based on the conditions
def update_s_columns(row):
    for column in input_df.columns[1:]:  # Exclude the 'Enable' column
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
input_df.to_csv(input_csv_file, index=False, sep=',', mode='w')

# Print the updated DataFrame
print(input_df)
