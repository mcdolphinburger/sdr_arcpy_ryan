"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: megareverseline.py
Created: 20170203
Modified: xxx
About: On the selectedline features, reverses the line direction, reverses the ranges and
	   flips the parity.

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


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
lf = "LEFT_FROM"
lt = "LEFT_TO"
rf = "RIGHT_FROM"
rt = "RIGHT_TO"

# lf = "FROMLEFT"
# lt = "TOLEFT"
# rf = "FROMRIGHT"
# rt = "TORIGHT"



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\n\nOn the selected Centerline features:\n  Flipping the line direction\n  Reversing the ranges\n  Flipping the parity\n\n")





# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================
try:
	# Reversing the line direction
	# ------------------------------
	msg("Reversing the line direction...")
	arcpy.FlipLine_edit(lyr)

except Exception as e:
	msg("\nThere was an error reversing the line directions.")
	msg("\n  Error message:\n  " + str(e))

	
try:

	# Reversing the ranges and flipping parity
	# ---------------------------------------------
	msg("Reversing the ranges and flipping the parity...")
	cur = arcpy.UpdateCursor(lyr)
	for row in cur:
		vlf = row.getValue(lf)
		vlt = row.getValue(lt)
		vrf = row.getValue(rf)
		vrt = row.getValue(rt)
		row.setValue(lf, vrt)
		row.setValue(lt, vrf)
		row.setValue(rf, vlt)
		row.setValue(rt, vlf)
		cur.updateRow(row)
		
	cur, row = None, None	
	
except Exception as e:
	msg("\nThere was an error reversing the ranges and/or flipping the parity.")
	msg("\n  Error message:\n  " + str(e))
	row, cur = None, None
	
	


arcpy.AddMessage("\n\nDone!\n\n")



	




