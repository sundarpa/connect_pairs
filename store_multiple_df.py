import pandas as pd

# Sample DataFrames
data1 = {'A': [1, 2, 3], 'B': [4, 5, 6]}
data2 = {'C': [7, 8, 9], 'D': [10, 11, 12]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Combine DataFrames into a list
df_list = [df1, df2]

# Combine DataFrames into a dictionary
df_dict = {'DataFrame1': df1, 'DataFrame2': df2}

# Split DataFrames from a list
df1_split, df2_split = df_list[0], df_list[1]

# Split DataFrames from a dictionary
df1_split_from_dict = df_dict['DataFrame1']
df2_split_from_dict = df_dict['DataFrame2']

# Now you can work with df1_split, df2_split, df1_split_from_dict, df2_split_from_dict as individual DataFrames

print("Split DataFrames from a list:")
print(df1_split)
print(df2_split)

print("\nSplit DataFrames from a dictionary:")
print(df1_split_from_dict)
print(df2_split_from_dict)
