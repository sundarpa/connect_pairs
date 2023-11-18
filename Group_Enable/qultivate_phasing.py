#! /prj/vlsi/pete/ptetools/prod/utils/python_package/python3

import os
import pandas as pd
import argparse
from ConverterSKUtest import convert_to_binary_and_fill_columns, convert_to_binary_and_int, qultivate_sku_fill_values, coloring_y_values, fill_qultivate_enable_values, load_csv_to_excel
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

def get_sku_definition():
	print("#######################################################################")
	print("Fetching SKU Data from TSS started....")
	sku_command = ['C:\T_QUERY\new_vidya\tquery.py', '--project', project, '--rev', si_rev, '--query', 'sku_definition.query', '--out_path', block_folder_path, '--db', 'BKUP']
	sku_out = subprocess.run(sku_command, capture_output=True, text=True)
	print(sku_out.stdout)
	print("SKU Data fetched from TSS successfully....")
	print("#######################################################################")
	

def remove_sku():
	print("#######################################################################")
	print("Removing the Sku data from TSS started....")
	remove_sku_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--featuring', featuring, '--query', 'remove_sku.query']
	remove_command = subprocess.run(remove_sku_command, capture_output=True, text=True)
	print(remove_command.stdout)
	print("Removed the sku data from TSS successfully....")
	print("#######################################################################")

def insert_sku():
	unique_rows = pd.DataFrame(columns=['sku_mcn','sku_short_name','featuring'])
	input_file = pd.read_csv(block_folder_path)
	sku_data_fetch_path = block_folder_path.split('/')
	output_path = '/'.join(sku_data_fetch_path[:-1]) + '/'
	print("#######################################################################")
	print("Fetching SKU Data from TSS started....")
	sku_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--query', 'sku_definition.query', '--out_path', output_path, '--db', 'BKUP']
	sku_out = subprocess.run(sku_command, capture_output=True, text=True)
	print(sku_out.stdout)
	print("SKU Data fetched from TSS successfully....")
	print("#######################################################################")
	existing_data = tuple(pd.read_csv(output_path + '/' + 'sku_definition.csv')['featuring'].values)
	for _, row in input_file.iterrows():
		if row['featuring'] in existing_data:
			print(f"Error: Featuring values already exists - {row['featuring']}")
		else:
			unique_rows = unique_rows.append({'sku_mcn':row['sku_mcn'], 'sku_short_name':row['sku_short_name'], 'featuring':row['featuring']}, ignore_index=True)
	for index,row in unique_rows.iterrows():
		sku_mcn = row['sku_mcn']
		sku_short_name = row['sku_short_name']
		featuring = row['featuring']
		print("#######################################################################")
		print("Inserting SKU Data into TSS started....")
		insert_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--sku_mcn', sku_mcn, '--sku_short_name', sku_short_name, '--featuring', featuring, '--query', 'insert_sku.query']
		insert_sku_command = subprocess.run(insert_command, capture_output=True, text=True)
		print(insert_sku_command.stdout)
		print("Insertion of SKU Data into TSS completed....")
		print("#######################################################################")

def update_sku():
	input_file = pd.read_csv(block_folder_path,usecols=['sku_mcn','featuring'])
	for index, row in input_file.iterrows():
		sku_mcn = row['sku_mcn']
		featuring = row['featuring']
		print("#######################################################################")
		print("SKU Definition updation started into TSS....")
		update_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--sku_mcn', sku_mcn, '--featuring', featuring, '--query', 'update_sku.query']
		print(update_command)
		update_sku_command = subprocess.run(update_command, capture_output=True, text=True)
		print(update_sku_command.stdout)
		print("SKU Definition updation into TSS completed....")
		print("#######################################################################")

def csv_to_excel():
	pd.read_csv(block_folder_path + '/' + 'sku_definition.csv').to_excel(block_folder_path + '/' + 'sku_definition.xlsx',sheet_name='sku_definition',index=False)
	# Import sheets from other Excel files
	source_excel = block_folder_path + '/' + 'sku_definition.xlsx'
	# sheet_names_to_import = ['sku_definition'] # List of sheet names to import
	# excel_file1 = block_folder_path + '/' + 'qultivate_phasing.xlsx'
	# for sheet_name in sheet_names_to_import:
	# 	source_df = pd.read_excel(source_excel, sheet_name)
	sku_df = pd.read_excel(source_excel)
	with pd.ExcelWriter(block_folder_path + '/' + 'qultivate_phasing.xlsx', engine='openpyxl', mode='a') as writer:
		sku_df.to_excel(writer, sheet_name='sku_definition', index=False)

	print("CSV converted to Excel and sheets imported successfully.")

