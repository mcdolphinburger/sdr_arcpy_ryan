

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: globalids_flagdupes.py
Created: 20200130
Modified: 20200130
About: Flags duplicate Global ID values by creating a field and adding attributes that mark any Global ID that appears more than once.

NOTES:

"""

# Import modules
# ---------------------------
import arcpy, sys, string, datetime


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
	
def FieldExists(fields, fname):
	for fld in fields:
		if fld.name == fname:
			return True
			break
	return False
			

	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================


# TEXT —Names or other textual qualities.
# FLOAT —Numeric values with fractional values within a specific range.
# DOUBLE —Numeric values with fractional values within a specific range.
# SHORT —Numeric values without fractional values within a specific range; coded values.
# LONG —Numeric values without fractional values within a specific range.
# DATE —Date and/or Time.
# BLOB —Images or other multimedia.
# RASTER —Raster images.
# GUID —GUID values

# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value	
	
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
fld = arcpy.GetParameterAsText(1)
resfld = arcpy.GetParameterAsText(2)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nChecking field " + fld + " for duplicate values.\n")


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Check for existence of results field. Create it, if necessary.
if not FieldExists(arcpy.ListFields(lyr), resfld):
	arcpy.AddField_management(lyr, resfld, "TEXT", "", "", "10", resfld, "NULLABLE", "NON_REQUIRED", "")

# Cursor on just the field to check for dupes.
cur = arcpy.da.SearchCursor(lyr, [fld])

# Dump all ID values into a list.
GIDs = []
for row in cur:
	GIDs.append(row[0])

# clear the cursor, then check for how many of a specific id appears in the list. If greater than 1, it's a dupe.	
cur, row = None, None
cur = arcpy.da.UpdateCursor(lyr, [fld, resfld])
for row in cur:
	if GIDs.count(row[0]) > 1:
		row[1] = "DUP"
	else:
		row[1] = "ok"
	cur.updateRow(row)

	
msg("\n\nDone!\n\n")



	




