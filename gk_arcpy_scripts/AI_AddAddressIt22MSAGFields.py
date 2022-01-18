# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# AI_AddAddressIt22MSAGFields.py
# Created on: 2014-05-21
#
#
# Description: 
# ----------------
#  
# 
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)



# Arguments: input table, field name, field type, precision, scale, length, field alias, is nullable, is required, domain


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if not FieldExists(fields, "E911_COMM_E"):
	arcpy.AddField_management(lyr, "E911_COMM_E", "TEXT", "", "", "32", "E911_COMM_E", "NULLABLE", "NON_REQUIRED", "")
if not FieldExists(fields, "E911_COMM_O"):
	arcpy.AddField_management(lyr, "E911_COMM_O", "TEXT", "", "", "32", "E911_COMM_O", "NULLABLE", "NON_REQUIRED", "")
if not FieldExists(fields, "ESN_E"):
	arcpy.AddField_management(lyr, "ESN_E", "SHORT", "", "", "", "ESN_E", "NULLABLE", "NON_REQUIRED", "")
if not FieldExists(fields, "ESN_O"):
	arcpy.AddField_management(lyr, "ESN_O", "SHORT", "", "", "", "ESN_O", "NULLABLE", "NON_REQUIRED", "")
if not FieldExists(fields, "EXCHANGE_E"):
	arcpy.AddField_management(lyr, "EXCHANGE_E", "TEXT", "", "", "32", "EXCHANGE_E", "NULLABLE", "NON_REQUIRED", "")
if not FieldExists(fields, "EXCHANGE_O"):
	arcpy.AddField_management(lyr, "EXCHANGE_O", "TEXT", "", "", "32", "EXCHANGE_O", "NULLABLE", "NON_REQUIRED", "")


msg("\n\nDone!\n\n")



	




