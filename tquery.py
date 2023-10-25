#! /pkg/qct/software/python/sles12/3.9.4/bin/python3
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
import argparse
from os.path import abspath, dirname
<<<<<<< HEAD
=======
from arg_parser import parse_argv  # Import the parse_argv function from the external module
from query import openquery
from connect_pairs import main
import json
import time
import warnings
import subprocess

warnings.filterwarnings("ignore")
>>>>>>> remotes/origin/vidya

current_wrk_dir = os.getcwd()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

<<<<<<< HEAD
def getopts(argv):
	
	opts = {}
	if set(argv) == {'--h','/prj/vlsi/pete/ptetools/prod/utils/tssquery/1.9/tquery.py'}:
		argv.append('help')
		if argv[0][0] == '/':
			opts[argv[0][2:]] = argv[1]
		argv = argv[1:]
		return opts 
	elif set(argv) == {'--help','/prj/vlsi/pete/ptetools/prod/utils/tssquery/1.9/tquery.py'}:
		argv.append('h')
		if argv[0][0] == '/':
			opts[argv[0][2:]] = argv[1]
		argv = argv[1:]
		return opts
	elif set(argv) == {'--h','/prj/vlsi/pete/ptetools/prod/utils/tssquery/1.9/tquery.py'}:
		argv.append('help')
		if argv[0][0] == '/':
			opts[argv[0][2:]] = argv[1]
		argv = argv[1:]
		return opts
	elif set(argv) == {'--h','/prj/vlsi/pete/ptetools/prod/utils/tssquery/1.9/tquery.py'}:
		argv.append('help')
		if argv[0][0] == '/':
			opts[argv[0][2:]] = argv[1]
		argv = argv[1:]
		return opts
	elif set(argv) == {'--h','/prj/vlsi/pete/ptetools/prod/utils/tssquery/1.9/tquery.py'}:
		argv.append('help')
		if argv[0][0] == '/':
			opts[argv[0][2:]] = argv[1]
		argv = argv[1:]
		return opts
	else:
		while argv:
			if argv[0][0] == '-':
			    opts[argv[0][2:]] = argv[1]  # remove -- from arguments
			argv = argv[1:]
		return opts

CONFIG_PATH = "/prj/vlsi/pete/ptetools/prod/tss/TSS_DB_CONFIG/config.ini"
=======
def convert_dataframe_to_json(dataframe):
    json_data = dataframe.to_json(orient='records')
    json_body = json.loads(json_data)
    json_formatted_str = json.dumps(json_body, indent=4)
    return json_formatted_str
>>>>>>> remotes/origin/vidya

# Define a function to dynamically import a module by name
def import_module(module_name):
    try:
        imported_module = importlib.import_module(module_name)
        print(f"Module '{module_name}' imported successfully.")
        return imported_module
    except ImportError:
        print(f"Failed to import module '{module_name}'.")
        return None

# Function to decrypt an encrypted string
def decrypt(encrypted_str):
    try:
        decrypted_bytes = base64.b64decode(encrypted_str)
        decrypted_str = decrypted_bytes.decode('utf-8')
        return decrypted_str
    except Exception as e:
        print("Error decrypting:", str(e))
        return None

# Function to fetch data from a CSV file
def fetch_data_from_csv(csv_filename):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(csv_filename)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return None

# Parse command-line arguments using the imported function
myargs, config_path, csv_module_name = parse_argv(sys.argv[1:])

# Determine the configuration file path based on the command-line argument or use the default
if config_path:
    CONFIG_PATH = config_path
else:
    CONFIG_PATH = "./config.ini"

# Create a ConfigParser and read the configuration file
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

