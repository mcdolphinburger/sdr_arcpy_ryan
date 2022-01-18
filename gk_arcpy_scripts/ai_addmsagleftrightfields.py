
"""
Author: Glenn Kammerer
Email: gkammerer.com
Tool: ai_addmsagleftrightfields.py
Created: 20160823
Modified: 20170612
About: Adds Left and Right fields to the attribute table for MSAG Community, ESn and Telco Exchanges, if desired.

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
msg("\n\n")

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
bCOM = arcpy.GetParameter(1)
bESN = arcpy.GetParameter(2)	
bEXC = arcpy.GetParameter(3)		


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)
mcommL = "COMM_L"
mcommR = "COMM_R"
esnL = "ESN_L"
esnR = "ESN_R"
exchL = "EXCH_L"
exchR = "EXCH_R"
zipL = "ZIP_L"
zipR = "ZIP_R"




# Arguments: input table, field name, field type, precision, scale, length, field alias, is nullable, is required, domain


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if bCOM:
	msg("Adding MSAG Community Left/Right fields")
	if not FieldExists(fields, "COMM_L"):
		arcpy.AddField_management(lyr, "COMM_L", "TEXT", "", "", "32", "COMM_L", "NULLABLE", "NON_REQUIRED", "")
	if not FieldExists(fields, "COMM_R"):
		arcpy.AddField_management(lyr, "COMM_R", "TEXT", "", "", "32", "COMM_R", "NULLABLE", "NON_REQUIRED", "")
if bESN:
	msg("Adding MSAG ESN Left/Right fields")
	if not FieldExists(fields, "ESN_L"):
		arcpy.AddField_management(lyr, "ESN_L", "SHORT", "", "", "", "ESN_L", "NULLABLE", "NON_REQUIRED", "")
	if not FieldExists(fields, "ESN_R"):
		arcpy.AddField_management(lyr, "ESN_R", "SHORT", "", "", "", "ESN_R", "NULLABLE", "NON_REQUIRED", "")
if bEXC:
	msg("Adding MSAG Telco Exchange Left/Right fields")
	if not FieldExists(fields, "EXCH_L"):
		arcpy.AddField_management(lyr, "EXCH_L", "TEXT", "", "", "32", "EXCH_L", "NULLABLE", "NON_REQUIRED", "")
	if not FieldExists(fields, "EXCH_R"):
		arcpy.AddField_management(lyr, "EXCH_R", "TEXT", "", "", "32", "EXCH_R", "NULLABLE", "NON_REQUIRED", "")


msg("\n\nDone!\n\n")



	




