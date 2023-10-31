#! /prj/vlsi/pete/ptetools/prod/utils/python_package/python3

import os
import pandas as pd
import argparse
from ConverterSKUtestCase import convert_to_binary_and_fill_columns, convert_to_binary_and_int
import configparser
import base64
import pymysql
import re
import time
import subprocess
from os.path import abspath, dirname
import shutil
from openpyxl import load_workbook,Workbook
from openpyxl.styles import Font
from tquery import fetch_data_from_csv

import shutil
import sys
current_wrk_dir = os.getcwd()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# path of our database configuration file
CONFIG_PATH = "/prj/vlsi/pete/ptetools/prod/tss/TSS_DB_CONFIG/config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# decryption of our datbase credentials from our configuration file
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

def merge_sku_definition ():
	# Read the first Excel file into a DataFrame
	df1 = pd.read_excel(block_folder_path + 'sku_definition.xlsx')
	get_sku_definition()

	# Read the second Excel file into another DataFrame
	df2 = pd.read_excel(block_folder_path +'sku_definitionbackup.xlsx')

	# Merge the two DataFrames on the headers (assuming headers are in the first row)
	merged_df = pd.merge(df1, df2, on=list(df1.columns), how='outer', indicator=True)

	# Filter out rows that are not unique (present in both DataFrames)
	unique_rows = merged_df[merged_df['_merge'] != 'both']

	# Print only the rows that are unique in either DataFrame
	filtered_unique_rows = unique_rows[list(df1.columns)]
	
	processed_data = filtered_unique_rows.apply(process_row, axis=1) 
	# Print the processed data
	for item in processed_data:
		if "Processed:" not in item: 
			#print("#####No new sku definition found to update.######") 
			continue
		original_string = item
		substring_to_remove = "Processed:"
		modified_string = original_string.replace(substring_to_remove, "")
		data_string = modified_string

		# Split the data string into a list of key-value pairs
		key_value_pairs = [pair.strip() for pair in data_string.split(',')]

		# Create an empty dictionary to store the extracted data
		extracted_data = {}

		# Extract the data into the dictionary
		for pair in key_value_pairs:
			key, value = pair.split(' - ')
			extracted_data[key] = value

		# Extract variables from the extracted_data dictionary
		sku_mcn = extracted_data['sku_mcn']
		sku_short_name = extracted_data['sku_short_name']
		featuring = extracted_data['featuring']

		# Print the extracted variables
		#print(sku_mcn)
		#print(sku_short_name)
		#print(featuring)
		connect_db(sku_mcn,sku_short_name,featuring)
	print("####################### Sku updated sucessfull ###################################")
# Define a function to process a row
def process_row(row):
	# Assuming the row contains columns 'Name', 'Age', 'Location' as headers
	sku_mcn = row['sku_mcn']
	sku_short_name = row['sku_short_name']
	featuring = row['featuring']

	# Your processing logic here
	processed_result = f"Processed: sku_mcn - {sku_mcn}, sku_short_name - {sku_short_name}, featuring - {featuring}"
	return processed_result
def remove_sku ():
	print("#######################################################################")
	print("Removing the Sku data from TSS started....")
	phasing_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--featuring', featuring, '--query', 'remove_sku.query', '--db', 'PROD']
	phasing_out = subprocess.run(phasing_command, capture_output=True, text=True)
	#print(phasing_out.stdout)
	#print(phasing_out.stdout)
	print("Removed the sku data from TSS successfully....")
	print("#######################################################################")
def push_sku_definition ():
	# Specify the sheet name you want to read
	sheet_name = 'sku_definition' # Replace with the actual sheet name

	# Read the Excel file with the specified sheet name
	excel_file_path = block_folder_path + 'qultivate_phasing.xlsx'
	df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

	# Get the first row as keys
	keys = df.columns.tolist()

	# Initialize a list to store student dictionaries
	data_list = []

	# Iterate through the rows (excluding the first row)
	for index, row in df.iterrows():
		data = row.tolist()
	# Create a dictionary entry with the keys as keys and the corresponding data as values
		student_dict = dict(zip(keys, data))
		data_list.append(student_dict)
	connect_db(data_list)
