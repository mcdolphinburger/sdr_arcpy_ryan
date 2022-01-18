
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: AI_CalcRangeLowHigh.py
Created: 20120204
Modified: 20170709
About: Calculates the Low and High address range values and writes them to the centerlines. Also calculates and
       writes the Parity Constant to the centerlines.

"""

## -------------------------------------------------------------------------------------------------------
##                               Import Modules
## -------------------------------------------------------------------------------------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


## -------------------------------------------------------------------------------------------------------
##                               Functions
## -------------------------------------------------------------------------------------------------------

def msg(msg):
	arcpy.AddMessage(msg)

def FieldExists(fields, fname):
	for fld in fields:
		if fld.Name == fname:
			return True
	return False

def CreateTextField(lyr, fname, len):
	arcpy.AddField_management(lyr, fname, "TEXT", "", "", len, fname, "NULLABLE", "NON_REQUIRED", "")
	
def CreateLongField(lyr, fname):
	arcpy.AddField_management(lyr, fname, "LONG", "", "", "", fname, "NULLABLE", "NON_REQUIRED", "")
	
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

	
#                                                                                               B E G I N
# -------------------------------------------------------------------------------------------------------

arcpy.AddMessage("\n\nCalculating Range LOW/HIGH Values")
arcpy.AddMessage("=================================" + "\n\n")


#                                                                                        Script arguments
# -------------------------------------------------------------------------------------------------------
FL1 = arcpy.GetParameterAsText(0)										



#                                                                               Initialize some variables
# -------------------------------------------------------------------------------------------------------
desc1 = arcpy.Describe(FL1)
fc1 = desc1.FeatureClass
fields1 = fc1.Fields
PC = "PCONST"
LF = "LEFT_FROM"
LT = "LEFT_TO"
RF = "RIGHT_FROM"
RT = "RIGHT_TO"
# LF = "L_FROM_ADD"
# LT = "L_TO_ADD"
# RF = "R_FROM_ADD"
# RT = "R_TO_ADD"
# LF = "FROMLEFT"
# LT = "TOLEFT"
# RF = "FROMRIGHT"
# RT = "TORIGHT"

# Parsing strings
# --------------------------------------------------------------------------------------------------------------------------------
# Get the first N characters in a string: val[:N], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


#                                        Check centerline layer for required fields, add them if necessary
# --------------------------------------------------------------------------------------------------------
if not FieldExists(fields1, "PCONST"):
	CreateTextField(FL1, "PCONST", "4")
	msg("  Range Parity Constant [PCONST] field didn't exist. Field created.")
	
if not FieldExists(fields1, "RNG_LOW"):
	CreateLongField(FL1, "RNG_LOW")
	msg("  Low Range [RNG_LOW] fild didn't exist. Field created.")
	
if not FieldExists(fields1, "RNG_HIGH"):
	CreateLongField(FL1, "RNG_HIGH")
	msg("  High Range [RNG_HIGH] field didn't exist. Field created.")
	


#                                                                  Create and write Range Parity Constants
# --------------------------------------------------------------------------------------------------------
msg("\nUpdating Range Parity Constants")
cur, feat = None, None
cur = arcpy.UpdateCursor(FL1)
for feat in cur:
	vLF = float(feat.getValue(LF))
	vLT = float(feat.getValue(LT))
	vRF = float(feat.getValue(RF))
	vRT = float(feat.getValue(RT))
	feat.PCONST = CalculatePCONST(vLF, vLT, vRF, vRT)	
	cur.updateRow(feat)
	

#                                                                                  Writing LOW/HIGH values
# --------------------------------------------------------------------------------------------------------
msg("Updating/Calculating LOW and HIGH fields")
cur, feat = None, None
cur = arcpy.UpdateCursor(FL1)	
for feat in cur:
    pc = feat.getValue("PCONST")
    pcl = pc[:2]
    pcr = pc[-2:]
    vLF = float(feat.getValue(LF))
    vLT = float(feat.getValue(LT))
    vRF = float(feat.getValue(RF))
    vRT = float(feat.getValue(RT))
    if pc == "XXXX":
        lw = 0
        hi = 0
    elif pcl != "XX" and pcr == "XX":
        lw = min(vLF, vLT)
        hi = max(vLF, vLT)
    elif pcl == "XX" and pcr != "XX":
        lw = min(vRF, vRT)
        hi = max(vRF, vRT)
    else:
        lw = min(vLF, vLT, vRF, vRT)
        hi = max(vLF, vLT, vRF, vRT)
    feat.RNG_LOW = lw
    feat.RNG_HIGH = hi
    cur.updateRow(feat)
	


	

msg("\n\nDone!\n\n")