<<<<<<< HEAD
def decrypt(config_db):
    dec = []
    for j in config.sections():
        if re.match(j, config_db):
            enc = base64.urlsafe_b64decode(str(config.get(j,'encrypted_password')))
            for i in range(len(enc)):
                key_c = (config.get(j,'db'))[i % len((config.get(j,'db')))]
                dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
                dec.append(dec_c)
            decrypted_password = "".join(dec)

            user = config.get(j,'user')
            host = config.get(j,'host')
            port = config.get(j,'port')
            db = config.get(j,'db')
            stage_dict =  {
                    'host': str(host),
                    'port': int(port),
                    'password': decrypted_password,
                    'user': str(user),
                    'db': str(db)
                }
            return stage_dict

dbCheck = getopts(argv)

databaseList = []
with open(CONFIG_PATH, 'r') as fp:
	data = fp.read()
supportedDb = re.compile(r'\[(.*?)\]')

for match in supportedDb.finditer(data):
	databaseList.append(match.group(1))

if not "db" in dbCheck.keys():
	print("connecting to PROD db")
	stage_dict = decrypt('PROD')
elif dbCheck["db"].upper() in databaseList:
	print("connecting to" , dbCheck['db'], "db")
	stage_dict = decrypt(str(dbCheck['db'].upper()))
elif dbCheck["db"].upper() not in databaseList:
	print("connection failed")
	print("Please check the connection in config.ini")
	raise SystemExit

conn = pymysql.connect(host=stage_dict['host'], port=stage_dict['port'], user= stage_dict['user'], passwd=stage_dict['password'], db=stage_dict['db'])

conn.autocommit(True)

def openquery(myargs):
	matchList = []
	missingArguments = []
	requiredParameters = {}
	if len(myargs) == 1:	
		if 'h' in myargs.keys() or 'help' in myargs.keys(): 
			print("provide --query <queryName.query> from below supported list")
			dir_path = '/prj/vlsi/pete/ptetools/prod/utils/tssquery/1.9/*.query'
			for queries in glob.glob(dir_path, recursive=True):
    				print(queries)

	elif "query" in myargs.keys() and "help" in myargs.keys() and "h" not in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
	
		for match in regex.finditer(data):
			matchList.append(match.group(2))  # add all the required arguments to a list
	
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
		str = "tquery "
		if 'help' in myargs:
			for item in requiredParameters:
				str += "--" + item + ' ' + '<' + requiredParameters[item] + '>' + ' '
			print("#############################################################################################")		
			print(f"{str}" + "--query" + ' ' + myargs['query'])
			print("#############################################################################################")

	elif "query" in myargs.keys() and "h" not in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
	
		for match in regex.finditer(data):
			matchList.append(match.group(2))  # add all the required arguments to a list
#		print(matchList)
	
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
#		print(requiredParameters)
#		print(myargs.items())

		for key in requiredParameters.keys():
			if not key in myargs:
				missingArguments.append(key)
		if len(missingArguments) > 0:	
			print("missing arguments : ", missingArguments)
			raise SystemExit
			 
		for k, v in requiredParameters.items():
			if v in myargs.keys():
	    			print(f"{k} : {myargs[v]}")  # prints only arguments which are mentioned in query file

		for k, v in myargs.items():
			data = data.replace(f'"{k}"', f'"{v}"')
		return data	# returns replaced query

	elif "query" in myargs.keys() and "h" in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
	
		for match in regex.finditer(data):
			matchList.append(match.group(2))  # add all the required arguments to a list
	
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
		str = "tquery "
		if 'h' in myargs:
			for item in requiredParameters:
				str += "--" + item + ' ' + '<' + requiredParameters[item] + '>' + ' '
			print("###########################################################################################")		
			print(f"{str}" + "--query" + ' ' + myargs['query'])
			print("###########################################################################################")
			
	elif "query" in myargs.keys() and "help" in myargs.keys() and "h" not in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
	
		for match in regex.finditer(data):
			matchList.append(match.group(2))  # add all the required arguments to a list
	
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
		str = "tquery "
		if 'help' in myargs:
			for item in requiredParameters:
				str += "--" + item + ' ' + '<' + requiredParameters[item] + '>' + ' '
			print("#############################################################################################")		
			print(f"{str}" + "--query" + ' ' + myargs['query'])
			print("#############################################################################################")
		
	elif "query" in myargs.keys() and "h" not in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
	
		for match in regex.finditer(data):
			matchList.append(match.group(2))  # add all the required arguments to a list
