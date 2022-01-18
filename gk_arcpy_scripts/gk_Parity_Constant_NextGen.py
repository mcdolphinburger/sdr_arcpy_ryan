

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: gk_Parity_Constant_NextGen.py
Created: 2018xxxx
Modified: 20200916
About: Calculates/Updates left and right parity values for NENA Next Gen standard.

"""

# Import arcpy module
import arcpy, arcpy.mapping, sys, string, datetime
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(fds, fname):
	for fld in fds:
		if fld.name.upper() == fname.upper():
			#msg("True!")
			return True
	#msg("False!")
	return False

def CreateTextField(lyr, fname, len):
	arcpy.AddField_management(lyr, fname, "TEXT", "", "", len, fname, "NULLABLE", "NON_REQUIRED", "")
	
def GetParity(v):
	if v == 0:
		return "Z"
	elif v % 2 == 0:   #if input_num % 2 == 0
		return "E"
	else:
		return "O"


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
LF = arcpy.GetParameterAsText(1)
LT = arcpy.GetParameterAsText(2)
RF = arcpy.GetParameterAsText(3)
RT = arcpy.GetParameterAsText(4)
pL = arcpy.GetParameterAsText(5)
pR = arcpy.GetParameterAsText(6)

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
desc = arcpy.Describe(lyr)
fc = desc.FeatureClass
fds = arcpy.ListFields(lyr)
PC = "PCONST"





# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
arcpy.AddMessage("\n\nCalculating Parity Constants for Next Gen 9-1-1")
arcpy.AddMessage("========================================================\n\n")









# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


#                                        Check centerline layer for required fields, add them if necessary
# --------------------------------------------------------------------------------------------------------
if not FieldExists(fds, pL):
	CreateTextField(lyr, pL, "4")
	msg("Left Range Parity Constant [PARITY_L] exists?  FALSE (field created)")
else:
	msg("Left Range Parity Constant [PARITY_L] exists?  TRUE")
	
if not FieldExists(fds, pR):
	CreateTextField(lyr, pR, "4")
	msg("Right Range Parity Constant [PARITY_R] exists?  FALSE (field created)")
else:
	msg("Right Range Parity Constant [PARITY_R] exists?  TRUE")
	


#                                                                  Create and write Range Parity Constants
# --------------------------------------------------------------------------------------------------------
cursorfields = []
cursorfields.append(LF)
cursorfields.append(LT)
cursorfields.append(RF)
cursorfields.append(RT)
cursorfields.append(pL)
cursorfields.append(pR)

with arcpy.da.UpdateCursor(lyr, cursorfields) as cur:
	for row in cur:
		pLF = GetParity(row[0])
		pLT = GetParity(row[1])
		pRF = GetParity(row[2])
		pRT = GetParity(row[3])
		
		if pLF == "Z" and pLT == "Z":
			row[4] = "Z"
		elif (pLF == "Z" and pLT == "E") or (pLF == "E" and pLT == "Z"):
			row[4] = "E"
		elif (pLF == "Z" and pLT == "O") or (pLF == "O" and pLT == "Z"):
			row[4] = "O"
		elif (pLF == "E" and pLT == "O") or (pLF == "O" and pLT == "E"):
			row[4] = "B"
		elif pLF == "E" and pLT == "E":
			row[4] = "E"
		elif pLF == "O" and pLT == "O":
			row[4] = "O"

		if pRF == "Z" and pRT == "Z":
			row[5] = "Z"
		elif (pRF == "Z" and pRT == "E") or (pRF == "E" and pRT == "Z"):
			row[5] = "E"
		elif (pRF == "Z" and pRT == "O") or (pRF == "O" and pRT == "Z"):
			row[5] = "O"
		elif (pRF == "E" and pRT == "O") or (pRF == "O" and pRT == "E"):
			row[5] = "B"
		elif pRF == "E" and pRT == "E":
			row[5] = "E"
		elif pRF == "O" and pRT == "O":
			row[5] = "O"
		
		cur.updateRow(row)





arcpy.AddMessage("\n\n\nDone!\n\n\n")