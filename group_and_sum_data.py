import pandas as pd
import group_and_sum_input  # Import the group_input module

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
        group_data = df[df['block_name'].isin(block_names)]  # Use 'block_name' here
        group_sums[group] = group_data.drop(columns='block_name').sum()
        group_sums[group]['P0%'] = (group_data['p0'] / group_data['P0pass'] * 100).mean()
        group_sums[group]['P1%'] = (group_data['p1'] / group_data['P1pass'] * 100).mean()
        group_sums[group]['P2%'] = (group_data['p2'] / group_data['P2pass'] * 100).mean()
        group_sums[group]['P3%'] = (group_data['p3'] / group_data['P3pass'] * 100).mean()

    # Concatenate the summed values and percentage columns into a new DataFrame
    grouped_df = pd.DataFrame(group_sums).T.reset_index()
    grouped_df = grouped_df.rename(columns={'index': 'Group'})

    return grouped_df, group_df

# Use the DataFrame created in group_and_sum_input.py
input_data = group_and_sum_input.df

grouped_df, group_df = group_and_sum(input_data)

print("Grouped Data:")
print(grouped_df)

print("\nGroup Definitions:")
print(group_df)
