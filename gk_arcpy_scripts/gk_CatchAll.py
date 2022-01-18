# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# gk_CatchAll.py
# Created on: 2013-07-09
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
import arcpy, arcpy.mapping, sys, string, datetime
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(fields, fname):
	doesexist = "FALSE"
	for fld in fields:
		if fld.Name == fname:
			doesexist = "TRUE"
	return doesexist

def CreateTextField(lyr, fname, len):
	arcpy.AddField_management(lyr, fname, "TEXT", "", "", len, fname, "NULLABLE", "NON_REQUIRED", "")
	
def CalculatePCONST(x1, x2, y1, y2):
	if x1 == 0:
		cLF = "X"
	elif x1/2 == int(x1/2):
		cLF = "E"
	else:
		cLF = "O"
	if x2 == 0:
		cLT = "X"
	elif x2/2 == int(x2/2):
		cLT = "E"
	else:
		cLT = "O"
	if y1 == 0:
		cRF = "X"
	elif y1/2 == int(y1/2):
		cRF = "E"
	else:
		cRF = "O"
	if y2 == 0:
		cRT = "X"
	elif y2/2 == int(y2/2):
		cRT = "E"
	else:
		cRT = "O"
	return cLF + cLT + cRF + cRT


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)
fldLO = "RNG_FROM"
fldHI = "RNG_TO"



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	










# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


	


#                                                                  Create and write Range Parity Constants
# --------------------------------------------------------------------------------------------------------
msg("\nRearranging Low/High values.")
cur = arcpy.UpdateCursor(lyr)
for row in cur:
	L = row.getValue(fldLO)
	H = row.getValue(fldHI)
	if L > H:
		vLO = H
		vHI = L
		row.setValue(fldLO, vLO)
		row.setValue(fldHI, vHI)
	cur.updateRow(row)
	



row = None
cur = None

arcpy.AddMessage("\n\n\nDone!\n\n\n")



	




