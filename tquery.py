from sys import argv
import importlib
import pymysql
import csv
import sys
import re
import glob
import os
import pandas as pd
from pandas import ExcelWriter
import configparser
import base64
import glob
import argparse
import random
import string
from os.path import abspath, dirname
from arg_parser import parse_argv  # Import the parse_argv function from the external module
from query import openquery
from connect_pairs import process_csv_files
import json
import time
import warnings

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

def process_csv_file(csv_file):
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
    except Exception as e:
        print(f"Error: {e}")

# Function to decrypt an encrypted string
def decrypt(encrypted_str):
    try:
        decrypted_bytes = base64.b64decode(encrypted_str)
        decrypted_str = decrypted_bytes.decode('utf-8')
        return decrypted_str
    except Exception as e:
        print("Error decrypting:", str(e))
        return None

# Parse command-line arguments using the imported function
myargs, config_path = parse_argv(sys.argv[1:])

# Determine the configuration file path based on the command-line argument or use the default
if config_path:
    CONFIG_PATH = config_path
else:
    CONFIG_PATH = "./config.ini"

# Create a ConfigParser and read the configuration file
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Get the remote database credentials from the config file
db_host = config['SEARCHTOOL']['host']
db_port = int(config['SEARCHTOOL']['port'])
db_user = config['SEARCHTOOL']['user']
db_db = config['SEARCHTOOL']['db']
encrypted_db_password = config['SEARCHTOOL']['encrypted_password']

# Decrypt the remote database password
db_password = decrypt(encrypted_db_password)

try:
    # Connect to the remote database
    db_credentials = {
        'host': db_host,
        'port': db_port,
        'user': db_user,
        'passwd': db_password,
        'db': db_db
    }

    conn = pymysql.connect(**db_credentials)
    conn.autocommit(True)
    print("Connected to the remote database.")

except pymysql.Error:
    print("Failed to connect to the remote database")

    # If the remote connection fails, connect to the local database
    # Get the local database credentials from the config file
    local_db_host = config['LOCALDB']['host']
    local_db_port = int(config['LOCALDB']['port'])
    local_db_user = config['LOCALDB']['user']
    local_db_db = config['LOCALDB']['db']
    encrypted_local_db_password = config['LOCALDB']['encrypted_password']

    # Decrypt the local database password
    local_db_password = decrypt(encrypted_local_db_password)

    local_db_credentials = {
        'host': local_db_host,
        'port': local_db_port,
        'user': local_db_user,
        'passwd': local_db_password,
        'db': local_db_db
    }

    try:
        conn = pymysql.connect(**local_db_credentials)
        conn.autocommit(True)
        print("Connected to the local database.")
    except pymysql.Error:
        print("Failed to connect to the local database.")

if __name__ == '__main__':
	queriesResult = []
	finalSheetNames = []
	block = ""
	# json_data_dict = {}
	start_time = time.time()

	if 'csv' in myargs:
		# Extract CSV data from myargs (assuming it's a dictionary)
		csv_data = myargs['csv']
		process_csv_file(csv_data)

		# Specify the module name for CSV handling (passed as a command-line argument)
		csv_module_name = myargs.get('csv_module', 'connect_pairs')  # Default to 'connect_pairs' if not specified

		# Dynamically import the module for CSV data
		imported_module_csv = import_module(csv_module_name)

		if imported_module_csv:
			if hasattr(imported_module_csv, "process_csv_files") and callable(imported_module_csv.process_csv_files):
				# Call the process_csv_data function with the CSV data string
				csv_result = imported_module_csv.process_csv_files(myargs, csv_data)
			else:
				print(f"Module '{csv_module_name}' for CSV data does not have a 'process_csv_data' function.")

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