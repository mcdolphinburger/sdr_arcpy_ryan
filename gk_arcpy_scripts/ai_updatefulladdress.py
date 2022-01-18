
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: ai_updatecompiledroadnameandfulladdress.py
Created: 20120605
Modified: 20170612
About: Re-calculates the AddressIt full address values.

"""




# Import modules
# ---------------------------
import sys, arcpy, arcpy.mapping, string, datetime


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)                 		# feature layer to act on
fldHN = arcpy.GetParameterAsText(1)                     # field containing structure numbers
fldSTR = arcpy.GetParameterAsText(2)                    # field containing full street names
fldUNIT = arcpy.GetParameterAsText(3)					# field containing unit designations (optional)
fldADD = arcpy.GetParameterAsText(4)					# field containing the full address

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
cursorfields = [fldHN, fldSTR, fldADD]
if fldUNIT:
	cursorfields.append(fldUNIT)
	


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------
m = "\n\nCalculating and Updating Full Address values"
m = m + "\n------------------------------------------------------------------------\n"
msg(m)

# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Calculating address point full address values
# --------------------------------------------------------------------------------------------------------------
row, cur = None, None
cur = arcpy.da.UpdateCursor(lyr, cursorfields)
for row in cur:
	a = row[0]
	nam = row[1]
	if fldUNIT:
		unit = row[3]
	else:
		unit = ""
	fulladd = ((str(a) + " " + nam).strip() + " " + unit).strip()
	row[2] = fulladd
	cur.updateRow(row)





arcpy.AddMessage("\n\nDone!\n\n")



	




