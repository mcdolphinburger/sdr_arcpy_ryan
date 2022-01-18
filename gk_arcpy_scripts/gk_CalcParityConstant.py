

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: calcparityconstant.py
Created: 2012xxxx
Modified: 20191212
About: Calculates the Parity Constant.

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
inLyr = arcpy.GetParameterAsText(0)
LF = arcpy.GetParameterAsText(1)
LT = arcpy.GetParameterAsText(2)
RF = arcpy.GetParameterAsText(3)
RT = arcpy.GetParameterAsText(4)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
desc = arcpy.Describe(inLyr)
fc = desc.FeatureClass
fields = fc.Fields
PC = "PCONST"



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
arcpy.AddMessage("\n\nCalculating Parity Constant")
arcpy.AddMessage("=================================" + "\n\n")









# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


#                                        Check centerline layer for required fields, add them if necessary
# --------------------------------------------------------------------------------------------------------
if FieldExists(fields, "PCONST") != "TRUE":
	CreateTextField(inLyr, "PCONST", "4")
	msg("Range Parity Constant [PCONST] exists?  FALSE (field created)")
else:
	msg("Range Parity Constant [PCONST] exists?  TRUE")
	


#                                                                  Create and write Range Parity Constants
# --------------------------------------------------------------------------------------------------------
msg("\nUpdating Range Parity Constants . . .")
cur = arcpy.UpdateCursor(inLyr)
for feat in cur:
	vLF = float(feat.getValue(LF))
	vLT = float(feat.getValue(LT))
	vRF = float(feat.getValue(RF))
	vRT = float(feat.getValue(RT))
	feat.PCONST = CalculatePCONST(vLF, vLT, vRF, vRT)	
	cur.updateRow(feat)
	


arcpy.AddMessage("\n\n\nDone!\n\n\n")



	




