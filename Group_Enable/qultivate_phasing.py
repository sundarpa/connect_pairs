#! /pkg/qct/software/python/sles12/3.9.4/bin/python3
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
from tquery import fetch_data_from_csv

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
	df_result = convert_to_binary_and_int(final_df_sheet1, column_headings)
	df_result.to_excel(block_folder_path + '/' + 'merged_data.xlsx', sheet_name='merged', index=False)


def getting_phasing_csv(folder_path):
	print("#######################################################################")
	print("Fetching phasing data from TSS started....")
	phasing_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/1.9/tquery.py', '--project', project, '--rev', si_rev, '--block', block_name, '--query', 'phasing_details.query', '--out_path', block_folder_path, '--db', 'BKUP']
	phasing_out = subprocess.run(phasing_command, capture_output=True, text=True)
	print(phasing_out.stdout)
	print("Phasing data fetched from TSS successfully....")
	print("#######################################################################")
	csv_file = folder_path + '/' + 'phasing.csv'
	excel_file = block_folder_path + '/' + 'qultivate_populates.xlsx'
	return csv_file,excel_file


def populate_skn_data():
	print("#######################################################################")
	print("Fetching SKU Data from TSS started....")
	sku_command = ['/prj/vlsi/pete/ptetools/prod/utils/tssquery/1.9/tquery.py', '--project', project, '--rev', si_rev, '--query', 'sku_definition.query', '--out_path', block_folder_path, '--db', 'BKUP']
	sku_out = subprocess.run(sku_command, capture_output=True, text=True)
	print(sku_out.stdout)
	print("SKU Data fetched from TSS successfully....")
	print("#######################################################################")
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
	parser.add_argument("-input_file")
	parser.add_argument('-project', required=False, help='project name')
	parser.add_argument('-rev', required=False, help='si revision name')
	parser.add_argument('-block', required=False, help='block name')
	parser.add_argument('-out_path', required=False, help='path to store the csvs')
	args = parser.parse_args()
	
	project = args.project
	si_rev = args.rev
	block_name = args.block
	out_path = args.out_path

	project_folder_path = os.path.join(out_path,project)
	rev_folder_path = os.path.join(project_folder_path,si_rev)
	block_folder_path = os.path.join(rev_folder_path,block_name)
	if not os.path.exists(block_folder_path):
		os.makedirs(block_folder_path, exist_ok=False)	
	
	start_time = time.time()	

	if args.pull:
		csv_file,excel_file = getting_phasing_csv(block_folder_path)
		if os.path.exists(excel_file):
			os.remove(excel_file)
		original_df = pd.read_csv(csv_file)
		column_headings = populate_skn_data()
		load_csv_to_excel(csv_file, excel_file)
		expanding_columns()
		print(f"Data loaded from {csv_file} to {excel_file} successfully.")

	if args.push:
		column_headings = populate_skn_data()
		merging_columns(column_headings)
		columns = ['phasing_id', 'qultivate_enable', 'qultivate_category', 'qultivate_value_encoded']
		modified_df = pd.read_excel(block_folder_path + '/' + 'merged_data.xlsx', usecols=columns)
		filtered_df = modified_df[(modified_df['qultivate_enable'].isna()) & (modified_df['qultivate_category'].isna()) & (modified_df['qultivate_value_encoded'] != 0)]
		update_statements = []
		for index, row in filtered_df.iterrows():
			update_values = ', '.join([f"phasing.{col} = {row[col]}" for col in filtered_df.columns if col != 'phasing_id' and not pd.isna(row[col])])
			update_statement = f"UPDATE phasing SET {update_values} WHERE phasing.phasing_id = '{row['phasing_id']}';"
			update_statements.append(update_statement)
		try:
			stage_dict = decrypt('PROD')
			# database connection setup
			conn = pymysql.connect(host=stage_dict['host'], port=stage_dict['port'], user= stage_dict['user'], passwd=stage_dict['password'], db=stage_dict['db'])
			conn.autocommit(True)
			cursor = conn.cursor()
			for statement in update_statements:
				if statement:
					cursor.execute(statement)
			cursor.close()
		except pymysql.err.ProgrammingError as except_detail:
			print("pymysql.err.ProgrammingError: «{}»".format(except_detail))
		finally:
			conn.close()
	end_time = time.time()
	print("Script successfully completed in:", end_time - start_time, "seconds")
#        modified_df.to_csv(csv_file, index=False, mode='w')