#		print(matchList)
	
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
#		print(requiredParameters)
#		print(myargs.items())

		for key in requiredParameters.keys():
			if not key in myargs:
				missingArguments.append(key)
		if len(missingArguments) > 0:	
			print("missing arguments : ", missingArguments)
			raise SystemExit
			 
		for k, v in requiredParameters.items():
			if v in myargs.keys():
	    			print(f"{k} : {myargs[v]}")  # prints only arguments which are mentioned in query file

		for k, v in myargs.items():
			data = data.replace(f'"{k}"', f'"{v}"')
		return data	# returns replaced query
		
	elif "query" in myargs.keys() and "help" in myargs.keys() and "h" not in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
	
		for match in regex.finditer(data):
			matchList.append(match.group(2))  # add all the required arguments to a list
	
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
		str = "tquery "
		if 'help' in myargs:
			for item in requiredParameters:
				str += "--" + item + ' ' + '<' + requiredParameters[item] + '>' + ' '
			print("#############################################################################################")		
			print(f"{str}" + "--query" + ' ' + myargs['query'])
			print("#############################################################################################")
		
	elif "query" in myargs.keys() and "h" not in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
	
		for match in regex.finditer(data):
			matchList.append(match.group(2))  # add all the required arguments to a list
#		print(matchList)
	
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
#		print(requiredParameters)
#		print(myargs.items())

		for key in requiredParameters.keys():
			if not key in myargs:
				missingArguments.append(key)
		if len(missingArguments) > 0:	
			print("missing arguments : ", missingArguments)
			raise SystemExit
			 
		for k, v in requiredParameters.items():
			if v in myargs.keys():
	    			print(f"{k} : {myargs[v]}")  # prints only arguments which are mentioned in query file

		for k, v in myargs.items():
			data = data.replace(f'"{k}"', f'"{v}"')
		return data	# returns replaced query
		
		
	elif "query" in myargs.keys() and "help" in myargs.keys() and "h" not in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
=======
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
>>>>>>> remotes/origin/vidya

    conn = pymysql.connect(**db_credentials)
    conn.autocommit(True)
    print("Connected to the remote database.")

<<<<<<< HEAD
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
		str = "tquery "
		if 'help' in myargs:
			for item in requiredParameters:
				str += "--" + item + ' ' + '<' + requiredParameters[item] + '>' + ' '
			print("#############################################################################################")		
			print(f"{str}" + "--query" + ' ' + myargs['query'])
			print("#############################################################################################")
	
	elif "query" in myargs.keys() and "h" not in myargs.keys():
		with open(myargs['query'], 'r') as fp:
			data = fp.read()
		regex = re.compile(r'(["])((?:\\.|[^\\d])*?)(\1)')
	
		for match in regex.finditer(data):
			matchList.append(match.group(2))  # add all the required arguments to a list
#		print(matchList)
	
		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
#		print(requiredParameters)
#		print(myargs.items())

		for key in requiredParameters.keys():
			if not key in myargs:
				missingArguments.append(key)
		if len(missingArguments) > 0:	
			print("missing arguments : ", missingArguments)
			raise SystemExit
			 
		for k, v in requiredParameters.items():
			if v in myargs.keys():
	    			print(f"{k} : {myargs[v]}")  # prints only arguments which are mentioned in query file

		for k, v in myargs.items():
			data = data.replace(f'"{k}"', f'"{v}"')
		return data	# returns replaced query

		
=======
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
>>>>>>> remotes/origin/vidya

if __name__ == '__main__':
	queriesResult = []
	finalSheetNames = []
<<<<<<< HEAD
	myargs = getopts(argv)
	block = ""
