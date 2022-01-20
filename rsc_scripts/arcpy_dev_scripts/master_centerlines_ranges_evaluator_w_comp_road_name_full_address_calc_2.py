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
    
def FieldExistsAlpha(lyrR, fname):
	for fld in arcpy.ListFields(lyrR):
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

def CreateTextField(lyrR, fname, len):
	arcpy.AddField_management(lyr, fname, "TEXT", "", "", len, fname, "NULLABLE", "NON_REQUIRED", "")
	
def CreateLongField(lyrR, fname):
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

def CalculateRoadName(rn1, rn2, rn3, rn4, rn5):
    rn = (rn1 + " " + rn2).strip()
    rn = (rn + " " + rn3).strip()
    rn = (rn + " " + rn4).strip()
    rn = (rn + " " + rn5).strip()
    return rn


#                                                                                        Script arguments
# -------------------------------------------------------------------------------------------------------
lyrR = arcpy.GetParameterAsText(0)
lyrA = arcpy.GetParameterAsText(1)
LF = arcpy.GetParameterAsText(2)
LT = arcpy.GetParameterAsText(3)
RF = arcpy.GetParameterAsText(4)
RT = arcpy.GetParameterAsText(5)
fldRES = arcpy.GetParameterAsText(6)
fldREZ = arcpy.GetParameterAsText(7)
pL = arcpy.GetParameterAsText(8)
pR = arcpy.GetParameterAsText(9)
doPRT = arcpy.GetParameter(10)


#                                                                               Initialize some variables
# -------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyrR)
cursorfields = ["PCONST", "RNG_EVAL1", LF, LT, RF, RT, "RNG_LOW", "RNG_HIGH"]
desc = arcpy.Describe(lyrR)
fc = desc.FeatureClass
fds = arcpy.ListFields(lyrR)


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
	CreateTextField(lyrR, "PCONST", "4")
	msg("             Range Parity Constant [PCONST] exists?  FALSE (field created)")
else:
	msg("             Range Parity Constant [PCONST] exists?  TRUE")
    
if not FieldExists(fields, "RNG_EVAL1"):
	CreateTextField(lyrR, "RNG_EVAL1", "4")
	msg("Range Evaluation Constant field [RNG_EVAL1] exists?  FALSE (field created)")
else:
	msg("Range Evaluation Constant field [RNG_EVAL1] exists?  TRUE")
    
if not FieldExists(fields, "RNG_LOW"):
	CreateLongField(lyrR, "RNG_LOW")
	msg("                        Low Range [RNG_LOW] exists?  FALSE (field created)")
else:
	msg("                        Low Range [RNG_LOW] exists?  TRUE")
	
if not FieldExists(fields, "RNG_HIGH"):
	CreateLongField(lyrR, "RNG_HIGH")
	msg("                      High Range [RNG_HIGH] exists?  FALSE (field created)")
else:
	msg("                      High Range [RNG_HIGH] exists?  TRUE")
	

#                                                                  Create and write Range Parity Constants
# --------------------------------------------------------------------------------------------------------
msg("\nUpdating Range Parity Constants and Range Evaluation Constants...")
cur, row = None, None
cur = arcpy.da.UpdateCursor(lyrR, cursorfields)
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
cur = arcpy.da.UpdateCursor(lyrR, cursorfields)	
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

if FieldExistsAlpha(lyrR, fldRES):
	msg("Field " + fldRES + " exists?  TRUE\n")
else:
	arcpy.AddField_management(lyrR, fldRES, "TEXT", "", "", "16", fldRES, "NULLABLE", "NON_REQUIRED", "")
	msg("Field " + fldRES + " exists?  FALSE. Field was created.\n")

with arcpy.da.UpdateCursor(lyrR, [LF,LT,RF,RT,fldRES]) as cur:
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

if FieldExistsAlpha(lyrR, fldREZ):
	msg("Field " + fldREZ + " exists?  TRUE\n")