def expanding_qultivate_sku_columns():
	
	df_sheet2 = pd.read_csv(block_folder_path + '/' + 'sku_definition.csv')
	column_data = df_sheet2.iloc[1:, [0,2]]
	qultivate_sku_filtered_rows = column_data[column_data.iloc[:,0].str.startswith('SKU') == True]
	sku_column_headings = qultivate_sku_filtered_rows.values.tolist()
	return sku_column_headings

def expanding_columns():
	df_sheet1 = pd.read_excel(block_folder_path + '/' + 'qultivate_populates.xlsx', sheet_name='phasing')
	final_df_sheet1 = convert_to_binary_and_fill_columns(df_sheet1, column_headings)
	final_df_sheet1['qultivate_enable'] = final_df_sheet1.apply(fill_qultivate_enable_values, axis=1)
	qultivate_sku_columns = expanding_qultivate_sku_columns()
	for item in qultivate_sku_columns:
		sku = item[0]
		values = item[1].split(',')
		final_df_sheet1[sku] = final_df_sheet1.apply(lambda row: ','.join([row[val] for val in values]), axis=1)
	final_df_sheet1 = qultivate_sku_fill_values(final_df_sheet1)
	qultivate_bin_header = [col for col in final_df_sheet1.columns if not col.startswith('SKU_') and col not in ['block_name', 'phasing_id', 'pattern_name', 'pattern_type', 'platform', 'qultivate_enable']]
	qultivate_sku_header = [col for col in final_df_sheet1.columns if col.startswith('SKU_')]
	multi_columns = pd.MultiIndex.from_tuples([('QULTIVATE_BIN',col) if col in qultivate_bin_header else ('QULTIVATE_SKU', col) if col in qultivate_sku_header else ('', col) for col in final_df_sheet1.columns])
	final_df_sheet1.columns = multi_columns
	styled_df = final_df_sheet1.style.applymap(coloring_y_values, subset=pd.IndexSlice[:, final_df_sheet1.columns[6:]])
	with pd.ExcelWriter(block_folder_path + '/' + 'qultivate_phasing.xlsx', engine='openpyxl') as writer:
		styled_df.to_excel(writer, sheet_name='qultivate_phasing')

	# removing empty line between header and data
	# writer = pd.ExcelWriter(block_folder_path + '/' + 'qultivate_phasing.xlsx', engine='xlsxwriter')
	# styled_df.to_excel(writer, sheet_name='qultivate_phasing')
	# writer.sheets['qultivate_phasing'].set_row(2, None, None, {'hidden': True})
	# writer.save()
	

def merging_columns(column_headings):
	# Perform reverse process to convert 'Y' and 'N' to binary and integers
	# final_df_sheet1 = pd.read_excel(block_folder_path + '/' + 'qultivate_phasing.xlsx', sheet_name='qultivate_phasing')
	try:
		final_df_sheet1 = pd.read_excel(block_folder_path + '/' + 'qultivate_phasing.xlsx', sheet_name='qultivate_phasing')
	except Exception as e:
    		print("Error:", e)
	df_result = convert_to_binary_and_int(final_df_sheet1, column_headings)
	df_result.to_excel(block_folder_path + '/' + 'merged_data.xlsx', sheet_name='merged', index=False)
	

def getting_phasing_csv(block_folder_path):
	# print("#######################################################################")
	# print("Fetching phasing data from TSS started....")
	# if args.block:
	# 	phasing_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--block', block_name, '--platform', platform,'--query', 'qultivate_phasing_details.query', '--out_path', block_folder_path, '--db', 'BKUP']
	# 	phasing_out = subprocess.run(phasing_command, capture_output=True, text=True)
	# 	print(phasing_out.stdout)
	# else:
	# 	phasing_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/2.0/tquery.py', '--project', project, '--rev', si_rev, '--platform', platform, '--query', 'phasing.query', '--out_path', block_folder_path, '--db', 'BKUP']
	# 	phasing_out = subprocess.run(phasing_command, capture_output=True, text=True)
	# 	print(phasing_out.stdout)
	# print("Phasing data fetched from TSS successfully....")
	# print("#######################################################################")
	csv_file = block_folder_path + '/' + 'phasing.csv'
	qultivate_phasing_dataframe = pd.read_csv(csv_file)
	# Write the DataFrame to an Excel file
	qultivate_phasing_dataframe.to_excel(block_folder_path + '/' + 'qultivate_populates.xlsx')
	excel_file = block_folder_path + '/' + 'qultivate_populates.xlsx'
	# column_names = ['phasing_id', 'qultivate_enable', 'qultivate_value_encoded']
	return csv_file,excel_file


