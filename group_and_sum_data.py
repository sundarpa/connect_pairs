import pandas as pd


def group_and_sum(df):
    # Create a dictionary to define the groups based on block names
    group_definitions = {
        'fruits': ['fru_apple', 'frui_orange'],
        'vegetables': ['veg_cucumber'],
        'nuts': ['nut_peanut']
    }

    # Create a new DataFrame to store the group definitions
    group_df = pd.DataFrame(group_definitions.items(), columns=['Group', 'Block Names'])

    # Initialize a dictionary to store the summed values and percentage columns
    group_sums = {group: {} for group in group_definitions}

    for group, block_names in group_definitions.items():
        group_data = df[df['block'].isin(block_names)]
        group_sums[group] = group_data.drop(columns='block').sum()
        group_sums[group]['P0%'] = (group_data['p0'] / group_data['P0pass'] * 100).mean()
        group_sums[group]['P1%'] = (group_data['p1'] / group_data['P1pass'] * 100).mean()
        group_sums[group]['P2%'] = (group_data['p2'] / group_data['P2pass'] * 100).mean()
        group_sums[group]['P3%'] = (group_data['p3'] / group_data['P3pass'] * 100).mean()

    # Concatenate the summed values and percentage columns into a new DataFrame
    grouped_df = pd.DataFrame(group_sums).T.reset_index()
    grouped_df = grouped_df.rename(columns={'index': 'Group'})

    return grouped_df, group_df


# Sample input DataFrame
data = {
    'block': ['fru_apple', 'frui_orange', 'veg_cucumber', 'nut_peanut', 'frui_orange'],
    'planned': [10, 15, 5, 20, 10],
    'available': [8, 12, 4, 18, 8],
    'p0': [2, 3, 1, 4, 2],
    'p1': [1, 2, 1, 3, 1],
    'p2': [3, 4, 1, 5, 3],
    'p3': [2, 3, 1, 4, 2],
    'p4': [2, 3, 1, 4, 2],
    'P0pass': [5, 6, 2, 7, 5],
    'P1pass': [4, 5, 2, 6, 4],
    'P2pass': [6, 7, 3, 8, 6],
    'P3pass': [5, 6, 3, 7, 5]
}

df = pd.DataFrame(data)

grouped_df, group_df = group_and_sum(df)

print("Grouped Data:")
print(grouped_df)

print("\nGroup Definitions:")
print(group_df)