def get_sku_definition():
	print("#######################################################################")
	print("Fetching SKU Data from TSS started....")
	stage_dict = decrypt('PROD')
			# database connection setup
	conn = pymysql.connect(host=stage_dict['host'], port=stage_dict['port'], user= stage_dict['user'], passwd=stage_dict['password'], db=stage_dict['db'])
	conn.autocommit(True)
	cursor = conn.cursor()
	with conn.cursor() as cursor:
		query = ("SELECT sku_definition.sku_mcn,sku_definition.sku_short_name,sku_definition.featuring FROM sku_definition JOIN si_revision ON sku_definition.si_revision_fk = si_revision.si_revision_id JOIN project ON si_revision.project_fk = project.project_id  WHERE project.project_name =" +"'"+ project +"'"+" AND si_revision.si_revision_name ="+"'"+ si_rev + "'"+ "AND sku_definition.state != 'Deleted' ;")
		cursor.execute(query)
		#result = cursor.fetchall()
		# Fetch data using cursor
		data = cursor.fetchall()

		# Get column names from cursor description
		column_names = [column[0] for column in cursor.description]

		# Create a new Excel workbook for the main output file
		wb_main = Workbook()

		# Create a new Excel workbook for the backup file
		wb_backup = Workbook()

		# Select the active worksheets
		ws_main = wb_main.active
		ws_backup = wb_backup.active

		# Set the sheet names to match the filenames
		sheet_name = "sku_definition"
		ws_main.title = sheet_name
		ws_backup.title = sheet_name + "_backup"

		# Write column headings and apply formatting for main output
		for col_num, column_title in enumerate(column_names, 1):
			ws_main.cell(row=1, column=col_num, value=column_title)
			ws_main.cell(row=1, column=col_num).font = Font(bold=True)

		# Write data to main output
		for row_num, row_data in enumerate(data, 2):
			for col_num, cell_value in enumerate(row_data, 1):
				ws_main.cell(row=row_num, column=col_num, value=cell_value)

		# Copy the main output data to the backup sheet
		for row in ws_main.iter_rows(min_row=1, max_row=ws_main.max_row, min_col=1, max_col=ws_main.max_column):
			for cell in row:
				ws_backup[cell.coordinate].value = cell.value

		# Save both Excel files with matching sheet names
		wb_main.save(block_folder_path + sheet_name + ".xlsx")
		wb_backup.save(block_folder_path +sheet_name + "backup.xlsx")
def connect_db(sku_mcn,sku_short_name,featuring):
	text =  featuring # Example string with a tab character
	has_whitespace = any(char.isspace() for char in text)
	if has_whitespace:
		print("################## WARNING MESSAGE ##################")
		print("#### please remove the sapce and replace with _ ########")
		print("#### sku should be like No_Modam_w_nav #####")
		sys.exit()
	stage_dict = decrypt('PROD')
			# database connection setup
	conn = pymysql.connect(host=stage_dict['host'], port=stage_dict['port'], user= stage_dict['user'], passwd=stage_dict['password'], db=stage_dict['db'])
	conn.autocommit(True)
	cursor = conn.cursor()
	with conn.cursor() as cursor:
		query = ("SELECT si_revision.si_revision_id FROM si_revision JOIN project ON si_revision.project_fk = project.project_id WHERE project.project_name ="+"'"+ project + "'"+"AND si_revision.si_revision_name =" + "'"+si_rev +"'"+";")
		cursor.execute(query)
		result = cursor.fetchall()
		si_rev_id = ', '.join(item[0] for item in result)
		cursor.close()
	with conn.cursor() as cursor:
		query = "INSERT INTO sku_definition(si_revision_fk,sku_mcn,sku_short_name,featuring) VALUES (" + "'" + si_rev_id + "'," + "'"+ sku_mcn + "'," + "'" + sku_short_name + "'," + "'" + featuring + "'" + ")" + ";"
		cursor.execute(query)
		# Close the connection
		cursor.close()
		conn.close()
		#print ("connection closed")

def csv_to_excel(input_folder):
	csv_file = input_folder
	excel_file = block_folder_path + 'sku_definition.xlsx'
	df = pd.read_csv(csv_file)
	df.to_excel(excel_file, sheet_name= "sku_definition",index=False)
	# Import sheets from other Excel files
	source_excel = block_folder_path + 'sku_definition.xlsx'
	#print(source_excel)
	sheet_names_to_import = ['sku_definition'] # List of sheet names to import
	excel_file1 = block_folder_path + 'qultivate_phasing.xlsx'
	for sheet_name in sheet_names_to_import:
		source_df = pd.read_excel(source_excel, sheet_name)
	with pd.ExcelWriter(excel_file1, engine='openpyxl', mode='a') as writer:
		book = load_workbook(excel_file1)
		writer.book = book
		writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
		source_df.to_excel(writer, sheet_name=sheet_name, index=False)
	print("CSV converted to Excel and sheets imported successfully.")