=======
	block = ""
	# json_data_dict = {}
	start_time = time.time()

	# Check for the 'csvfile' argument
	if 'csvfile' in myargs:
		csv_filename = myargs['csvfile']  # Get the provided CSV filename
		if csv_filename:
			try:
				# Fetch data from the specified CSV file
				data_from_csv = fetch_data_from_csv(csv_filename)
				if data_from_csv is not None:
					print("Data from CSV file:")
					print(data_from_csv)
			except Exception as e:
				print(f"Error fetching data from CSV: {str(e)}")
	else:
		print("No 'csvfile' argument provided")

	#check if csv is in myargs
	if 'csv' in myargs:
		csv_module_name = myargs['csv']  # Get the provided CSV module name
		if csv_module_name:
			try:
				imported_module_csv = importlib.import_module(csv_module_name)
				print(f"Module '{csv_module_name}' imported successfully.")

				# Check if the imported module has a 'main' function
				if hasattr(imported_module_csv, "main") and callable(imported_module_csv.main):
					imported_module_csv.main("input_vectors.csv", "mapping.csv")
				else:
					print(f"Module '{csv_module_name}' does not have a 'main' function.")
			except ImportError:
				print(f"Failed to import module '{csv_module_name}' for CSV data")

>>>>>>> remotes/origin/vidya
	try:
		block = myargs['block']
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
			#filename = ''.join(random.choice(string.ascii_lowercase) for i in range(16)) 
			for cmdoneonly in splitString:
				cmdoneonly = cmdoneonly.replace('\n', ' ').replace('\n\n', '').strip()
				#print(cmdoneonly)
				if cmdoneonly.strip():
					if cmdoneonly.startswith(('UPDATE','DELETE','INSERT','SET')):
						cursor.execute(cmdoneonly)
						count = cursor.rowcount
						if count>0:
							print("Affected rows:",count)
						else:
							print("Nothing to update,please check the data:",count,"rows")
					else:
						cursor.execute(cmdoneonly)
						results = cursor.fetchall()
						if results :
							df = pd.DataFrame(results, columns=[x[0] for x in cursor.description])
							queriesResult.append(df)
<<<<<<< HEAD
							#print(queriesResult)
							
							sheetName = re.compile(r'^SELECT\s+.+FROM\s+([a-z_]+)')
							for names in sheetName.finditer(cmdoneonly):
								finalSheetNames.append(names.group(1))
							#print(finalSheetNames)
							folderName = myargs['query'][:-6]
							print(folderName)
							path = myargs.get('out_path',current_wrk_dir)
							if path == current_wrk_dir:
								project_folder = myargs['project']
								project_folder_path = os.path.join(path,project_folder)
								rev_folder = myargs['rev']
								rev_folder_path = os.path.join(project_folder_path,rev_folder)
								block_folder = myargs['block']
								block_folder_path = os.path.join(rev_folder_path,block_folder)
								path = os.path.join(block_folder_path, folderName)
							os.makedirs(path, exist_ok=True)
							for n,df in enumerate(queriesResult):
									#print(path)
=======
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
>>>>>>> remotes/origin/vidya

									#print(df.to_json(orient='records'))
									#df.to_csv(path + '_dir' + '/' + f'{finalSheetNames[n]}' + '_' + f'{filename[n]}' + '.csv', index=False)
									df.to_csv(path + '/' + f'{finalSheetNames[n]}' + '.csv', index=False)									
																								
									print("Output file downloaded:",path + '/' + f'{finalSheetNames[n]}' + '.csv')

						else:
							print("The query result doesn't have any data to showcase")	
						
			cursor.close()
			print("script execution completed")
		except pymysql.err.ProgrammingError as except_detail:
			print("pymysql.err.ProgrammingError: «{}»".format(except_detail))
		finally:
			conn.close()
<<<<<<< HEAD
	

=======
			end_time = time.time()
			print("Script successfully completed in:", end_time - start_time, "seconds")
>>>>>>> remotes/origin/vidya
