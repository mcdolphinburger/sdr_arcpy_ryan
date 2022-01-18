
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: parsepretypes.py
Created: 20160623
Modified: 20170510
About: Parses Pre Type values from the Street Name field and puts them in the Pre Type field and removes
       it from the Street Name field.
"""



# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def GetPreType(nam):
	pt = "pass"
	for i in dictStrTypes:
		if i in n:
			if n[:len(i)] == i:
				pt = i
	return pt


	
# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================



# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			  	# Feature Layer containing compiled road name attributes
fld1 = arcpy.GetParameterAsText(1)				# Field containing road name values
fld2 = arcpy.GetParameterAsText(2)				# Field for Pre Type values


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
dictStrTypes = {}
dictStrTypes["INTERSTATE"] = "INTERSTATE"
dictStrTypes["US HIGHWAY"] = "US HIGHWAY"
dictStrTypes["STATE HIGHWAY"] = "STATE HIGHWAY"
dictStrTypes["STATE ROAD"] = "STATE ROAD"
dictStrTypes["STATE ROUTE"] = "STATE ROUTE"
dictStrTypes["HIGHWAY"] = "HIGHWAY"
dictStrTypes["COUNTY ROAD"] = "COUNTY ROAD"
dictStrTypes["BUSINESS ROUTE"] = "BUSINESS ROUTE"
dictStrTypes["COUNTY LANE"] = "COUNTY LANE"
dictStrTypes["COUNTY DRIVE"] = "COUNTY DRIVE"
dictStrTypes["COUNTY STREET"] = "COUNTY STREET"
dictStrTypes["FARM ROAD"] = "FARM ROAD"
dictStrTypes["PRIVATE ROAD"] = "PRIVATE ROAD"


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nParsing Pre Type values frrom " + fld1 + " in " + lyr)
msg("========================================================================================================\n\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Pass 1: Parsing pre type street name values
# -----------------------------------------------------------------------------------------------------------

try:

	#fds = ["'" + fld1 + "', '" + fld2 + "'"]
	fds = []
	fds.append(fld1)
	fds.append(fld2)

	cur, row = None, None
	#cur = arcpy.da.UpdateCursor(lyr, ['STREETNAME', 'PRETYPE'])
	cur = arcpy.da.UpdateCursor(lyr, fds)
	for row in cur:
		n = row[0]
		v = GetPreType(n)
		if v != "pass":
			msg("Parsing " + v + " from " + n)
			nam = n[len(v):].strip()
			row[0] = nam
			row[1] = v
			cur.updateRow(row)

	cur, row = None, None	


except Exception as e:
	msg("\nThere was an error re-calculating the full street names.")
	msg("\n  Error message:\n  " + str(e))
	row, cur = None, None




arcpy.AddMessage("\n\nDone!\n\n")



	




