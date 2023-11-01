from sys import argv
import pymysql
import importlib
import csv
import sys
import re
import glob
import os
import pandas as pd
from pandas import ExcelWriter
import glob
import argparse
import random
import string
from os.path import abspath, dirname
from arg_parser import parse_argv  # Import the parse_argv function from the external module
from query import openquery
import json
import time
import warnings
import subprocess
from Database import get_database_connection, decrypt

warnings.filterwarnings("ignore")

#to make the current dir where the script resides
current_wrk_dir = os.getcwd()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def convert_dataframe_to_json(dataframe):
    json_data = dataframe.to_json(orient='records')
    json_body = json.loads(json_data)
    json_formatted_str = json.dumps(json_body, indent=4)
    return json_formatted_str

# Define a function to dynamically import a module by name
def import_module(module_name):
    try:
        imported_module = importlib.import_module(module_name)
        print(f"Module '{module_name}' imported successfully.")
        return imported_module
    except ImportError:
        print(f"Failed to import module '{module_name}'.")
        return None

# Function to fetch data from a CSV file and return both the DataFrame and the CSV filename
def fetch_data_from_csv(csv_filename):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(csv_filename)
        return df, csv_filename
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return None, None

# Parse command-line arguments using the imported function
myargs, config_path, csv_module_name = parse_argv(sys.argv[1:])

if __name__ == '__main__':
	queriesResult = []
	finalSheetNames = []
	block = ""
	# json_data_dict = {}
	start_time = time.time()
	conn = get_database_connection(config_path)

	# Check for the 'csvfile' argument
	if 'csvfile' in myargs:
		csv_filenames = myargs['csvfile']  # Get the provided CSV filenames as a list
		csv_files = csv_filenames.split(':')  # Split the filenames by ':' into a list
		# Created a dictionary to store DataFrames with CSV filenames as keys
		data_dict = {}

		for csv_file in csv_files:
			data_from_csv, csv_name = fetch_data_from_csv(csv_file)
			if data_from_csv is not None:
				data_dict[csv_name] = data_from_csv  # Store the DataFrame with the CSV filename as the key
				print(f"Data from CSV file {csv_name}:")
				print(data_from_csv)
				# print(data_dict)

	#check if csv is in myargs
	if 'csv' in myargs:
		csv_module_name = myargs['csv']  # Get the provided CSV module name
		if csv_module_name:
			try:
				imported_module_csv = importlib.import_module(csv_module_name)
				print(f"Module '{csv_module_name}' imported successfully.")

				# Check if the imported module has a 'main' function
				if hasattr(imported_module_csv, "main") and callable(imported_module_csv.main):
					imported_module_csv.main("Input_vectors.csv", "mapping.csv")
				else:
					print(f"Module '{csv_module_name}' does not have a 'main' function.")
			except ImportError:
				print(f"Failed to import module '{csv_module_name}' for CSV data")

	try:
		block = myargs['block'] #Todo: low priority,  remove the block and apply this for other arguments
	except KeyError:
		block = None
	if block is not None:
		if "," in block:
			# Split the input string by comma and wrap each part in double quotes
			output_string = block.replace(",", "\",\"")
			myargs['block'] = output_string
	replacedData = openquery(myargs)
	if replacedData is None:
		pass
	else:
		if conn:
			print("connected successfully")
		else:
			print("Not Connected")
		splitString = replacedData.split(";")
		try:
			cursor = conn.cursor()
			success = True  # Flag for the success of all operations

			for cmdoneonly in splitString:
				cmdoneonly = cmdoneonly.replace('\n', ' ').replace('\n\n', '').lower().strip()

				if cmdoneonly.strip():
					if cmdoneonly.startswith(('update', 'delete', 'insert')):
						try:
							cursor.execute(cmdoneonly)
							conn.commit()  # Commit the transaction if the operation is successful
							print("Operation completed successfully")
						except Exception as e:
							conn.rollback()  # Rollback the transaction if an error occurs
							print(f"Operation failed: {str(e)}")
							success = False  # Set the success flag to False
					else:
						cursor.execute(cmdoneonly)
						results = cursor.fetchall()
						if results:
							df = pd.DataFrame(results, columns=[x[0] for x in cursor.description])
							queriesResult.append(df)
							# check if json is in myargs
							if 'json' in myargs:
								json_formatted_str = convert_dataframe_to_json(df)
								json_module_name = myargs.get('json_module', 'reg')  # Default to 'reg' if not specified

								# Dynamically import the module for JSON data
								imported_module_json = import_module(json_module_name)

								if imported_module_json:
									if hasattr(imported_module_json, "main") and callable(imported_module_json.main):
										result = imported_module_json.main(myargs, json_formatted_str)
									else:
										print(
											f"Module '{json_module_name}' for JSON data does not have a 'main' function.")
							else:
								sheetName = re.compile(r'^select\s+.+from\s+([a-z_]+)')
								for names in sheetName.finditer(cmdoneonly):
									finalSheetNames.append(names.group(1))
								folderName = myargs['query'][:-6]
								path = myargs.get('out_path',current_wrk_dir)
								if path == current_wrk_dir: #todo: lower priority, remove the project, rev, block
									project_folder = myargs['project']
									project_folder_path = os.path.join(path,project_folder)
									rev_folder = myargs['rev']
									rev_folder_path = os.path.join(project_folder_path,rev_folder)
									block_folder = myargs['block']
									block_folder_path = os.path.join(rev_folder_path,block_folder)
									path = os.path.join(block_folder_path, folderName)
								os.makedirs(path, exist_ok=True)
								for n,df in enumerate(queriesResult):
										#df.to_csv(path + '_dir' + '/' + f'{finalSheetNames[n]}' + '_' + f'{filename[n]}' + '.csv', index=False)
										df.to_csv(path + '/' + f'{finalSheetNames[n]}' + '.csv', index=False)
						else:
							print("The query result doesn't have any data to showcase")
			cursor.close()

			if success:
				print("All operations completed successfully")
			else:
				print("Some operations failed, transaction rolled back")
			#print("script execution completed")
		except pymysql.err.ProgrammingError as except_detail:
			print("pymysql.err.ProgrammingError: «{}»".format(except_detail))
		finally:
			conn.close()
			end_time = time.time()
			print("Script successfully completed in:", end_time - start_time, "seconds")