def load_csv_to_excel(csv_file, excel_file):
	df = pd.read_csv(csv_file)
	sheet_name = os.path.splitext(os.path.basename(csv_file))[0]
	df.to_excel(excel_file, index=False, sheet_name=sheet_name)


def create_modified_file(excel_file):
	df_modidfied = pd.read_excel(excel_file, sheet_name=0)
	return df_modidfied


def compare_dataframes(df1, df2):
	merge_df = df1.merge(df2, indicator=True, how='outer')
	modified_rows = merge_df[merge_df['_merge'] == 'right_only'].drop(columns=['_merge'])
	return modified_rows


def expanding_columns():
	df_sheet1 = pd.read_excel(block_folder_path + '/' + 'qultivate_populates.xlsx', sheet_name='phasing')
	final_df_sheet1 = convert_to_binary_and_fill_columns(df_sheet1, column_headings)
	final_df_sheet1.to_excel(block_folder_path + '/' + 'qultivate_phasing.xlsx', sheet_name='qultivate_phasing', index=False)


def merging_columns(column_headings):
	# Perform reverse process to convert 'Y' and 'N' to binary and integers
	final_df_sheet1 = pd.read_excel(block_folder_path + '/' + 'qultivate_phasing.xlsx', sheet_name='qultivate_phasing')
	try:
		final_df_sheet1 = pd.read_excel(block_folder_path + '/' + 'qultivate_phasing.xlsx', sheet_name='qultivate_phasing')
	except Exception as e:
    		print("Error:", e)
	df_result = convert_to_binary_and_int(final_df_sheet1, column_headings)
	df_result.to_excel(block_folder_path + '/' + 'merged_data.xlsx', sheet_name='merged', index=False)
	

def getting_phasing_csv(folder_path):
	print("#######################################################################")
	print("Fetching phasing data from TSS started....")
	phasing_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--block', block_name, '--query', 'phasing_details_list.query', '--out_path', block_folder_path, '--db', 'PROD']
	phasing_out = subprocess.run(phasing_command, capture_output=True, text=True)
	#print(phasing_out.stdout)
	#print(phasing_out.stdout)
	print("Phasing data fetched from TSS successfully....")
	print("#######################################################################")
	csv_file = folder_path + '/' + 'phasing.csv'
	excel_file = block_folder_path + '/' + 'qultivate_populates.xlsx'
	column_names = ['phasing_id', 'qultivate_enable', 'qultivate_category', 'qultivate_value_encoded']
	read_input_phasing_csv = pd.read_csv(folder_path + '/' + 'phasing.csv')
	read_input_phasing_csv = read_input_phasing_csv[column_names]
	read_input_phasing_csv.to_csv(folder_path + '/' + 'phasing_backup.csv', index=False)
	return csv_file,excel_file


def populate_skn_data():
	print("#######################################################################")
	print("Fetching SKU Data from TSS started....")
	sku_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--query', 'sku_definition.query', '--out_path', block_folder_path, '--db', 'PROD']
	sku_out = subprocess.run(sku_command, capture_output=True, text=True)
	print(sku_out.stdout)
	print("SKU Data fetched from TSS successfully....")
	sku_out = subprocess.run(sku_command, capture_output=True, text=True)
	print(sku_out.stdout)
	load_csv_to_excel(block_folder_path + '/' + 'sku_definition.csv', block_folder_path + '/' + 'qultivate_populates.xlsx')
	df_sheet2 = pd.read_excel(block_folder_path + '/' + 'qultivate_populates.xlsx', sheet_name='sku_definition', header=None)
	column_headings = df_sheet2.iloc[1:, 2].tolist()
	return column_headings

