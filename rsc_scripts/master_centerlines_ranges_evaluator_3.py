"""
Author: Ryan Saul Cunningham
Email: rcunningham@sdrmaps
Tool: master_centerlines_ranges_evaluator_1.py
Created: 2012-09-08
Modified: 2022-01-16
About: Master road centerlines properties evaluation script: calculates low and high range values, overall (----) parity constant, ranges evalution constant, reversed ranges constant, offset ranges constant, left and right parity constants.
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
    
def FieldExistsBeta(fds, fname):
	for fld in fds:
		if fld.name.upper() == fname.upper():
			#msg("True!")
			return True
	#msg("False!")
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
    
def GetLRParity(v):
	if v == 0:
		return "Z"
	elif v % 2 == 0:   #if input_num % 2 == 0
		return "E"
	else:
		return "O"


#                                                                                        Script arguments
# -------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
LF = arcpy.GetParameterAsText(1)
LT = arcpy.GetParameterAsText(2)
RF = arcpy.GetParameterAsText(3)
RT = arcpy.GetParameterAsText(4)
fldRES = arcpy.GetParameterAsText(5)
fldREZ = arcpy.GetParameterAsText(6)
pL = arcpy.GetParameterAsText(7)
pR = arcpy.GetParameterAsText(8)


#                                                                               Initialize some variables
# -------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)
cursorfields = ["PCONST", "RNG_EVAL1", LF, LT, RF, RT, "RNG_LOW", "RNG_HIGH"]
desc = arcpy.Describe(lyr)
fc = desc.FeatureClass
fds = arcpy.ListFields(lyr)


# ==============================================================================================================
# BLOCK 1: calculate PCONST, RNG_EVAL1, RNG_LOW and RNG_HIGH
# ==============================================================================================================


#                                                                                               B E G I N
# -------------------------------------------------------------------------------------------------------
arcpy.AddMessage("\n\nUpdating Range Info")
arcpy.AddMessage("=================================" + "\n\n")


#                                        Check centerline layer for required fields, add them if necessary
# --------------------------------------------------------------------------------------------------------
if not FieldExists(fields, "PCONST"):
	CreateTextField(lyr, "PCONST", "4")
	msg("             Range Parity Constant [PCONST] exists?  FALSE (field created)")
else:
	msg("             Range Parity Constant [PCONST] exists?  TRUE")
    
if not FieldExists(fields, "RNG_EVAL1"):
	CreateTextField(lyr, "RNG_EVAL1", "4")
	msg("Range Evaluation Constant field [RNG_EVAL1] exists?  FALSE (field created)")
else:
	msg("Range Evaluation Constant field [RNG_EVAL1] exists?  TRUE")
    
if not FieldExists(fields, "RNG_LOW"):
	CreateLongField(lyr, "RNG_LOW")
	msg("                        Low Range [RNG_LOW] exists?  FALSE (field created)")
else:
	msg("                        Low Range [RNG_LOW] exists?  TRUE")
	
if not FieldExists(fields, "RNG_HIGH"):
	CreateLongField(lyr, "RNG_HIGH")
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
# BLOCK 2: calculate REV_RNG (or desired reversed ranges input) constant
# ==============================================================================================================


# Introduction message
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nUpdating reversed ranges constant. . .\n")

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



# ==============================================================================================================
# BLOCK 3: calculate OFFSET_RNG (or desired offset ranges input) constant
# ==============================================================================================================


# Introduction message
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nUpdating offset ranges constant. . .\n")

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



# ==============================================================================================================
# BLOCK 4: calculate PARITY_L and PARITY_R (or desired left and right parity input) constants
# ==============================================================================================================


# Introduction message
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nUpdating left and right parity constants. . .\n")


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
		pLF = GetLRParity(row[0])
		pLT = GetLRParity(row[1])
		pRF = GetLRParity(row[2])
		pRT = GetLRParity(row[3])
		
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



msg("\nGreat success! \(^ o ^)/\n")

msg("\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n ")