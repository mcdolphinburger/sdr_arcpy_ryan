# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# RCL_Secondary_Fields.py
# Created on: 2012-02-15
#
#
# Description: 
# ----------------
# Adds a new suite of tools to a road centerline feature class. The fields added are:
#		JOIN_ID
# 	ADD_COUNT_L
#		ADD_COUNT_R
#		TO_ADDRESS
#		LEN_MILES
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


def msg(msg):
	arcpy.AddMessage(msg)

def FieldExists(lyr, fname):
	doesexist = False
	for fld in arcpy.ListFields(lyr):
		if fld.name == fname:
			doesexist = True
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


msg("\n\nAdding Secondary Centerline Fields\n===========================================\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
FL1 = arcpy.GetParameterAsText(0)					# Road centerline feature layer


# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
desc1 = arcpy.Describe(FL1)
shapefield = desc1.ShapeFieldName
spref = desc1.spatialReference
LF = "LEFT_FROM"
LT = "LEFT_TO"
RF = "RIGHT_FROM"
RT = "RIGHT_TO"


# Check centerline layer for fields. Add them if necessary.
# --------------------------------------------------------------------------------------------------------------

fnam = "JOINID"
if FieldExists(FL1, fnam) == True:
	msg("Field [" + fnam + "] exists?  TRUE")
else:
	CreateLongField(FL1, fnam)
	msg("Field [" + fnam + "] exists?  FALSE (field created)")
	
fnam = "ADD_COUNT_L"
if FieldExists(FL1, fnam) == True:
	msg("Field [" + fnam + "] exists?  TRUE")
else:
	CreateLongField(FL1, fnam)
	msg("Field [" + fnam + "] exists?  FALSE (field created)")
	
fnam = "ADD_COUNT_R"
if FieldExists(FL1, fnam) == True:
	msg("Field [" + fnam + "] exists?  TRUE")
else:
	CreateLongField(FL1, fnam)
	msg("Field [" + fnam + "] exists?  FALSE (field created)")
	
fnam = "LEN_MILES"
if FieldExists(FL1, fnam) == True:
	msg("Field [" + fnam + "] exists?  TRUE")
else:
	CreateDoubleField(FL1, fnam)
	msg("Field [" + fnam + "] exists?  FALSE (field created)")

msg("\n\n")	
	
	
# Calculate JOINID values.
# --------------------------------------------------------------------------------------------------------------
msg("Updating/Calculating JOINID field . . .")
cur = arcpy.UpdateCursor(FL1)
for feat in cur:
	feat.JOINID = feat.getValue("OBJECTID")
	cur.updateRow(feat)
del cur, feat
	

# Calculate Address Counts Left and Right.
# --------------------------------------------------------------------------------------------------------------
msg("Updating/Calculating ADDRESS_COUNT_L and ADDRESS_COUNT_R fields . . .")
cur = arcpy.UpdateCursor(FL1)	
for feat in cur:
	pc = feat.getValue("PCONST")
	pcl = pc[0:2]
	pcr = pc[2:len(pc)]
	vLF = float(feat.getValue(LF))
	vLT = float(feat.getValue(LT))
	vRF = float(feat.getValue(RF))
	vRT = float(feat.getValue(RT))	
	if pc == "XXXX":
		acl = 0
		acr = 0
	elif pcl != "XX" and pcr == "XX":
		acl = (abs(vLT - vLF)) / 2 + 1
		acr = 0
	elif pcl == "XX" and pcr != "XX":
		acr = (abs(vRT - vRF)) / 2 + 1
		acl = 0
	else:
		acl = (abs(vLT - vLF)) / 2 + 1
		acr = (abs(vRT - vRF)) / 2 + 1
	feat.ADD_COUNT_L = acl
	feat.ADD_COUNT_R = acr
	cur.updateRow(feat)
del cur, feat
	
	
# Calculate LEN_MILES values.
# --------------------------------------------------------------------------------------------------------------
msg("Updating/Calculating LEN_MILES field . . .")
if spref.type != "Projected":
	msg("    Data is not projected, stopped calculating.")
else:
	units = spref.linearUnitName
	cur = arcpy.UpdateCursor(FL1)	
	for row in cur:
		# 1 meter = 0.000621371192 miles
		feat = row.getValue(shapefield)
		d = feat.length
		if units == "Meter":
			ln = d * 0.000621371192
		elif units == "Feet":
			ln = d / 5280
		elif units == "Foot_US":
			ln = d / 5280
		else:
			ln = 0
		row.LEN_MILES = ln
		cur.updateRow(row)
del cur, row, feat





arcpy.AddMessage("\n\nDone!\n\n")



