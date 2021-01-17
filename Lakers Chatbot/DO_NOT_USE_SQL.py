# Author: Alfredo Mejia
# Descrp: This file consists of functions that is going to help DO_NOT_USE.py execute the database commands

# Imports
from sqlite3 import Error
import sqlite3
import sys


# Descr: Creates a db file and establishes the connection to it. The connection is then returned
def create_connection(db_name):
    # Try to establish a connection to the db. Otherwise exit the program and display error message
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        sys.exit(e)

    # Return connection
    return conn


# Descr: Executes a create table query to a specific db file
def create_table(db_connection, create_table_query):
    # Try to execute the query to create a table.
    try:
        connection_cursor = db_connection.cursor()
        connection_cursor.execute(create_table_query)

    # Otherwise, display error message and quit program
    except Error as e:
        sys.exit(e)


# Descr: Inserts a list as entries in a table specified in a specific db file
def create_list_entry(db_connection, tb_data, table_name):
    # Get rid of duplicates that are already in the db
    get_rid_duplicates(db_connection, tb_data, table_name)

    # Create a query
    sql = "INSERT INTO " + str(table_name) + "(element) VALUES(?)"

    # Execute query
    for element in tb_data:
        cur = db_connection.cursor()
        cur.execute(sql, [element])
        db_connection.commit()


# Descr: Modifies the list passed (tb_data) and removes any data already in the table. This ensures the insertion of
#        of new data isn't a duplicate
def get_rid_duplicates(db_connection, tb_data, tb_name):
    # Get the db data
    results = get_db_data(db_connection, tb_name)

    # If the db data is in the list, then remove it because it doesn't need to be added
    for id, element in results:
        if element in tb_data:
            tb_data.remove(element)


# Descr: Returns all the data from a specific table in a db file
def get_db_data(db_conn, tb_name):
    # Get all the data given a db from the table
    cur = db_conn.cursor()
    query = "SELECT * FROM " + str(tb_name)
    results = cur.execute(query).fetchall()

    # Return results
    return results
