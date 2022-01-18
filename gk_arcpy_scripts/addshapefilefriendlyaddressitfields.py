
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: addshapefilefriendlyaddressitfields.py
Created: 20180209
Modified: 20180209
About: Converts some AddressIt field names so they don't get truncated when exported to Shapefile

"""




# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)
	
	
def FieldExists(fields, fname):
	for fld in fields:
		if fld.name == fname:
			return True
	return False





# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)

FL = []
FL = [
	["DATE_CREATED", "DATE_NEW"],
	["DATE_MODIFIED", "DATE_MOD"],
	["USER_INITIALS", "USER_INIT"],
	["STRUCTURE_NUM", "HOUSE_NUM"],
	["STREET_NAME", "STR_NAME"],
	["STREET_TYPE", "STR_TYPE"],
	["COMP_STR_NAME", "FULL_NAME"],
	["FULL_ADDRESS", "FULL_ADD"],
	["FIRST_NAME1", "FIRSTNAME1"],
	["FIRST_NAME2", "FIRSTNAME2"],
	["CELL_PHONE1", "CELLPHONE1"],
	["CELL_PHONE2", "CELLPHONE2"],
	["STRUCTURE_COMP", "STRUCTCOMP"],
	["STRUCTURE_TYPE", "STRUCTTYPE"],
	["LAST_CHANGE", "LASTCHANGE"],
	["DATA_SOURCE", "DATASOURCE"],
	["FEATURE_GUID", "FEAT_GUID"],
	["CLASSIFICATION", "STR_CLASS"],
	["E911_COMM_E", "E911COMME"],
	["E911_COMM_O", "E911COMMO"],
	["E911_COMM_L", "E911COMML"],
	["E911_COMM_R", "E911COMMR"]
	]
	


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fds = arcpy.ListFields(lyr)


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n")

	

# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

for i in FL:
	if FieldExists(fds, i[0]):
		msg(" Renaming field " + str(i[0]) + " to " + str(i[1]))
		arcpy.AlterField_management(lyr, i[0], i[1])






arcpy.AddMessage("\n\n\n")



	




