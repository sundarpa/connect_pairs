import pandas as pd

def interchange_columns(df, col1, col2):
    # Print DataFrame before interchange
    print("DataFrame before interchange:")
    print(df)

    # Interchange columns
    df[col1], df[col2] = df[col2].copy(), df[col1].copy()

    # Rename columns
    df.rename(columns={col1: col2, col2: col1}, inplace=True)

    # Print DataFrame after interchange
    print("\nDataFrame after interchange:")
    print(df)

    # Save the updated DataFrame back to the same Excel file
    with pd.ExcelWriter('qultivate_phasing.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='qultivate_phasing', index=False)

    print("Updated DataFrame saved to qultivate_phasing.xlsx")

    # return df

# Load your DataFrame from the Excel file
phasing_df = pd.read_excel('qultivate_phasing.xlsx')

phasing_df = interchange_columns(phasing_df, 'NO_MODEM', 'NO_AIE')







