import pandas as pd

import pandas as pd

def convert_to_binary_and_int(df, headings):
    # Convert 'Y' and 'N' to binary values for columns from 'Sheet2'
    for col in headings:
        df[col] = df[col].apply(lambda x: 1 if x == 'Y' else 2 if x == 'N' else 0)

    # Convert binary columns back to integer 'qultivate_value_encoded' column
    df['qultivate_value_encoded'] = df[headings].apply(lambda row: int(''.join(map(str, row)), 3), axis=1)

    # Find the index of the first heading from 'Sheet2'
    first_heading_index = df.columns.get_loc(headings[0])

    # Insert 'qultivate_value_encoded' column before the first heading from 'Sheet2'
    df.insert(first_heading_index, 'qultivate_value_encoded', df.pop('qultivate_value_encoded'))

    # Drop the heading columns taken from Sheet2
    df.drop(columns=headings, inplace=True)

    return df

def delete_and_recalculate_from_excel(file_path, columns_to_delete, headings):
    # Read DataFrame from Excel file
    df = pd.read_excel(file_path)

    # Display DataFrame before deletion
    print("Before deleting")
    print(df)

    # Drop the specified columns
    df.drop(columns=columns_to_delete, inplace=True)

    # Display DataFrame after deletion
    print("After deleting")
    print(df)

    # Use the existing function to convert binary columns to integer
    df = convert_to_binary_and_int(df, headings)

    # Display DataFrame after conversion
    print("After converting to integer")
    print(df)

    # Save the updated DataFrame back to the same Excel file
    df.to_excel(file_path, index=False)

    return df

# Example usage:
excel_file_path = r"C:\T_QUERY\new_vidya\Group_Enable\Testing.xlsx"
columns_to_delete = ['NO_MCU']
headings=['NO_MODEM','NO_MCU','NO_NAV','PARTIAL_GPU']

# Call the function to delete columns and recalculate 'value'
result_df = delete_and_recalculate_from_excel(excel_file_path, columns_to_delete,headings)
