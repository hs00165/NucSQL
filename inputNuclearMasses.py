import sqlite3
from sqlite3 import Error
import math
import functions



if __name__ == '__main__':
	conn, cursor = functions.connect_to_database("NucSQL.db")

	functions.create_NucMasss_table(conn, cursor)
	
	MassTable = "raw_data_files/masstable.txt"

	functions.input_mass_table(MassTable, conn, cursor)