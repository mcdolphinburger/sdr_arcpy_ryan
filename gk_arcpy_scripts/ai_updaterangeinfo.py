
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: AI_CalcRangeLowHigh.py
Created: 20171026
Modified: 20171026
About: Updates range Low/High values, parity constant, and range evaluation constant.

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
		if fld.name == fname:
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

arcpy.AddMessage("\n\nUpdating Range Info")
arcpy.AddMessage("=================================" + "\n\n")


#                                                                                        Script arguments
# -------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
lf = arcpy.GetParameterAsText(1)
lt = arcpy.GetParameterAsText(2)
rf = arcpy.GetParameterAsText(3)
rt = arcpy.GetParameterAsText(4)									



#                                                                               Initialize some variables
# -------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)
cursorfields = []
cursorfields = ["PCONST", "RNG_EVAL1", lf, lt, rf, rt, "RNG_LOW", "RNG_HIGH"]

# Parsing strings
# --------------------------------------------------------------------------------------------------------------------------------
# Get the first N characters in a string: val[:N], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


#                                        Check centerline layer for required fields, add them if necessary
# --------------------------------------------------------------------------------------------------------
if not FieldExists(fields, "PCONST"):
	CreateTextField(FL1, "PCONST", "4")
	msg("             Range Parity Constant [PCONST] exists?  FALSE (field created)")
else:
	msg("             Range Parity Constant [PCONST] exists?  TRUE")
    
if not FieldExists(fields, "RNG_EVAL1"):
	CreateTextField(FL1, "RNG_EVAL1", "4")
	msg("Range Evaluation Constant field [RNG_EVAL1] exists?  FALSE (field created)")
else:
	msg("Range Evaluation Constant field [RNG_EVAL1] exists?  TRUE")
    
if not FieldExists(fields, "RNG_LOW"):
	CreateLongField(FL1, "RNG_LOW")
	msg("                        Low Range [RNG_LOW] exists?  FALSE (field created)")
else:
	msg("                        Low Range [RNG_LOW] exists?  TRUE")
	
if not FieldExists(fields, "RNG_HIGH"):
	CreateLongField(FL1, "RNG_HIGH")
	msg("                      High Range [RNG_HIGH] exists?  FALSE (field created)")
else:
	msg("                      High Range [RNG_HIGH] exists?  TRUE")
	

#                                                                  Create and write Range Parity Constants
# --------------------------------------------------------------------------------------------------------
msg("\nUpdating Range Parity Constants and Range Evaluation Constants...")
cur, row = None, None
cur = arcpy.da.UpdateCursor(lyr, cursorfields)
for row in cur:
    vLF = float(row[2])
    vLT = float(row[3])
    vRF = float(row[4])
    vRT = float(row[5])

    v = CalculatePCONST(vLF, vLT, vRF, vRT)
    msg(v)
    row[0] = v

    dL = vLT - vLF							# delta Left
    dR = vRT - vRF							# delta Right
    dF = abs(vLF - vRF)						# delta From
    dT = abs(vLT - vRT)						# delta To

    # Left range evaluation.
    #   if X: Left From and Left To both equal 0
    #   if 0: Left From and Left To are equal.
    #   if +: Left From is less than Left To.
    #   if -: Left From is greater than Left To.
    if vLF == 0 and vLT == 0:
        res1 = "X"
    elif dL == 0:
        res1 = "0"
    elif dL > 0:
        res1 = "+"
    else:
        res1 = "-"

    # Right range evaluation.
    #   if X: Right From and Right To both equal 0
    #   if 0: Right From and Right To are equal.
    #   if +: Right From is less than Right To.
    #   if -: Right From is greater than Right To.
    if vRF == 0 and vRT == 0:
        res2 = "X"
    elif dR == 0:
        res2 = "0"
    elif dR > 0:
        res2 = "+"
    else:
        res2 = "-"
        
    # From range evaluation.
    #	if X: Right From and Left From both equal 0
    #	if 0: Right From and Left From are equal
    #	if 1: Right From and Left From differ by 1
    #	if +: Right From and Left From differ by more than 1
    if vLF == 0 and vRF == 0:
        res3 = "X"
    elif dF == 0:
        res3 = "0"
    elif dF == 1:
        res3 = "1"
    else:
        res3 = "+"

    # To range evaluation
    #	if X: Right To and Left To both equal 0
    #	if 0: Right To and Left To are equal
    #	if 1: Right To and Left To differ by 1
    #	if +: Right To and Left To differ by more than 1
    if vLT == 0 and vRT == 0:
        res4 = "X"
    elif dT == 0:
        res4 = "0"
    elif dT == 1:
        res4 = "1"
    else:
        res4 = "+"

    row[1] = res1 + res2 + res3 + res4
        
    cur.updateRow(row)
	

#                                                                                  Writing LOW/HIGH values
# --------------------------------------------------------------------------------------------------------
arcpy.AddMessage("Updating/Calculating LOW and HIGH fields...")
cur, row = None, None
cur = arcpy.da.UpdateCursor(lyr, cursorfields)	
for row in cur:
    pc = row[0]
    pcl = pc[:2]
    pcr = pc[-2:]
    vLF = row[2]
    vLT = row[3]
    vRF = row[4]
    vRT = row[5]
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
    row[6] = lw
    row[7] = hi
    cur.updateRow(row)

	

arcpy.AddMessage("\n\nDone!\n\n")



