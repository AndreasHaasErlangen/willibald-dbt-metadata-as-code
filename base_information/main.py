import json
import sqlite3
import requests
import lib
import transform
import argparse
from argparse import RawTextHelpFormatter

# Load metadata from dataspot into FDM_Willibald.json

def dataspot2sqlite(credential_file_name:str, database_file:str):

    username, password = lib.get_userinfo(credential_file_name)
    # Create SQLite database and table
    sqlite_databasename = database_file #'dataspotparameters.db'
    conn,cursor=lib.get_cursor(sqlite_databasename)
    lib.create_sqlite_tables(cursor=cursor, replace=True)
    lib.create_sqlite_views(cursor=cursor, replace=True)

    source_data_fdm = lib.get_source('FDM_Willibald', username, password)
    transform.to_rules(source=source_data_fdm, cursor=cursor, table_name='fdm_dataspot_rules')
    transform.to_relationships(source=source_data_fdm, cursor=cursor, table_name='fdm_dataspot_relationship')
    transform.to_business_attribute(source=source_data_fdm, cursor=cursor, table_name='fdm_dataspot_businessattribute')
    transform.to_business_object(source=source_data_fdm, cursor=cursor, table_name='fdm_dataspot_businessobject')
    transform.to_transformation(source=source_data_fdm, cursor=cursor, table_name='fdm_dataspot_transformation')

    source_data_tdm = lib.get_source('TDM_Willibald', username, password)

    transform.to_physical_source_attributes(source=source_data_tdm, cursor=cursor, table_name='tdm_dataspot_source_attributes')
    transform.to_physical_source_table(source=source_data_tdm, cursor=cursor, table_name='tdm_dataspot_source_table')
    transform.to_physical_source(source=source_data_tdm, cursor=cursor, table_name='tdm_dataspot_source')
    transform.to_source_add_attributes(source=source_data_tdm, cursor=cursor, table_name='tdm_dataspot_source_add_attributes')
    transform.to_source_datatypes(source=source_data_tdm, cursor=cursor, table_name='tdm_dataspot_source_datatypes')


    conn.commit()
    conn.close()


if __name__ == '__main__':

    # python main.py 
    # python main.py -c credentials.json -d "c:\\temp\\dataspotparameters.db"
    parser = argparse.ArgumentParser(
                    prog = 'data2sqllite', formatter_class=RawTextHelpFormatter, 
                    description = 'Gets json from the dataspot-website and creates meta-data for turbovault4dbt. \n usage: python main.py (defaults: credentials.json and dataspotparameters.db in current folder) \n or python main.py -c credentials.json -d "c:\\temp\\dataspotparameters.db"')
    parser.add_argument('-c', '--credential_file_name', help='Name (and Path) of credential-file', default="credentials.json")
    parser.add_argument('-d', '--database_file', help='Name (and Path of the sqlite-database-file)', default="dataspotparameters.db")                     
    
    args = parser.parse_args()
    
    dataspot2sqlite(credential_file_name=args.credential_file_name, database_file=args.database_file)
