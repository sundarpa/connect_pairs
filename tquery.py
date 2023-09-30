from sys import argv
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
import random
import string
from os.path import abspath, dirname
from arg_parser import parse_argv  # Import the parse_argv function from the external module

#to make the current dir where the script resides
current_wrk_dir = os.getcwd()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Function to decrypt an encrypted string
def decrypt(encrypted_str):
    try:
        decrypted_bytes = base64.b64decode(encrypted_str)
        decrypted_str = decrypted_bytes.decode('utf-8')
        return decrypted_str
    except Exception as e:
        print("Error decrypting:", str(e))
        return None

# Path to the config file
CONFIG_PATH = "./config.ini"
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

#autocommit where there is a need to commit only once, say not in loop
# conn.autocommit(True)
def openquery(myargs):
	matchList = []
	missingArguments = []
	requiredParameters = {}
	if len(myargs) == 1:
		if 'h' in myargs.keys() or 'help' in myargs.keys():
			print("provide --query <queryName.query> from below supported list")
			dir_path = '/released_path/*.query'
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
		print(matchList)

		for param in range(len(matchList)):
			requiredParameters[matchList[param]] = matchList[param]  # converts to required dictionary
		print(requiredParameters)
		print(myargs.items())

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
		return data  # returns replaced query

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

if __name__ == '__main__':
	queriesResult = []
	finalSheetNames = []
	#myargs = getopts(sys.argv)
	block = ""

	# Parse command-line arguments using the imported function
	myargs = parse_argv(sys.argv[1:])
	# print(myargs)
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