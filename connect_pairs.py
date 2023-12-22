import pandas as pd

def main(input_csv_file, mapping_csv_file):
    # Read input vectors and mapping data into DataFrames
    input_df = pd.read_csv(input_csv_file, sep='_')
    mapping_df = pd.read_csv(mapping_csv_file)

    # Filter rows in input_df containing 'INI' in col3
    init_df = input_df[input_df['col3'] == 'INI']

    # Filter rows in input_df containing 'body' in col3
    body_df = input_df[input_df['col3'] != 'INI']

    # Join init_df with mapping_df on specified conditions
    init_mapped_df = pd.merge(init_df, mapping_df, left_on=['col4', 'col5'], right_on=['ini_core1', 'ini_core2'])
    print("init_mapped_df:")
    print(init_mapped_df)

    # Combine init_mapped_df and body_df column-wise into a single DataFrame named "init_body"
    init_body = pd.merge(init_mapped_df, body_df, left_on=['body_core1', 'body_core2'], right_on=['col4', 'col5'])
    print("init_body:")
    print(init_body)

main("input_vectors.csv","mapping.csv")