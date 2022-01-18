
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: adds2roads.py
Created: 20161212
Modified: 20181107
About: Compares full address values from a point layer to a centerline layer and determines
       if the address is centerline-valid.

"""




# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)


def FieldExists(fds, fnam):
	fnam = fnam.upper()
	for fld in fds:
		if fld.name.upper() == fnam:
			return True
	return False

def BuildWhereClause(lyr, fld, val):
	fc = arcpy.Describe(lyr).featureClass
	if ".gdb" in fc.path or ".shp" in fc.path:
		if is_number(val):
			wc = "\"" + fld + "\" = " + str(val)
		else:
			wc = "\"" + fld + "\" = '" + val + "'"
	elif is_number(val):
		wc = "[" + fld + "] = " + str(val)
	else:
		wc = "[" + fld + "] = '" + val + "'"
	return wc

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
	return False


# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value
"""
a = House Number / Structure Number
p = Parity Constant
r1 = Left Low
r2 = Left High
r3 = Right Low
r4 = Right High
"""
def GetLowHi(a, p, r1, r2, r3, r4):
	pL = p[:2]
	pR = p[-2:]
	if a % 2 == 0:
		aP = "E"
	else:
		aP = "D"
	if p == "XXXX":
		return 0, 0
	elif (pL != "EE" and pL != "OO" and pL != "XX") or (pR != "EE" and pR != "OO" and pR != "XX"):
		return min(r1, r2, r3, r4), max(r1, r2, r3, r4)
	elif (aP == "E" and pL == "EE") or (aP == "D" and pL == "OO"):
		return r1, r2
	elif (aP == "E" and pR == "EE") or (aP == "D" and pR == "OO"):
		return r3, r4
	else:
		return -1, -1
	
	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrA = arcpy.GetParameterAsText(0)			# Address Point Layer; the layer getting results written to
lyrR = arcpy.GetParameterAsText(1)			# Street Centerline Layer; the layer the Address Points are being compared to
bolComm = arcpy.GetParameter(2)				# Boolean on whether or not to use community values in the compare


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fdsA = arcpy.ListFields(lyrA)

# Street Centerline variables
pconstfld = "PCONST"
fullstreetfieldR = "COMP_STR_NAME"
lffld = "LEFT_FROM"
ltfld = "LEFT_TO"
rffld = "RIGHT_FROM"
rtfld = "RIGHT_TO"
if bolComm:
	comLfld = "E911_COMM_L"
	comRfld = "E911_COMM_R"
	# comLfld = "COMM_L"
	# comRfld = "COMM_R"
	cursorfieldsR = [pconstfld, fullstreetfieldR, lffld, ltfld, rffld, rtfld, comLfld, comRfld]
else:
	cursorfieldsR = [pconstfld, fullstreetfieldR, lffld, ltfld, rffld, rtfld]


# Address Point variables
fullstreetfieldA = "COMP_STR_NAME"
housenumfield = "STRUCTURE_NUM"
resultfield = "ADD_CHECK"
if bolComm:
	#commfield = "COMMUNITY"
	commfield = "E911_COMM"
	cursorfieldsA = [fullstreetfieldA, housenumfield, resultfield, commfield]
else:
	cursorfieldsA = [fullstreetfieldA, housenumfield, resultfield]




# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\nComparing Address Points to Street Centerlines\n")
msg("     Address Points Layer: " + lyrA)
msg("  Street Centerline Layer: " + lyrR + "\n\n")



## ==============================================================================================================
##                                                                                        D O   T H E   W O R K
## ==============================================================================================================

# Add the result field, if necessary
# -------------------------------------------------------------------------------------------------------------	
if not FieldExists(fdsA, "ADD_CHECK"):
	msg("Result field missing, adding it now.\n")
	arcpy.AddField_management(lyrA, "ADD_CHECK", "TEXT", "", "", "50", "ADD_CHECK", "NULLABLE", "NON_REQUIRED", "")



# Begin the compare process
# ---------------------------------------------------------------------------------------------------------------		

# Build street name dictionaries for both address points and centerlines
try:

	msg("Building Street Centerline street name dictionary")
	row, cur = None, None
	streetdicR = {}
	with arcpy.da.SearchCursor(lyrR, fullstreetfieldR) as cur:
		for row in cur:
			if not row[0] in streetdicR:
				streetdicR[row[0]] = row[0]
	#msg(str(len(streetdicR)))
	
	msg("Building Address Point street name dictionary")
	row, cur = None, None
	streetdicA = {}
	with arcpy.da.SearchCursor(lyrA, fullstreetfieldA) as cur:
		for row in cur:
			if not row[0] in streetdicA:
				streetdicA[row[0]] = row[0]
	#msg(str(len(streetdicA)))

except Exception as e:
    msg("\nThere was an error building the street name dictionaries.")
    msg("\n  Error message:\n  " + str(e))
    row, cur = None, None


# Check for zero addresses and road name mismatches
try:
	#cursorfieldsA = [fullstreetfieldA, housenumfield, resultfield, commfield]
	#cursorfieldsA = [fullstreetfieldA, housenumfield, resultfield]
	msg("\nPASS 1 of 2: Checking for zero House Numbers and Street Name mismatches")
	with arcpy.da.UpdateCursor(lyrA, cursorfieldsA) as cur:
		for row in cur:
			if row[1] == 0 and not row[0] in streetdicR:
				row[2] = "Fail: Name/Zero Add"	
			elif row[1] == 0 and row[0] in streetdicR:
				row[2] = "Fail: Zero Add"
			elif row[1] != 0 and not row[0] in streetdicR:
				row[2] = "Fail: Name"
			else:
				row[2] = "ok"
			cur.updateRow(row)

except Exception as e:
    msg("\n**********************************************************************************")
    msg("There was an error checking for zero addresses and name mismatches.")
    msg("Error message:\n  " + str(e))
    msg("**********************************************************************************\n")

	
# Check for out of range addresses
#try:
#cursorfieldsR = [pconstfld, fullstreetfieldR, lffld, ltfld, rffld, rtfld, comLfld, comRfld]
#cursorfieldsR = [pconstfld, fullstreetfieldR, lffld, ltfld, rffld, rtfld]
#cursorfieldsA = [fullstreetfieldA, housenumfield, resultfield, commfield]
#cursorfieldsA = [fullstreetfieldA, housenumfield, resultfield]
msg("PASS 2 of 2: Checking for out of range addresses")
expr = BuildWhereClause(lyrA, resultfield, "ok")
cur = arcpy.da.UpdateCursor(lyrA, cursorfieldsA, expr)
for row in cur:
	n = row[0]
	a = row[1]
	flag = False
	curR = arcpy.da.SearchCursor(lyrR, cursorfieldsR)
	for rowR in curR:
		nr = rowR[1]
		lw, hi = GetLowHi(a, rowR[0], rowR[2], rowR[3], rowR[4], rowR[5])
		if n == nr and a >= lw and a <= hi:
			flag = True
			row[2] = "Pass"
			break
	if flag == False:
		row[2] = "Fail: OOR"
	cur.updateRow(row)
		

cur, row, curR, rowR = None, None, None, None

# except Exception as e:
    # msg("\n**********************************************************************************")
    # msg("There was an error checking for out of range addresses.")
    # msg("Error message:\n  " + str(e))
    # msg("**********************************************************************************\n")
    # curlistR = None
    



msg("\n\nDone!\n\n")

