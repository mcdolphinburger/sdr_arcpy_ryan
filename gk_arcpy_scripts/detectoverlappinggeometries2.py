
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: detectoverlappinggeometries2.py
Created: 20170518
Modified: xxxxxxxx
About: Detects overlapping geometries and flags overlapping features in the attribute table.

"""




# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


## ==============================================================================================================
##                                                                     F U N C T I O N S / D E F I N I T I O N S
## ==============================================================================================================
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
fds = arcpy.ListFields(lyr)
resfield = "OLAP_GEOCHK"


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\nScanning for Duplicate Geometry\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O R K
# ==============================================================================================================


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
	


while True:
    arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "\"" + resfield + "\" = '--'"))
	ct = GetSelectionCount(lyr)
    if ct < 1:
        break
    

	
try:

	cursorfields = []
	cursorfields = ['OID@', 'SHAPE@', resfield]
	# cursorfields.append('SHAPE@')
	# cursorfields.append(resfield)
	# cursorfields.append('OID@')
	arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
	row, cur = None, None
	olapcount = 0
	cur = arcpy.da.UpdateCursor(lyr, cursorfields)
	for row in cur:
		res = row[2]
		if res == "--":
			resval = "OLAP"
			id = row[0]
			#arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "\"" + OIDFieldName + "\" = " + str(x))
			arcpy.SelectLayerByLocation_management(lyr, "SHARE_A_LINE_SEGMENT_WITH", row[1], "", "NEW_SELECTION")
			ct = GetSelectionCount(lyr)
			if ct > 1:
				msg("Object ID: " + str(id) + "        Selection Count: " + str(ct))
				olapcount = olapcount + 1
				row[2] = resval + "-" + str(ct)
				cur.updateRow(row)

	row, cur = None, None
	arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
	msg("\n\nDone!\n\n")
	
except Exception as e:
	row, cur = None, None
	msg("\nThere was an error in the main loop.")
	msg("\nError message:\n\n" + str(e))



	



	
	
	
	
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




