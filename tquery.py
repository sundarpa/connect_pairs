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

current_wrk_dir = os.getcwd()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def getopts(argv):
    opts = {}

    # Check if the first argument is a file path starting with '/'
    if argv and argv[0][0] == '/':
        opts[argv[0][2:]] = argv[1]
        argv = argv[1:]

    while argv:
        if argv[0].startswith("--") or argv[0].startswith("-"):
            option = argv[0][2:]
            if len(argv) > 1 and not argv[1].startswith("--") and not argv[1].startswith("-"):
                opts[option] = argv[1]  # Assign the value if available
                argv = argv[2:]
            else:
                opts[option] = None  # Assign None if no value is provided
                argv = argv[1:]
        else:
            print("Error: Invalid argument", argv[0])
            return opts

    return opts

CONFIG_PATH = "./config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

conn = pymysql.connect(host="localhost", port=3306, user= "root", passwd="QWE#44#rtyuio", db="searchtool")

conn.autocommit(True)

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

if __name__ == '__main__':
	queriesResult = []
	finalSheetNames = []
	#myargs = getopts(sys.argv)
	block = ""
	import sys

	myargs = getopts(sys.argv[1:])
	# print(myargs)
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
									#df.to_csv(path + '_dir' + '/' + f'{finalSheetNames[n]}' + '_' + f'{filename[n]}' + '.csv', index=False)
									df.to_csv(path + '/' + f'{finalSheetNames[n]}' + '.csv', index=False)

						else:
							print("The query result doesn't have any data to showcase")	
						
			cursor.close()

			if success:
				print("All operations completed successfully")
			else:
				print("Some operations failed, transaction rolled back")
			#print("scrip execution completed")
		except pymysql.err.ProgrammingError as except_detail:
			print("pymysql.err.ProgrammingError: «{}»".format(except_detail))
		finally:
			conn.close()