
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: addzeroestoblankrangevalues.py
Created: 20161216
Modified: 20170418
About: In street centerline data with range fields as text, will change the value of blank range value to a zero.

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
schema = arcpy.GetParameterAsText(1)			  	# String; the schema for the range fields
fldLF = arcpy.GetParameterAsText(2)			  		# The Left Low field to check
fldLT = arcpy.GetParameterAsText(3)			  		# The Left High field to check
fldRF = arcpy.GetParameterAsText(4)			  		# The Right Low field to check
fldRT = arcpy.GetParameterAsText(5)			  		# The Right High field to check


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------

#fldOID = arcpy.Describe(lyr).OIDFieldName

# if schema == "AddressIt 2.1" or schema == "AddressIt 2.3":
	# fldLF = "LEFT_FROM"
	# fldLT = "LEFT_TO"
	# fldRF = "RIGHT_FROM"
	# fldRT = "RIGHT_TO"
# elif schema == "Oklahoma Webmap":
	# fldLF = "L_FROM_ADD"
	# fldLT = "L_TO_ADD"
	# fldRF = "R_FROM_ADD"
	# fldRT = "R_TO_ADD"
	
cursorfields = []
cursorfields = [fldLF, fldLT, fldRF, fldRT]
# cursorfields.append(fldLF)
# cursorfields.append(fldLT)
# cursorfields.append(fldRF)
# cursorfields.append(fldRT)



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\n\nAnd away we go!\n-------------------------------------------------\n")




# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# cur = arcpy.UpdateCursor(lyr)
cur = arcpy.da.UpdateCursor(lyr, cursorfields)
for row in cur:
	if row[0] is None or row[0].strip() == "":
		row[0] = 0
		cur.updateRow(row)
	if row[1] is None or row[1].strip() == "":
		row[1] = 0
		cur.updateRow(row)
	if row[2] is None or row[2].strip() == "":
		row[2] = 0
		cur.updateRow(row)
	if row[3] is None or row[3].strip() == "":
		row[3] = 0
		cur.updateRow(row)		

row, cur = None, None



arcpy.AddMessage("\n\nDone!\n\n")



	




