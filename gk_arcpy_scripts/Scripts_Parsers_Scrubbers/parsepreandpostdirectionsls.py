
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: parsepreandpostdirectionals.py
Created: 20200917
Modified: 20200917
About: Parses Pre-directional and Post-directional values from the selected field and puts the parsed
       values in the designated fields.
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
	
def ValidateField(fds, fn):
	for f in fds:
		if f.name.upper() == fn.upper():
			return "exists"
	arcpy.AddField_management(lyr, fn, "TEXT", "", "", 2, fn, "NULLABLE", "NON_REQUIRED", "")
	return "new"


	
# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================



# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			  	# Feature Layer containing the target road name data
fstn = arcpy.GetParameterAsText(1)				# Field containing road name values
spre = arcpy.GetParameterAsText(2)				# Field for pre-directional values
spdr = arcpy.GetParameterAsText(3)				# Field for post-directional values


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fds = arcpy.ListFields(lyr)
# dictStrTypes = {}
# dictStrTypes["INTERSTATE"] = "INTERSTATE"
# dictStrTypes["US HIGHWAY"] = "US HIGHWAY"
# dictStrTypes["STATE HIGHWAY"] = "STATE HIGHWAY"
# dictStrTypes["STATE ROAD"] = "STATE ROAD"
# dictStrTypes["STATE ROUTE"] = "STATE ROUTE"
# dictStrTypes["HIGHWAY"] = "HIGHWAY"
# dictStrTypes["COUNTY ROAD"] = "COUNTY ROAD"
# dictStrTypes["BUSINESS ROUTE"] = "BUSINESS ROUTE"
# dictStrTypes["COUNTY LANE"] = "COUNTY LANE"
# dictStrTypes["COUNTY DRIVE"] = "COUNTY DRIVE"
# dictStrTypes["COUNTY STREET"] = "COUNTY STREET"
# dictStrTypes["FARM ROAD"] = "FARM ROAD"
# dictStrTypes["PRIVATE ROAD"] = "PRIVATE ROAD"


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nParsing Pre-directional and Post-directional values frrom " + fstn + " in " + lyr)
msg("========================================================================================================\n\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Pass 1: Parsing pre type street name values
# -----------------------------------------------------------------------------------------------------------

try:

	# Validate Pre and Post directional field name choices.
	if ValidateField(fds, spre) == "exists":
		msg(spre + " exists? True")
	else:
		msg(spre + " exists? False, field created")
	if ValidateField(fds, spdr) == "exists":
		msg(spdr + " exists? True")
	else:
		msg(spdr + " exists? False, field created")
		
		
		

	# #fds = ["'" + fld1 + "', '" + fld2 + "'"]
	# fds = []
	# fds.append(fstn)
	# fds.append(fpre)
	# fds.append(fpdr)

	# cur, row = None, None
	# #cur = arcpy.da.UpdateCursor(lyr, ['STREETNAME', 'PRETYPE'])
	# cur = arcpy.da.UpdateCursor(lyr, fds)
	# for row in cur:
		# n = row[0]
		# v = GetPreType(n)
		# if v != "pass":
			# msg("Parsing " + v + " from " + n)
			# nam = n[len(v):].strip()
			# row[0] = nam
			# row[1] = v
			# cur.updateRow(row)

	# cur, row = None, None	


except Exception as e:
	msg("\n----------------------------------------------------------------------------")
	msg("\nThere was an error parsing the pre and post directional values.")
	msg("\n  Error message:\n  " + str(e))
	row, cur = None, None
	msg("----------------------------------------------------------------------------")




arcpy.AddMessage("\n\nDone!\n\n")



	




