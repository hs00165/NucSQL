import sqlite3
from sqlite3 import Error
import math
import re
import functions


if __name__ == '__main__':


	conn, cursor = functions.connect_to_database("NucSQL.db")

	functions.create_energyLevels_table(conn, cursor)


	for i in range(1,13):
		fileName = "raw_data_files/mass"+str(i)+".txt"

		functions.addNuclearLevels(fileName, conn, cursor)