#! /pkg/qct/software/python/sles12/3.9.4/bin/python3

import pandas as pd

def convert_to_binary_and_fill_columns(df, headings):
    # Replace empty values in the first column with 0
    df['qultivate_value_encoded'].fillna(0, inplace=True)

    # Convert the first column to binary
    binary_column = df['qultivate_value_encoded'].apply(lambda x: np.base_repr(int(x), base=3).zfill(len(headings)))

    print("binary column:\n",binary_column)

    # Split the binary value into separate columns
    binary_split = binary_column.apply(lambda x: [int(bit) for bit in x])
    print("binary_split")

    # Replace binary values with 'N' and 'Y'
    binary_split_replaced = binary_split.apply(lambda bits: ['-' if bit == 0 else 'Y' if bit == 1 else 'N' for bit in bits])

    # Adjust binary values if they exceed the available columns
    for i in range(len(binary_split_replaced)):
        binary_value = binary_split_replaced[i]
        if len(binary_value) > len(headings):
            binary_split_replaced[i] = binary_value[-len(headings):]

    # Create a new DataFrame with the binary values
    new_df = pd.DataFrame(binary_split_replaced.tolist(), columns=headings)

    # Insert the new DataFrame after the 'qultivate_value_encoded' column
    idx = df.columns.get_loc('qultivate_value_encoded')
    final_df = pd.concat([df.iloc[:, :idx + 1], new_df, df.iloc[:, idx + 1:]], axis=1)
    print("final df:\n",final_df)
    # Drop the 'qultivate_value_encoded' column before concatenation
    df_without_data = final_df.drop(columns=['qultivate_value_encoded'])

    print ("convertbin",df_without_data)
    return df_without_data

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

def update_enable_column(selected_data):
    enable_value = ''

    for column in selected_data.columns[1:]: 
#        print(selected_data[column]) # Exclude the 'Enable' column
        if selected_data[column].eq('Y').any():
            enable_value = 'Y'
            break
        elif selected_data[column].eq('N').any():
            enable_value = 'N'
        else:
            enable_value = '-'
	    # Update 'Enable' column
    selected_data['qultivate_enable'] = enable_value
    #print('final update enable column is:\n',selected_data)
    return selected_data

#update the sku_mcn columns based on the conditions
def update_sku_columns(selected_data,sku_df):
    for column in sku_df.columns[0:]:  # Exclude the 'Enable' column
        if any(selected_data[selected_data['sku_mcn'].str.startswith('C')]):
            condition = sku_df[sku_df['sku_mcn'] == column]['featuring'].values[0]
            #print('the condition is:\n',condition)
            condition_columns = featuring.split(':')

            if any(selected_data[condition_columns] == 'Y'):
                selected_data[column] = 'Y'
            elif any(selected_data[condition_columns] == 'N'):
                selected_data[column] = 'N'
            else:
                selected_data[column] = '-'

    return selected_data