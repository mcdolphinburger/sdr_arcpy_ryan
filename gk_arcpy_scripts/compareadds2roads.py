
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
	
	
def CalculateFullStreetName(rw, nameslist):
	nam = ""
	for s in nameslist:
		i = nameslist.index(s)
		n = rw[i].strip()
		nam = (nam + " " + n).strip()
	return nam

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

#bolComm = False


# Street Centerline variables
fdsR = arcpy.ListFields(lyrR)
fcR = arcpy.Describe(lyrR).featureClass
if FieldExists(fdsR, "PRE_TYPE"):
    streetnamefieldsR = ["PRE_DIR", "PRE_TYPE", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME"]
else:
    streetnamefieldsR = ["PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME"]

cursorfieldsR = streetnamefieldsR
fullstreetfieldR = "COMP_STR_NAME"
pconstfld = "PCONST"
rnglowfld = "RNG_LOW"
rnghifld = "RNG_HIGH"
l_commfield = "COMM_L"
r_commfield = "COMM_R"


# Address Point variables
fdsA = arcpy.ListFields(lyrA)
fcA = arcpy.Describe(lyrA).featureClass
if FieldExists(fdsA, "PRE_TYPE"):
    streetnamefieldsA = ["PRE_DIR", "PRE_TYPE", "STREET_NAME", "STREET_TYPE", "POST_DIR"]    
else:
    streetnamefieldsA = ["PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR"]

streetnamefieldsA.append("COMP_STR_NAME")
cursorfieldsA = streetnamefieldsA
housenumfield = "STRUCTURE_NUM"
resultfield = "ADD_CHECK"
fullstreetfieldA = "COMP_STR_NAME"
commfield = "COMMUNITY"







# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\nComparing Address Points to Street Centerlines\n")
msg("     Address Points Layer: " + lyrA)
msg("  Street Centerline Layer: " + lyrR + "\n\n")



## ==============================================================================================================
##                                                                                        D O   T H E   W O R K
## ==============================================================================================================


# Begin the compare process
# ---------------------------------------------------------------------------------------------------------------		

# Check for results field, create it if necessary
if not FieldExists(fdsA, resultfield):
	msg("Creating results field " + resultfield)
	arcpy.AddField_management(lyrA, resultfield, "TEXT", "", "", "50", resultfield, "NULLABLE", "NON_REQUIRED", "")
	
	
	
# Build street name dictionaries for both address points and centerlines
try:
	
	msg("Building Address Point street name dictionary")
	row, cur = None, None
	streetdicA = {}
	with arcpy.da.SearchCursor(lyrA, fullstreetfieldA) as cur:
		for row in cur:
			if not row[0] in streetdicA:
				streetdicA[row[0]] = row[0]
	#msg(str(len(streetdicA)))

	msg("Building Street Centerline street name dictionary")
	row, cur = None, None
	streetdicR = {}
	with arcpy.da.SearchCursor(lyrR, fullstreetfieldR) as cur:
		for row in cur:
			if not row[0] in streetdicR:
				streetdicR[row[0]] = row[0]
	#msg(str(len(streetdicR)))


except Exception as e:
    msg("\nThere was an error building the street name dictionaries.")
    msg("\n  Error message:\n  " + str(e))
    row, cur = None, None


# Check for zero addresses and road name mismatches
try:
	msg("\nPASS 1 of 2: Checking for zero House Numbers and Street Name mismatches")
	curlistA = []
	curlistA.append(housenumfield)
	curlistA.append(fullstreetfieldA)
	curlistA.append(resultfield)
	with arcpy.da.UpdateCursor(lyrA, curlistA) as cur:
		for row in cur:
			if row[0] == 0 and row[1] in streetdicR:
				row[2] = "Fail: Zero Add"
			elif row[0] != 0 and not row[1] in streetdicR:
				row[2] = "Fail: Name"
			elif row[0] == 0 and not row[1] in streetdicR:
				row[2] = "Fail: Name/Zero Add"	
			else:
				row[2] = "ok"
			cur.updateRow(row)

	curlist = None

except Exception as e:
    msg("\n**********************************************************************************")
    msg("There was an error checking for zero addresses and name mismatches.")
    msg("Error message:\n  " + str(e))
    msg("**********************************************************************************\n\n")
    curlistA = None
	
	
try:
	msg("PASS 2 of 2: Checking for out of range addresses")
	curlistR = []
	curlistR.append(fullstreetfieldR)
	curlistR.append(rnglowfld)
	curlistR.append(rnghifld)
	expr = BuildWhereClause(lyrA, resultfield, "ok")
	cur = arcpy.da.UpdateCursor(lyrA, curlistA, expr)
	for row in cur:
		a = row[0]
		n = row[1]
		flag = False
		curR = arcpy.da.SearchCursor(lyrR, curlistR)
		for rowR in curR:
			na = rowR[0]
			lw = rowR[1]
			hi = rowR[2]
			if n == na and a >= lw and a <= hi:
				res = "Pass"
				flag = True
		if flag == False:
			res = "Fail: Out of Range"
		row[2] = res
		cur.updateRow(row)

	cur, row, curR, rowR = None, None, None, None

except Exception as e:
    msg("\n**********************************************************************************")
    msg("There was an error checking for out of range addresses.")
    msg("Error message:\n  " + str(e))
    msg("**********************************************************************************\n")
    curlistR = None
    



msg("\n\nDone!\n\n")

