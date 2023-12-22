#! /pkg/qct/software/python/sles12/3.9.4/bin/python3
import pandas as pd

# Replace these with your input and output file paths
input_excel_file = "/prj/vlsi/pete/ptetools/prod/tss/runcommands/supportFiles/sundarav/qultivate_phasing.xlsx"
output_csv_file = "/prj/vlsi/pete/ptetools/prod/tss/runcommands/supportFiles/sundarav/qultivate_phasing.csv"

# Read the Excel file
excel_data = pd.read_excel(input_excel_file)

# Save the data as a CSV file
excel_data.to_csv(output_csv_file, index=False)

print(f"Excel file '{input_excel_file}' converted to CSV file '{output_csv_file}'.")
	
