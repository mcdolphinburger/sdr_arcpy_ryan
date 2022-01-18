
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: detecttextinnumbers.py
Created: 20160927
Modified: 20161216
About: Evaluates a string attribute to see if it is an integer. If it is not, the Object ID and 
       value are displayed to the user.

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
	
def isinteger(x):
	if not x.isdigit():
		return False
	else:
		f = float(x)
		if f.is_integer():
			return True
		else:
			return False
		
	

# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================





# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			  		# Feature Layer
fld = arcpy.GetParameterAsText(1)			  		# The the field to check


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
oidfld = arcpy.Describe(lyr).OIDFieldName
cursorfields = []
cursorfields.append(oidfld)
cursorfields.append(fld)


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\n\nAnd away we go!\n-------------------------------------------------\n")




# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# cur = arcpy.UpdateCursor(lyr)
cur = arcpy.da.SearchCursor(lyr, cursorfields)
for row in cur:
	i = row[0]
	val = row[1]
	if val is None:
		msg(str(i) + ":  NULL")
	elif not isinteger(str(val)):
		msg(str(i) + ":  " + val)

row, cur = None, None



arcpy.AddMessage("\n\nDone!\n\n")



	




