
"""
Author: Glenn Kammerer
Email: gkammerer.com
Tool: ai_addmsagleftrightfields.py
Created: 20160823
Modified: 20170612
About: Adds Left and Right fields to the attribute table for Zip Code, Postal Community, MSAG Community, 
       ESN and Telco Exchanges, if desired.

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
msg("\nChecking for and adding Left/Right fields to the centerlines layer.\n\n")

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
	

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)

newfieldslist = []
newfieldslist = [
	["PARITY_L","TEXT","2"],
	["PARITY_R","TEXT","2"],
	["COUNTY_L","TEXT","40"],
	["COUNTY_R","TEXT","40"],
	["STATE_L","TEXT","2"],
	["STATE_R","TEXT","2"],
	["ZIP_L","TEXT","5"],
	["ZIP_R","TEXT","5"],
	["ZIP_COMM_L","TEXT","32"],
	["ZIP_COMM_R","TEXT","32"],
	["E911_COMM_L","TEXT","32"],
	["E911_COMM_R","TEXT","32"],
	["ESN_L","SHORT",""],
	["ESN_R","SHORT",""],
	["EXCHANGE_L","TEXT","4"],
	["EXCHANGE_R","TEXT","4"]]



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

for i in newfieldslist:
	if not FieldExists(fields, i[0]):
		msg("  " + i[0] + " already exists? False, creating field")
		arcpy.AddField_management(lyr, i[0], i[1], "", "", i[2], i[0], "NULLABLE", "NON_REQUIRED", "")
	else:
		msg("  " + i[0] + " already exists? True")




msg("\n\nDone!\n\n")



	




