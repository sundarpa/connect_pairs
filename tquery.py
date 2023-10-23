#! /pkg/qct/software/python/sles12/3.9.4/bin/python3
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
import argparse
from os.path import abspath, dirname

current_wrk_dir = os.getcwd()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

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

		

if __name__ == '__main__':
	queriesResult = []
	finalSheetNames = []
	myargs = getopts(argv)
	block = ""
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
	