else:
	arcpy.AddField_management(lyrR, fldREZ, "TEXT", "", "", "16", fldREZ, "NULLABLE", "NON_REQUIRED", "")
	msg("Field " + fldREZ + " exists?  FALSE. Field was created.\n")

with arcpy.da.UpdateCursor(lyrR, [LF,LT,RF,RT,fldREZ]) as cur:
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

if FieldExistsAlpha(lyrR, pL):
	msg("\nField " + pL + " exists?  TRUE\n")
else:
	arcpy.AddField_management(lyrR, pL, "TEXT", "", "", "16", pL, "NULLABLE", "NON_REQUIRED", "")
	msg("Field " + pL + " exists?  FALSE. Field was created.\n")
    
if FieldExistsAlpha(lyrR, pR):
	msg("Field " + pR + " exists?  TRUE\n")
else:
	arcpy.AddField_management(lyrR, pR, "TEXT", "", "", "16", pR, "NULLABLE", "NON_REQUIRED", "")
	msg("Field " + pR + " exists?  FALSE. Field was created.\n")


# Introduction message
# -------------------------------------------------------------------------------------------------------------	
msg("\nUpdating left and right parity constants. . .\n")


#                                                                  Create and write Range Parity Constants
# --------------------------------------------------------------------------------------------------------
cursorfields = []
cursorfields.append(LF)
cursorfields.append(LT)
cursorfields.append(RF)
cursorfields.append(RT)
cursorfields.append(pL)
cursorfields.append(pR)


with arcpy.da.UpdateCursor(lyrR, cursorfields) as cur:
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


# ==============================================================================================================
# BLOCK 5: calculate compiled road names, full address values
# ==============================================================================================================


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
if doPRT:
    cursorfieldsR = ["PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME", "PRE_TYPE"]
    cursorfieldsA = ["STRUCTURE_NUM", "PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME", "FULL_ADDRESS", "PRE_TYPE"]
else:
    cursorfieldsR = ["PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME"]
    cursorfieldsA = ["STRUCTURE_NUM", "PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME", "FULL_ADDRESS"]


# Calculating road centerline road name values
# --------------------------------------------------------------------------------------------------------------
msg("\n\nCalculating compiled road names values in road centerlines layer. . .\n")
row, cur = None, None
cur = arcpy.da.UpdateCursor(lyrR, cursorfieldsR)	
for row in cur:
    r1 = row[0].strip()
    if doPRT:
        r2 = row[5].strip()
    else:
        r2 = ""
    r3 = row[1].strip()
    r4 = row[2].strip()
    r5 = row[3].strip()
    rn = CalculateRoadName(r1, r2, r3, r4, r5)
    row[4] = rn
    cur.updateRow(row)
    
msg("\nGreat success! \(^ o ^)/\n")


# POSSIBILITY OF A SUB-BLOCK THAT WRITES ANY CHANGES MADE TO COMPILED ROAD NAMES ABOVE TO ANY CORRESPONDING STREET_NAME AND COMP_STR_NAME VALUES IN ADDRESSES LAYER?

# Calculating address point road names and full addresses
# --------------------------------------------------------------------------------------------------------------
msg("\n\nCalculating road names and full addresses values in addresses layer. . .\n")
row, cur = None, None
cur = arcpy.da.UpdateCursor(lyrA, cursorfieldsA)	
for row in cur:
    a = row[0]
    r1 = row[1].strip()
    if doPRT:
        r2 = row[7].strip()
    else:
        r2 = ""
    r3 = row[2].strip()
    r4 = row[3].strip()
    r5 = row[4].strip()
    rn = CalculateRoadName(r1, r2, r3, r4, r5)
    fa = (str(a) + " " + rn).strip()
    row[5] = rn
    row[6] = fa
    cur.updateRow(row)
    
msg("\nGreat success! \(^ o ^)/\n")

msg("\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n ")