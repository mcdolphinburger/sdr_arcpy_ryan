
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: dtectduplicategeometry.py
Created: 20140715
Modified: 20160416
About: Detects duplicate geometry and flags them in the attribute table.

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
	
def GetSelectionCount(lyr):
	return int(arcpy.GetCount_management(lyr).getOutput(0))
	
def FieldExists(fields, fname):
	for fld in fields:
		if fld.name == fname:
			return True
	return False


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
d = arcpy.Describe(lyr)
OIDFieldName = d.OIDFieldName
fds = arcpy.ListFields(lyr)
resfield = "DUPGEO_CHK"


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\nScanning for Duplicate Geometry\n")









# ==============================================================================================================
#                                                                                        D O   T H E   W O R K
# ==============================================================================================================

# Arguments: Layer Name or Table View, Selection Type, Expression
# arcpy.SelectLayerByAttribute_management(Layer, "NEW_SELECTION", "[COMP_STR_NAME] = '10TH ST'")

# Arguments: Input Feature Layer, Relationship, Selecting features, Search Distance, Selection type
# arcpy.SelectLayerByLocation_management(Target Layer, "INTERSECT", Selecting Layer, "", "NEW_SELECTION")

# Arguments: input table, field name, expression, expression type, code block
# arcpy.CalculateField_management(Input_Table, Field_Name, Expression, Expression_Type, Code_Block)
# arcpy.CalculateField_management(Addresses__2_, "E911_COMM", "\"xxxx\"", "VB", "")

# Arguments: input table, field name, field type, precision, scale, length, field alias, is nullable, is required, domain
# arcpy.AddField_management(FL1, "RACT", "TEXT", "", "", "32", "RACT", "NULLABLE", "NON_REQUIRED", "")
# arcpy.AddField_management(FL1, "LOW", "LONG", "", "", "", "LOW", "NULLABLE", "NON_REQUIRED", "")
# arcpy.AddField_management(FL1, "LOW", "SHORT", "", "", "", "LOW", "NULLABLE", "NON_REQUIRED", "")


# Check for existence of results field. If found, calc default values. If not found, create it
# and then calc the default values.
# -------------------------------------------------------------------------------------------------------------	
msg("Validating and setting up the result field.")
if FieldExists(fds, resfield):
	msg("  The field " + resfield + " already exists? True.")
	msg("  Calculating default value.\n")
	arcpy.CalculateField_management(lyr, resfield, "\"--\"", "VB", "")
else:
	arcpy.AddField_management(lyr, resfield, "TEXT", "", "", "32", resfield, "NULLABLE", "NON_REQUIRED", "")
	msg("  The field " + resfield + " already exists? False, created field.")
	msg("  Calculating default value.\n")
	arcpy.CalculateField_management(lyr, resfield, "\"--\"", "VB", "")
	
	

	
try:

	cursorfields = []
	cursorfields.append('SHAPE@')
	cursorfields.append(resfield)
	arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
	row, cur = None, None
	resval = "DUP "
	dupcount = 0
	cur = arcpy.SearchCursor(lyr)
	for row in cur:
		res = row.getValue(resfield)
		if res == "--":
			x = row.getValue(OIDFieldName)
			arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "\"" + OIDFieldName + "\" = " + str(x))
			arcpy.SelectLayerByLocation_management(lyr, "ARE_IDENTICAL_TO", lyr, "", "NEW_SELECTION")
			y = GetSelectionCount(lyr)
			if y > 1:
				msg("Object ID: " + str(x) + "        Selection Count: " + str(y))
				dupcount = dupcount + 1
				arcpy.CalculateField_management(lyr, resfield, "\"" + resval + str(dupcount) + "\"", "VB", "")
				arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

	row, cur = None, None
	arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
	msg("\n\nDone!\n\n")
	
except Exception as e:
	row, cur = None, None
	msg("\nThere was an error in the main loop.")
	msg("\nError message:\n\n" + str(e))



	




