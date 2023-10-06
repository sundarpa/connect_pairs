import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def main(myargs, json_data):
    milestone_details = pd.DataFrame()
    vector_pattern_details = pd.DataFrame()
    overall_data = pd.read_json(json_data, orient='records')
    column_names = list(overall_data.columns)
# do some process and print the output in csv/excel