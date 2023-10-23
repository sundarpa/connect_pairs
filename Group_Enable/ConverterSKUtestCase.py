#! /pkg/qct/software/python/sles12/3.9.4/bin/python3

import pandas as pd


def convert_to_binary_and_fill_columns(df, headings):
	# Replace empty values in the first column with 0
	df['qultivate_value_encoded'].fillna(0, inplace=True)

	# Convert the first column to binary
	binary_column = df['qultivate_value_encoded'].apply(lambda x: bin(int(x))[2:].zfill(len(headings)))

	# Split the binary value into separate columns
	binary_split = binary_column.apply(lambda x: [int(bit) for bit in x])

	# Replace binary values with 'N' and 'Y'
	binary_split_replaced = binary_split.apply(lambda bits: ['N' if bit == 0 else 'Y' for bit in bits])

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

	# Drop the 'qultivate_value_encoded' column before concatenation
	df_without_data = final_df.drop(columns=['qultivate_value_encoded'])

	return df_without_data


def convert_to_binary_and_int(df, headings):
	# Convert 'Y' and 'N' to binary values for columns from 'Sheet2'
	for col in headings:
		df[col] = df[col].apply(lambda x: 1 if x == 'Y' else 0)

	# Convert binary columns back to integer 'qultivate_value_encoded' column
	df['qultivate_value_encoded'] = df[headings].apply(lambda row: int(''.join(map(str, row)), 2), axis=1)

	# Find the index of the first heading from 'Sheet2'
	first_heading_index = df.columns.get_loc(headings[0])

	# Insert 'qultivate_value_encoded' column before the first heading from 'Sheet2'
	df.insert(first_heading_index, 'qultivate_value_encoded', df.pop('qultivate_value_encoded'))

	# Drop the heading columns taken from Sheet2
	df.drop(columns=headings, inplace=True)

	return df

