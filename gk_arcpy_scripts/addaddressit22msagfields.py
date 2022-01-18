

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: addaddressit22msagfields.py
Created: 2012-07-27
Modified: 2020-01-25
About: Adds the AddressIt 2.3 road range fields.

"""



# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(m):
	arcpy.AddMessage(m)
	
	
def FieldExists(fields, fname):
	for fld in fields:
		if fld.name == fname:
			return True
	return False


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nAdding AddressIt 2.2 Road Range Fields\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
sidetype = arcpy.GetParameterAsText(1)
doZip = arcpy.GetParameter(2)
doZipComm = arcpy.GetParameter(3)
doMSAGComm = arcpy.GetParameter(4)
doESN = arcpy.GetParameter(5)
doTelco = arcpy.GetParameter(6)



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)



# Arguments: input table, field name, field type, precision, scale, length, field alias, is nullable, is required, domain


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if doZip:
	if sidetype == "Even/Odd":
		if not FieldExists(fields, "ZIP_E"):
			arcpy.AddField_management(lyr, "ZIP_E", "TEXT", "", "", "32", "ZIP_E", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "ZIP_O"):
			arcpy.AddField_management(lyr, "ZIP_O", "TEXT", "", "", "32", "ZIP_O", "NULLABLE", "NON_REQUIRED", "")
	else:
		if not FieldExists(fields, "ZIP_L"):
			arcpy.AddField_management(lyr, "ZIP_L", "TEXT", "", "", "32", "ZIP_L", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "ZIP_R"):
			arcpy.AddField_management(lyr, "ZIP_R", "TEXT", "", "", "32", "ZIP_R", "NULLABLE", "NON_REQUIRED", "")
			
if doZipComm:
	if sidetype == "Even/Odd":
		if not FieldExists(fields, "ZIP_COMM_E"):
			arcpy.AddField_management(lyr, "ZIP_COMM_E", "TEXT", "", "", "32", "ZIP_COMM_E", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "ZIP_COMM_O"):
			arcpy.AddField_management(lyr, "ZIP_COMM_O", "TEXT", "", "", "32", "ZIP_COMM_O", "NULLABLE", "NON_REQUIRED", "")
	else:
		if not FieldExists(fields, "ZIP_COMM_L"):
			arcpy.AddField_management(lyr, "ZIP_COMM_L", "TEXT", "", "", "32", "ZIP_COMM_L", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "ZIP_COMM_R"):
			arcpy.AddField_management(lyr, "ZIP_COMM_R", "TEXT", "", "", "32", "ZIP_COMM_R", "NULLABLE", "NON_REQUIRED", "")
	
if doMSAGComm:
	if sidetype == "Even/Odd":
		if not FieldExists(fields, "E911_COMM_E"):
			arcpy.AddField_management(lyr, "E911_COMM_E", "TEXT", "", "", "32", "E911_COMM_E", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "E911_COMM_O"):
			arcpy.AddField_management(lyr, "E911_COMM_O", "TEXT", "", "", "32", "E911_COMM_O", "NULLABLE", "NON_REQUIRED", "")
	else:
		if not FieldExists(fields, "E911_COMM_L"):
			arcpy.AddField_management(lyr, "E911_COMM_L", "TEXT", "", "", "32", "E911_COMM_L", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "E911_COMM_R"):
			arcpy.AddField_management(lyr, "E911_COMM_R", "TEXT", "", "", "32", "E911_COMM_R", "NULLABLE", "NON_REQUIRED", "")
	
if doESN:
	if sidetype == "Even/Odd":
		if not FieldExists(fields, "ESN_E"):
			arcpy.AddField_management(lyr, "ESN_E", "SHORT", "", "", "", "ESN_E", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "ESN_O"):
			arcpy.AddField_management(lyr, "ESN_O", "SHORT", "", "", "", "ESN_O", "NULLABLE", "NON_REQUIRED", "")
	else:
		if not FieldExists(fields, "ESN_L"):
			arcpy.AddField_management(lyr, "ESN_L", "SHORT", "", "", "", "ESN_L", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "ESN_R"):
			arcpy.AddField_management(lyr, "ESN_R", "SHORT", "", "", "", "ESN_R", "NULLABLE", "NON_REQUIRED", "")
	
if doTelco:
	if sidetype == "Even/Odd":
		if not FieldExists(fields, "EXCHANGE_E"):
			arcpy.AddField_management(lyr, "EXCHANGE_E", "TEXT", "", "", "32", "EXCHANGE_E", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "EXCHANGE_O"):
			arcpy.AddField_management(lyr, "EXCHANGE_O", "TEXT", "", "", "32", "EXCHANGE_O", "NULLABLE", "NON_REQUIRED", "")
	else:
		if not FieldExists(fields, "EXCHANGE_L"):
			arcpy.AddField_management(lyr, "EXCHANGE_L", "TEXT", "", "", "32", "EXCHANGE_L", "NULLABLE", "NON_REQUIRED", "")
		if not FieldExists(fields, "EXCHANGE_R"):
			arcpy.AddField_management(lyr, "EXCHANGE_R", "TEXT", "", "", "32", "EXCHANGE_R", "NULLABLE", "NON_REQUIRED", "")
	



msg("\n\nDone!\n\n")



	




