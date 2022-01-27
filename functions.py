import sqlite3
from sqlite3 import Error
import math
import re


def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False




def connect_to_database(db_file):
	# Create a connection to the SWLite database in the argument

	conn = None

	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
		cursor = conn.cursor()
	except Error as e:
		print(e)
	finally:
		if conn:
			print(" -- connected --")
			
	return conn, cursor




def create_energyLevels_table(conn, cursor):

	try:
		

		cursor.execute("DROP TABLE IF EXISTS energyLevels")

		create_table_command = """CREATE TABLE energyLevels(
			aNum INT,
			element CHAR(20),
			energy FLOAT,
			energyUnc FLOAT,
			spinParity CHAR(20)
		)"""

		cursor.execute(create_table_command)

		print("Table created!")

		conn.commit()


	except Error as e:
		print(e)







def create_NucMasss_table(conn, cursor):

	try:
		

		cursor.execute("DROP TABLE IF EXISTS nuclei")

		create_table_command = """CREATE TABLE nuclearMasses(
			n_minus_z INT,
			zNum INT,
			nNum INT,
			aNum INT,
			element CHAR(20),
			massExcess FLOAT,
			massExcessUnc FLOAT,
			bindingEnergy FLOAT,
			bindingEnergyUnc FLOAT
		)"""

		cursor.execute(create_table_command)

		print("Table created!")

		conn.commit()


	except Error as e:
		print(e)












def input_mass_table(MassTable_file, conn, cursor):


	MassTable = open(MassTable_file, "r")

	# N_minus_Z_string
	# N_string
	# Z_string
	# A_string
	# El_string
	# ME_string
	# MEunc_string
	# BE_string
	# BEunc_string


	line_incriment = 0

	print(" test? ")

	allLines = MassTable.readlines()
	for text in allLines:

		if line_incriment > 38:


			N_minus_Z_string = int(text[1:4])
			N_string = int(text[5:9])
			Z_string = int(text[10:14])
			A_string = int(text[15:19])
			El_string = text[20:24].strip()
			Origin_string = text[25:30].strip()
			ME_string = float(text[31:41].replace("#",""))
			MEunc_string = float(text[42:52].replace("#",""))
			BE_string = float(text[53:64].replace("#",""))
			BEunc_string = float(text[65:72].replace("#",""))


			insert_command = "INSERT INTO nuclearMasses VALUES("+str(N_minus_Z_string) \
				+","+str(N_string) \
				+","+str(Z_string) \
				+","+str(A_string) \
				+",'"+El_string+"'" \
				+","+str(ME_string) \
				+","+str(MEunc_string) \
				+","+str(BE_string) \
				+","+str(BEunc_string)+")"

			print(insert_command)
			

			cursor.execute(insert_command)


		line_incriment+=1

	conn.commit()











def addNuclearLevels(dataFile, conn, cursor):


	ENSDF_table = open(dataFile, "r")

	line_incriment = 0

	previous_levels = [[],[]]


	# Reading in the lines from the ENSDF data file
	allLines = ENSDF_table.readlines()
	for text in allLines:

		lineBegin = text[0:5]
		
		# ====================== mass number =======================
		# ==========================================================
		lineBeginNumbers = ""
		for i in lineBegin.strip():
			if i.isdigit():
				lineBeginNumbers = lineBeginNumbers + i

		# ===================== element symbol =====================
		# ==========================================================
		lineBeginLetters = " ".join(re.findall("[a-zA-Z]+", lineBegin))
		lineBeginLetters.strip()

		# ======================= line type ========================
		# ==========================================================
		lineType = text[5:9].strip()

		# ======================= spin-parity ======================
		# ==========================================================
		spinParity = text[21:39].strip()

		# ========================== Energy ========================
		# ==========================================================
		if lineType == "L":
			if containsNumber(text[9:18]):
				levelEnergy = float(text[9:18])
			if containsNumber(text[19:21]):	
				levelEnergyUnc = float(text[19:21])
			else:
				levelEnergyUnc = 0

			if not (str(lineBeginNumbers+lineBeginLetters) in previous_levels[0] and levelEnergy in previous_levels[1]):
				print(lineBeginNumbers+lineBeginLetters+"   "+str(levelEnergy)+"+/-"+str(levelEnergyUnc)+"|"+spinParity)
				# Here push the data for the level into the SQL database
				# ======================================================

				insert_command = "INSERT INTO energyLevels VALUES("+str(lineBeginNumbers) \
					+",'"+str(lineBeginLetters)+"'" \
					+","+str(levelEnergy) \
					+","+str(levelEnergyUnc) \
					+",'"+str(spinParity)+"')"

				print(insert_command)

				cursor.execute(insert_command)

				# ======================================================

			previous_levels[0].append(str(lineBeginNumbers+lineBeginLetters))
			previous_levels[1].append(levelEnergy)



		line_incriment+=1

	conn.commit()
