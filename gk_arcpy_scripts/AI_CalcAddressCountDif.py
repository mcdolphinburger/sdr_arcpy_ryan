# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# CalcAddCountDiff.py
# Created on: 2012-02-27
#
#
# Description: 
# ----------------
# This script calculates the difference between the number of available addresses on the left side of
# the road versus the right side of the road, for each road centerline feature. It requires a single
# feature layer input (road centerlines), adds and/or updates the parity constant field as needed, and
# always adds a new field of type Long Integer called ADD_COUNT_DIF to hold the results.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import modules
# ---------------------------
import sys, arcpy, string, datetime


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
	
def CreateLongField(lyr, fname):
	arcpy.AddField_management(lyr, fname, "LONG", "", "", "", fname, "NULLABLE", "NON_REQUIRED", "")
	
def CreateShortField(lyr, fname):
	arcpy.AddField_management(lyr, fname, "SHORT", "", "", "", fname, "NULLABLE", "NON_REQUIRED", "")
	
def CreateDoubleField(lyr, fname):
	arcpy.AddField_management(lyr, fname, "DOUBLE", "", "", "", fname, "NULLABLE", "NON_REQUIRED", "")
	
def CalcPConstant(x1, x2, y1, y2):
	cLF = ""
	cLT = ""
	cRF = ""
	cRT = ""
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
	val = cLF + cLT + cRF + cRT
	
	return val



# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nCalculating Difference in Address Counts")
msg("=========================================\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
FL1 = arcpy.GetParameterAsText(0)					# Road centerline feature layer



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
desc1 = arcpy.Describe(FL1)
fc1 = desc1.FeatureClass
fields1 = fc1.Fields
shapefield = desc1.ShapeFieldName
spref = desc1.spatialReference
LF = "LEFT_FROM"
LT = "LEFT_TO"
RF = "RIGHT_FROM"
RT = "RIGHT_TO"


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

fnam = "PCONST"
if FieldExists(fields1, fnam) == "TRUE":
	msg("Field [" + fnam + "] exists?  TRUE")
else:
	CreateTextField(FL1, fnam,"4")
	msg("Field [" + fnam + "] exists?  FALSE (field created)")

fnam = "ADD_COUNT_DIF"
if FieldExists(fields1, fnam) == "TRUE":
	msg("Field [" + fnam + "] exists?  TRUE")
else:
	CreateLongField(FL1, fnam)
	msg("Field [" + fnam + "] exists?  FALSE (field created)")

	
# Calculate PCONST values.
# --------------------------------------------------------------------------------------------------------------
msg("Updating/Calculating PCONST field . . .")
cur1 = arcpy.UpdateCursor(FL1)
for feat1 in cur1:
	vLF = float(feat1.getValue(LF))
	vLT = float(feat1.getValue(LT))
	vRF = float(feat1.getValue(RF))
	vRT = float(feat1.getValue(RT))
	feat1.PCONST = CalcPConstant(vLF, vLT, vRF, vRT)	
	cur1.updateRow(feat1)


# Calculate Address Count Difference values
# --------------------------------------------------------------------------------------------------------------
msg("Updating/Calculating ADD_COUNT_DIF field . . .")
cur2 = arcpy.UpdateCursor(FL1)
for feat2 in cur2:
	pc = feat2.getValue("PCONST")
	pcl = pc[0:2]
	pcr = pc[2:len(pc)]
	vLF = float(feat2.getValue(LF))
	vLT = float(feat2.getValue(LT))
	vRF = float(feat2.getValue(RF))
	vRT = float(feat2.getValue(RT))	
	if pcl != "XX" and pcr != "XX":
		acl = (abs(vLT - vLF)) / 2 + 1
		acr = (abs(vRT - vRF)) / 2 + 1
		add_dif = abs(acl - acr)
	else:
		add_dif = -1
	feat2.ADD_COUNT_DIF = add_dif
	cur2.updateRow(feat2)



msg("\n\n\nDone!\n\n\n")



	




