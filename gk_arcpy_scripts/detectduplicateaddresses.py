
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

# check for results field, calculate default values
# dump all addresses into a dictionary



"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: dtectduplicateaddresses.py
Created: 20170223
Modified: 20170418
About: Detects duplicate addresses and flags them in the attribute table.

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
resfield = "DUPADD_CHK"

curfds = []
curfds.append(OIDFieldName)
curfds.append(resfield)
curfds.append("FULL_ADDRESS")



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n========================================================")
msg("Scanning for Duplicate Addresses.")
msg("========================================================\n\n")


# ==============================================================================================================
#                                                                                        D O   T H E   W O R K
# ==============================================================================================================

arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")


# Check for existence of results field. If found, calc default values. If not found, create it
# and then calc the default values.
# -------------------------------------------------------------------------------------------------------------	
msg("Validating and setting up the result field.")

try:

	if FieldExists(fds, resfield):
		msg("  The field " + resfield + " already exists? True.")
		msg("  Calculating default value.\n")
		arcpy.CalculateField_management(lyr, resfield, "\"--\"", "PYTHON", "")
	else:
		arcpy.AddField_management(lyr, resfield, "TEXT", "", "", "50", resfield, "NULLABLE", "NON_REQUIRED", "")
		msg("  The field " + resfield + " already exists? False, created field.")
		msg("  Calculating default value.\n")
		arcpy.CalculateField_management(lyr, resfield, "\"--\"", "PYTHON", "")
	
except Exception as e:
	msg("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	msg("There was an error establishing default result values.")
	msg("Error message:\n\n" + str(e))	
	msg("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	
	
# Dump all addresses into a dictionary	
# -------------------------------------------------------------------------------------------------------------	
msg("Dumping all full address values into a dictionary.")
dictAdds = {}

try:

	row, cur = None, None
	cur = arcpy.da.SearchCursor(lyr, "FULL_ADDRESS")
	for row in cur:
		a = row[0]
		if len(a) > 1:
			dictAdds[a] = a

except Exception as e:
	row, cur = None, None
	msg("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	msg("There was an error building the address dictionary.")
	msg("Error message:\n" + str(e))	
	msg("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	
	
	
# Detect and flag duplicate addresses
# -------------------------------------------------------------------------------------------------------------	
msg("Flagging duplicate addresses.")

try:

	j = 0
	cur = arcpy.da.UpdateCursor(lyr, curfds)
	msg(str(len(dictAdds)))
	for i in dictAdds:
		wc = "FULL_ADDRESS = '" + i + "'"
		arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", wc)
		if GetSelectionCount(lyr) > 1:
			j = j + 1
			msg("  " + i)
			arcpy.CalculateField_management(lyr, "DUPADD_CHK", "\"DUP: " + str(j) + "\"", "VB", "")

except Exception as e:
	arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
	row, cur = None, None
	msg("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	msg("There was an error detecting and flagging duplicate addresses.")
	msg("Error message:\n\n" + str(e))	
	msg("~~~~~~~~~~~~~~~~~~~~~~~~~~~")





	




