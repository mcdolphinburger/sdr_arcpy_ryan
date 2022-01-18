"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: gk_Parity_Constant.py
Created: 20120201
Modified: 20170609
About: Evaluates a string attribute to see if it is an integer. If it is not, the Object ID and 
       value are displayed to the user.

"""

# Import arcpy module
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env

# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(lyr, fname):
	for fld in arcpy.ListFields(lyr):
		if fld.name == fname:
			return True
	return False
	
def Parity(num):
	p = "-"
	if num == 0:
		p = "X"
	elif num/2 == int(num/2):
		p = "E"
	else:
		p = "O"
	return p



# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrR = arcpy.GetParameterAsText(0)					# Road centerline feature layer
theschema = arcpy.GetParameterAsText(1)				# Schema to use to get address range field names
LF = arcpy.GetParameterAsText(2)					# Left address range From/Low field
LT = arcpy.GetParameterAsText(3)					# Left address range To/High field
RF = arcpy.GetParameterAsText(4)					# Right address range From/Low field
RT = arcpy.GetParameterAsText(5)					# Right address range To/High field


# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
if theschema == "Oklahoma Webmap":
	LF = "L_FROM_ADD"
	LT = "L_TO_ADD"
	RF = "R_FROM_ADD"
	RT = "R_TO_ADD"
    



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Check centerline layer for PCONST field. Add it if necessary.
# --------------------------------------------------------------------------------------------------------------

if FieldExists(lyrR, "PCONST"):
		msg("\n\nThe field Parity Constant [PCONST] exists?  TRUE")
else:
	arcpy.AddField_management(lyrR, "PCONST", "TEXT", "", "", "4", "PCONST", "NULLABLE", "NON_REQUIRED", "")
	msg("\n\nThe field Parity Constant [PCONST] exists?  FALSE (field created)")

    
curfds = [LF, LT, RF, RT, "PCONST"]
    

# Create and write Range Parity Constants.
# --------------------------------------------------------------------------------------------------------------
msg("Writing range parity constants.")
cur = arcpy.da.UpdateCursor(lyrR, curfds)
for row in cur:
	cLF = Parity(float(row[0]))
	cLT = Parity(float(row[1]))
	cRF = Parity(float(row[2]))
	cRT = Parity(float(row[3]))
	row[4] = cLF + cLT + cRF + cRT
	cur.updateRow(row)

	
		
		
msg("\n\nDone!\n\n")