def load_data_from_csv(csv_file):
    # Calling fetch_data_from_csv function from tquery.py
    data_from_csv = fetch_data_from_csv(csv_file)
    if data_from_csv is not None:
        print("Data from CSV file:")
        print(data_from_csv)
    else:
        print("Failed to load data from the CSV file.")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="load data from csv to excel and compare two dataframes.")
	parser.add_argument("-pull", action="store_true", help="load csv data to excel")
	parser.add_argument("-push", action="store_true", help="compare original vs modified dataframe")
	parser.add_argument("-getsku", action="store_true", help="get sku definition")
	parser.add_argument("-remove_sku", action="store_true", help="to remove sku")
	parser.add_argument("-update_sku", action="store_true", help="updatesku definition")
	parser.add_argument("-input_file")
	parser.add_argument('-project', required=False, help='project name')
	parser.add_argument('-rev', required=False, help='si revision name')
	parser.add_argument('-block', required=False, help='block name')
	parser.add_argument('-out_path', required=False, help='path to store the csvs')
	parser.add_argument('-featuring', required=False, help='remove sku')
	parser.add_argument('-pushfile', required=False, help='path to read the csvs')
	
	args = parser.parse_args()

	csv_file_path = "C:\T_QUERY\tquery_vidya\INPUT.csv"
	load_data_from_csv(csv_file_path)
	
	project = args.project
	si_rev = args.rev
	block_name = args.block
	featuring = args.featuring
	if args.out_path:
		out_path = args.out_path
	if args.pushfile:
		pushfile = args.pushfile
		
	 
	#project_folder_path = os.path.join(out_path,project) if args.out_path else os.path.join(pushfile,project)
	#rev_folder_path = os.path.join(project_folder_path,si_rev)
	#block_folder_path = os.path.join(rev_folder_path,block_name)
        #block_folder_path = out_path
	if args.out_path:
		block_folder_path = out_path
	elif args.pushfile:
		block_folder_path = pushfile
	#if not os.path.exists(block_folder_path):
		#os.makedirs(block_folder_path, exist_ok=False)	
	
	start_time = time.time()	

	if args.pull:
		csv_file,excel_file = getting_phasing_csv(block_folder_path)
		if os.path.exists(excel_file):
			os.remove(excel_file)
		original_df = pd.read_csv(csv_file)
		column_headings = populate_skn_data()
		load_csv_to_excel(csv_file, excel_file)
		expanding_columns()
		csv_to_excel(block_folder_path + "sku_definition.csv")
		print(f"Data loaded from {csv_file} to {excel_file} successfully.")

	if args.push:
		column_headings = populate_skn_data()
		merging_columns(column_headings)
		columns = ['phasing_id', 'qultivate_enable', 'qultivate_category', 'qultivate_value_encoded']
		modified_df = pd.read_excel(block_folder_path + '/' + 'merged_data.xlsx', usecols=columns)
		#print(modified_df)
		modified_df.to_csv(block_folder_path + '/' + 'merged_data.csv', index=False)
		original_dataframe = pd.read_csv(block_folder_path + '/' + 'phasing_backup.csv')
		#print(original_dataframe)
		modified_dataframe = pd.read_csv(block_folder_path + '/' + 'merged_data.csv')
		#print(modified_dataframe)
		#filtered_df = modified_dataframe[modified_dataframe.isin(original_dataframe.to_dict('list')).all(axis=1)]
		filtered_df = modified_df
		#print(filtered_df)
		update_statements = []
		for index, row in filtered_df.iterrows():
			values = []
			for col in filtered_df.columns:
				if col != 'phasing_id' and not pd.isna(row[col]):
					if col in ['qultivate_enable', 'qultivate_category']:
						values.append(f"phasing.{col} = '{row[col]}'")
					elif col == 'qultivate_value_encoded':
						values.append(f"phasing.{col} = {row[col]}")
			if values:
				sql = "UPDATE phasing SET {}".format(', '.join(values))
				sql += " WHERE phasing.phasing_id = '{}';".format(row['phasing_id'])
				update_statements.append(sql)
		try:
			stage_dict = decrypt('PROD')
			# database connection setup
			conn = pymysql.connect(host=stage_dict['host'], port=stage_dict['port'], user= stage_dict['user'], passwd=stage_dict['password'], db=stage_dict['db'])
			conn.autocommit(True)
			cursor = conn.cursor()
			for statement in update_statements:
				if statement:
					print(statement)
					cursor.execute(statement)
			cursor.close()
			print("Qultivate data successfully updated")
			latest_modified_dataframe = pd.read_excel(block_folder_path + '/' + 'merged_data.xlsx', usecols=columns)
			latest_modified_dataframe.to_csv(block_folder_path + '/' + 'phasing_backup.csv', index=False)
		except pymysql.err.ProgrammingError as except_detail:
			print("pymysql.err.ProgrammingError: «{}»".format(except_detail))
		finally:
			conn.close()
	end_time = time.time()
	if args.getsku:
		get_sku_definition()
	if args.update_sku:
		merge_sku_definition()
	if args.remove_sku:
		remove_sku ()
	print("Script successfully completed in:", end_time - start_time, "seconds")
#        modified_df.to_csv(csv_file, index=False, mode='w')