def populate_skn_data():
	# get_sku_definition()
	load_csv_to_excel(block_folder_path + '/' + 'sku_definition.csv', block_folder_path + '/' + 'qultivate_populates.xlsx')
	df_sheet2 = pd.read_excel(block_folder_path + '/' + 'qultivate_populates.xlsx', sheet_name='sku_definition', header=None)
	print(block_folder_path)
	column_data = df_sheet2.iloc[1:, [0,2]]
	filtered_rows = column_data[column_data.iloc[:,0].str.startswith('SKU') == False]
	column_headings = filtered_rows.iloc[:,1].tolist()
	return column_headings


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="load data from csv to excel and compare two dataframes.")
	parser.add_argument("-pull", action="store_true", help="load csv data to excel")
	parser.add_argument("-push", action="store_true", help="compare original vs modified dataframe")
	parser.add_argument("-get_sku", action="store_true", help="get sku definition")
	parser.add_argument("-remove_sku", action="store_true", help="to remove sku")
	parser.add_argument("-update_sku", action="store_true", help="updatesku definition")
	parser.add_argument('-project', required=False, help='project name')
	parser.add_argument('-rev', required=False, help='si revision name')
	parser.add_argument('-block', required=False, help='block name')
	parser.add_argument('-platform', required=False, help='platform name')
	parser.add_argument('-out_path', required=False, help='path to store the csvs')
	parser.add_argument('-featuring', required=False, help='remove sku')
	parser.add_argument('-pushfile', required=False, help='path to read the csvs')
	parser.add_argument('-insert_sku', action="store_true", help="to insert sku")
	
	args = parser.parse_args()
	
	project = args.project
	si_rev = args.rev
	block_name = args.block
	platform =args.platform 
	featuring = args.featuring

	if args.platform:
		platform = args.platform
	else:
		platform ='ATE'

	if args.out_path:
		out_path = args.out_path
	if args.pushfile:
		pushfile = args.pushfile
		
	if args.out_path:
		block_folder_path = out_path
	elif args.pushfile:
		block_folder_path = pushfile

	# check for out_path to end with '/'
	if not block_folder_path.endswith('/') and not block_folder_path.endswith('.csv'):
		block_folder_path += '/'
	
	start_time = time.time()	

	if args.pull:
		csv_file,excel_file = getting_phasing_csv(block_folder_path)
		if os.path.exists(excel_file):
			os.remove(excel_file)
		original_df = pd.read_csv(csv_file)
		column_headings = populate_skn_data()
		load_csv_to_excel(csv_file, excel_file)
		expanding_columns()
		csv_to_excel()
		print(f"Data loaded from {csv_file} to {excel_file} successfully.")

	if args.push:
		column_headings = populate_skn_data()
		merging_columns(column_headings)
		columns = ['phasing_id', 'pattern_name','pattern_type','qultivate_enable', 'qultivate_value_encoded']
		modified_df = pd.read_excel(block_folder_path + '/' + 'merged_data.xlsx', usecols=columns)
		filtered_df = modified_df.dropna()
		# update_statements = []
		# print(filtered_df)
		filtered_df.to_csv(block_folder_path + '/' + 'phasing.csv',index=False)
		print("Qultivate data successfully updated")
		# for index, row in filtered_df.iterrows():
		# 	values = []
		# 	for col in filtered_df.columns:
		# 		if col != 'phasing_id' and not pd.isna(row[col]):
		# 			if col == 'qultivate_value_encoded':
		# 				values.append(f"phasing.{col} = {row[col]}")
		# 	if values:
		# 		sql = "UPDATE phasing SET {}".format(', '.join(values))
		# 		sql += " WHERE phasing.phasing_id = '{}';".format(row['phasing_id'])
		# 		update_statements.append(sql)
		# try:
		# 	stage_dict = decrypt('PROD')
		# 	conn = pymysql.connect(host=stage_dict['host'], port=stage_dict['port'], user= stage_dict['user'], passwd=stage_dict['password'], db=stage_dict['db'])
		# 	conn.autocommit(True)
		# 	cursor = conn.cursor()
		# 	for statement in update_statements:
		# 		if statement:
		# 			print(statement)
		# 			cursor.execute(statement)
		# 	cursor.close()
		# 	print("Qultivate data successfully updated")
		# latest_modified_dataframe = pd.read_excel(block_folder_path + '/' + 'merged_data.xlsx', usecols=columns)
		# latest_modified_dataframe.to_csv(block_folder_path + '/' + 'phasing_backup.csv', index=False)
		# except pymysql.err.ProgrammingError as except_detail:
		# 	print("pymysql.err.ProgrammingError: «{}»".format(except_detail))
		# finally:
		# 	conn.close()
	if args.get_sku:
		get_sku_definition()
	if args.update_sku:
		update_sku()
	if args.remove_sku:
		remove_sku()
	if args.insert_sku:
		insert_sku()
	end_time = time.time()
	print("Script successfully completed in:", end_time - start_time, "seconds")

