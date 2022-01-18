# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# AI_CompareStreetNames.py
# Created on: 2013-05-06
#
#
# Description: 
# ----------------
#  
# 
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(lyr, fname):
	doesexist = False
	for fld in arcpy.ListFields(lyr):
		if fld.name == fname:
			doesexist = True
	return doesexist
	
#	Receives: layer object
#	 Returns: string indicating the kind of workspace of the input layer
#	---------------------------------------------------------------------------------
def GetWorkspaceType(lyr):
	ds = arcpy.Describe(lyr)
	if (ds.dataElement.dataType) == "ShapeFile":
		work = "shape"
	elif (ds.dataElement.dataType) == "FeatureClass":
		p = ds.dataElement.catalogPath
		if ".mdb" in p:
			work = "pers"
		else:
			work = "file"
	else:
		work = "unk"
	return work

def CalcStreetName(n, r):
	if n == 1:
		s = ""
		if rn11:
			s1 = r.getValue(rn11)
		else:
			s1 = ""
		if rn12:
			s2 = r.getValue(rn12)
		else:
			s2 = ""
		s3 = r.getValue(rn13)
		if rn14:
			s4 = r.getValue(rn14)
		else:
			s4 = ""
		if rn15:
			s5 = r.getValue(rn15)
		else:
			s5 = ""
		s = (s1 + " " + s2).strip()
		s = (s + " " + s3).strip()
		s = (s + " " + s4).strip()
		s = (s + " " + s5).strip()
		return s
	else:
		s = ""
		if rn21:
			s1 = r.getValue(rn21)
		else:
			s1 = ""
		if rn22:
			s2 = r.getValue(rn22)
		else:
			s2 = ""
		s3 = r.getValue(rn23)
		if rn24:
			s4 = r.getValue(rn24)
		else:
			s4 = ""
		if rn25:
			s5 = r.getValue(rn25)
		else:
			s5 = ""
		s = (s1 + " " + s2).strip()
		s = (s + " " + s3).strip()
		s = (s + " " + s4).strip()
		s = (s + " " + s5).strip()
		return s	






# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr1 = arcpy.GetParameterAsText(0)				# a layer with road names to compare
lyr2 = arcpy.GetParameterAsText(1)				# another layer with road names to compare
schema = arcpy.GetParameterAsText(2)			# a value indicating which schema to use

rn11 = arcpy.GetParameterAsText(3)			  	# Field containing pre directional values for the first layer
rn12 = arcpy.GetParameterAsText(4)			  	# Field containing pre type values for the first layer
rn13 = arcpy.GetParameterAsText(5)			  	# Field containing street name values for the first layer
rn14 = arcpy.GetParameterAsText(6)			  	# Field containing street type values for the first layer
rn15 = arcpy.GetParameterAsText(7)			  	# Field containing post directional values for the first layer

rn21 = arcpy.GetParameterAsText(8)			  	# Field containing pre directional values for the second layer
rn22 = arcpy.GetParameterAsText(9)			  	# Field containing pre type values for the second layer
rn23 = arcpy.GetParameterAsText(10)			  	# Field containing street name values for the second layer
rn24 = arcpy.GetParameterAsText(11)			  	# Field containing street type values for the second layer
rn25 = arcpy.GetParameterAsText(12)			  	# Field containing post directional values for the second layer



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------




# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nComparing street names for layers:\n")
msg("  " + lyr1 + "\n  " + lyr2 + "\n\n")





# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Verify that the field exists for holding the compare results for each layer.
# If the doesn't exist, create it.
# -------------------------------------------------------------------------------------
if FieldExists(lyr1, "RNC"):
	msg("Field RNC exists in layer 1? TRUE")
else:
	arcpy.AddField_management(lyr1, "RNC", "TEXT", "", "", "64", "RNC", "NULLABLE", "NON_REQUIRED", "")
	msg("Field RNC exists in layer 1? FALSE, field created")	
	
if FieldExists(lyr2, "RNC"):
	msg("Field RNC exists in layer 2? TRUE\n")
else:
	arcpy.AddField_management(lyr2, "RNC", "TEXT", "", "", "64", "RNC", "NULLABLE", "NON_REQUIRED", "")
	msg("Field RNC exists in layer 2? FALSE, field created\n")

# Create a road name dictionary for layer 1
# -------------------------------------------------------------------------------------	
msg("Creating Street Name dictionary for layer 1.")
dic1 = {}
row, cur = None, None
cur = arcpy.SearchCursor(lyr1)
for row in cur:
	sn = CalcStreetName(1, row)
	dic1[sn] = sn

# Create a road name dictionary for layer 2
# -------------------------------------------------------------------------------------
msg("Creating Street Name dictionary for layer 2.\n")
dic2 = {}
row, cur = None, None
cur = arcpy.SearchCursor(lyr2)
for row in cur:
	sn = CalcStreetName(2, row)
	dic2[sn] = sn

# Compare road names in layer 1 to layer 2, write results in layer 1
# -------------------------------------------------------------------------------------
msg("Writing Street Name compare results to layer 1.")
cur, row = None, None
cur = arcpy.UpdateCursor(lyr1)
for row in cur:
	sn = CalcStreetName(1, row)
	if not sn in dic2.keys():
		row.setValue("RNC", "NO MATCH")
	else:
		row.setValue("RNC", "GOOD")
	cur.updateRow(row)

# Compare road names in layer 2 to layer 1, write results in layer 2
# -------------------------------------------------------------------------------------	
msg("Writing Street Name compare results to layer 2.")
cur, row = None, None
cur = arcpy.UpdateCursor(lyr2)
for row in cur:
	sn = CalcStreetName(2, row)
	if not sn in dic1.keys():
		row.setValue("RNC", "NO MATCH")
	else:
		row.setValue("RNC", "GOOD")
	cur.updateRow(row)
cur, row = None, None




	


arcpy.AddMessage("\n\nDone!\n\n")



	




