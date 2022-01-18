"""
Author: Ryan Saul Cunningham
Email: rcunningham@sdrmaps
Tool: master_centerlines_ranges_evaluator_1.py
Created: 2012-09-08
Modified: 2022-01-11
About: Master road centerlines properties evaluation script: calculates low and high range values, parity constant, ranges evalution constant, reversed ranges constant, offset ranges constant. 
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
    
def FieldExistsAlpha(lyr, fname):
	for fld in arcpy.ListFields(lyr):
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
LF = arcpy.GetParameterAsText(1)
LT = arcpy.GetParameterAsText(2)
RF = arcpy.GetParameterAsText(3)
RT = arcpy.GetParameterAsText(4)
fldRES = arcpy.GetParameterAsText(5)
fldREZ = arcpy.GetParameterAsText(6)


#                                                                               Initialize some variables
# -------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)
cursorfields = []
cursorfields = ["PCONST", "RNG_EVAL1", LF, LT, RF, RT, "RNG_LOW", "RNG_HIGH"]

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
    #msg(v)
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
    
#del row, cur
	

#                                                                                  Writing LOW/HIGH values
# --------------------------------------------------------------------------------------------------------
arcpy.AddMessage("Updating/Calculating LOW and HIGH fields...\n")
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

#del row, cur
	
msg("\nGreat success! \(^ o ^)/\n")

	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
# LF = "LEFT_FROM"
# LT = "LEFT_TO"
# RF = "RIGHT_FROM"
# RT = "RIGHT_TO"



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
#msg("\n\nEvaluating layer \"" + lyr + " for reversed ranges\n")
#msg("\n\nLooking for reversed ranges\n\n")
msg("\n\nUpdating reversed ranges constant. . .\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if FieldExistsAlpha(lyr, fldRES):
	msg("Field " + fldRES + " exists?  TRUE\n")
else:
	arcpy.AddField_management(lyr, fldRES, "TEXT", "", "", "16", fldRES, "NULLABLE", "NON_REQUIRED", "")
	msg("Field " + fldRES + " exists?  FALSE. Field was created.\n")

with arcpy.da.UpdateCursor(lyr, [LF,LT,RF,RT,fldRES]) as cur:
	for row in cur:
		vLF = row[0]
		vLT = row[1]
		vRF = row[2]
		vRT = row[3]
		dL = vLT - vLF							# delta Left
		dR = vRT - vRF							# delta Right
		# Left range evaluation.
		#   X : Left From and Left To both equal 0
		#   S : Left From and Left To are equal.
		#   > : Left From is less than Left To.
		#   < : Left From is greater than Left To.
		if vLF == 0 and vLT == 0:
			res1 = "X"
		elif dL == 0:
			res1 = "S"
		elif dL > 0:
			res1 = ">"
		else:
			res1 = "<"
		
		# Right range evaluation.
		#   X : Right From and Right To both equal 0
		#   S : Right From and Right To are equal.
		#   > : Right From is less than Right To.
		#   < : Right From is greater than Right To.
		if vRF == 0 and vRT == 0:
			res2 = "X"
		elif dR == 0:
			res2 = "S"
		elif dR > 0:
			res2 = ">"
		else:
			res2 = "<"

		row[4] = res1 + res2
		cur.updateRow(row)

del row, cur

msg("\nGreat success! \(^ o ^)/\n")

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
# msg("\n\nEvaluating layer \"" + lyr + " for offset ranges\n")
# msg("\n\nLooking for offset ranges\n\n")
msg("\n\nUpdating offset ranges constant. . .\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if FieldExistsAlpha(lyr, fldREZ):
	msg("Field " + fldREZ + " exists?  TRUE\n")
else:
	arcpy.AddField_management(lyr, fldREZ, "TEXT", "", "", "16", fldREZ, "NULLABLE", "NON_REQUIRED", "")
	msg("Field " + fldREZ + " exists?  FALSE. Field was created.\n")

with arcpy.da.UpdateCursor(lyr, [LF,LT,RF,RT,fldREZ]) as cur:
	for row in cur:
		vLF = row[0]
		vLT = row[1]
		vRF = row[2]
		vRT = row[3]
		
		if vLF == 0 or vRF == 0:
			rez1 = "X"
		else:
			rez1 = str(abs(vLF - vRF))
			
		if vLT == 0 or vRT == 0:
			rez2 = "X"
		else:
			rez2 = str(abs(vLT - vRT))
			

		row[4] = rez1 + ":" + rez2
		cur.updateRow(row)

del row, cur

msg("\nGreat success! \(^ o ^)/\n")

msg("\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n ")