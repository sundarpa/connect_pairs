import pymysql
import configparser
import base64
import os
import sys
def decrypt(encrypted_str):
    try:
        decrypted_bytes = base64.b64decode(encrypted_str)
        decrypted_str = decrypted_bytes.decode('utf-8')
        return decrypted_str
    except Exception as e:
        print("Error decrypting:", str(e))
        return None
# Give code If the config is not present in the tool location, create a dummy and ask user to fill up.
def create_dummy_config(config_path):
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config['REMOTEDB'] = {
            'host': 'your_remote_db_host',
            'port': 'your_remote_db_port',
            'user': 'your_remote_db_user',
            'db': 'your_remote_db_name',
            'encrypted_password': 'your_base64_encoded_password'
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
            print(f"Configuration file '{config_path}' created. Please fill in the required information.")

def get_database_connection(config_path, db_name=None):
    if config_path is None:
        config_path = "./config.ini"

    if not os.path.exists(config_path):
        print("Configuration file not found. Creating a dummy configuration.")
        create_dummy_config(config_path)
        return None  # Exit the function since the config file is not present

    config = configparser.ConfigParser()
    config.read(config_path)


    if db_name is None and len(sys.argv) > 2 and sys.argv[1] == '--db':
        db_name = sys.argv[2].upper()  # Use the provided database name directly and convert to uppercase

    if db_name is not None and db_name not in config:
        print(f"Database '{db_name}' configuration not found in the configuration file.")
        print("Config sections:", config.sections())
        return None

    db_section = db_name or 'TQUERY'  # Use the provided database name or default to 'TQUERY'

    db_host = config[db_section]['host']
    db_port = int(config[db_section]['port'])
    db_user = config[db_section]['user']
    db_db = config[db_section]['db']
    encrypted_db_password = config[db_section]['encrypted_password']

    db_password = decrypt(encrypted_db_password)

    try:
        db_credentials = {
            'host': db_host,
            'port': db_port,
            'user': db_user,
            'passwd': db_password,
            'db': db_db
        }

        conn = pymysql.connect(**db_credentials)
        conn.autocommit(True)
        print(f"Connected to the '{db_section}' database.")
        return conn
    except pymysql.Error:
        print(f"Failed to connect to the '{db_section}' database.")
        return None
