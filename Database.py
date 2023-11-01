import pymysql
import configparser
import base64

def decrypt(encrypted_str):
    try:
        decrypted_bytes = base64.b64decode(encrypted_str)
        decrypted_str = decrypted_bytes.decode('utf-8')
        return decrypted_str
    except Exception as e:
        print("Error decrypting:", str(e))
        return None

def get_database_connection(config_path):
    if config_path is None:
        config_path = "./config.ini"
    config = configparser.ConfigParser()
    config.read(config_path)

    # # Determine the configuration file path based on the command-line argument or use the default
    # if config_path:
    #     CONFIG_PATH = config_path
    # else:
    #     CONFIG_PATH = "./config.ini"

    # Create a ConfigParser and read the configuration file
    config = configparser.ConfigParser()
    config.read(config_path)

    db_host = config['SEARCHTOOL']['host']
    db_port = int(config['SEARCHTOOL']['port'])
    db_user = config['SEARCHTOOL']['user']
    db_db = config['SEARCHTOOL']['db']
    encrypted_db_password = config['SEARCHTOOL']['encrypted_password']

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
        print("Connected to the remote database.")
        return conn
    except pymysql.Error:
        print("Failed to connect to the remote database")

        # If the remote connection fails, connect to the local database
        local_db_host = config['LOCALDB']['host']
        local_db_port = int(config['LOCALDB']['port'])
        local_db_user = config['LOCALDB']['user']
        local_db_db = config['LOCALDB']['db']
        encrypted_local_db_password = config['LOCALDB']['encrypted_password']

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
            return conn
        except pymysql.Error:
            print("Failed to connect to the local database.")
            return None
