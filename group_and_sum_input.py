import pandas as pd

# Sample data
data = {
    'block_name': ['fru_apple', 'frui_orange', 'veg_cucumber', 'nut_peanut', 'frui_orange'],
    'pattern_id': [1, 2, 1, 2, 1],
    'p0': [2, 3, 1, 4, 2],
    'p1': [1, 2, 1, 3, 1],
    'p2': [3, 4, 1, 5, 3],
    'p3': [2, 3, 1, 4, 2],
    'p4': [2, 3, 1, 4, 2],
    'pat_type': ['Type1', 'Type2', 'Type1', 'Type2', 'Type1'],
    'P0pass': [5, 6, 2, 7, 5],
    'P1pass': [4, 5, 2, 6, 4],
    'P2pass': [6, 7, 3, 8, 6],
    'P3pass': [5, 6, 3, 7, 5]
}

# Create the DataFrame
df = pd.DataFrame(data)

# Calculate 'p0_p_count', 'p1_p_count', 'p2_p_count', and 'p3_p_count'
df['p0_p_count'] = df['p0'].apply(lambda x: str(x).count('p'))
df['p1_p_count'] = df['p1'].apply(lambda x: str(x).count('p'))
df['p2_p_count'] = df['p2'].apply(lambda x: str(x).count('p'))
df['p3_p_count'] = df['p3'].apply(lambda x: str(x).count('p'))

# Group by 'block_name' and 'pat_type', and count 'p' values in p0, p1, p2, and p3 columns
summary = df.groupby(['block_name', 'pat_type'])[['p0_p_count', 'p1_p_count', 'p2_p_count', 'p3_p_count']].sum().reset_index()

# Calculate 'patC0' and 'patC2' using 'pat_type' as 'Type1' or 'Type2'
summary['patC0'] = summary['pat_type'].map({'Type1': 1, 'Type2': 1})
summary['patC2'] = summary['pat_type'].map({'Type1': 1, 'Type2': 0})

# Fill NaN values with 0
summary.fillna(0, inplace=True)

# Display the summary
print("\nSummary:")
print(summary)
