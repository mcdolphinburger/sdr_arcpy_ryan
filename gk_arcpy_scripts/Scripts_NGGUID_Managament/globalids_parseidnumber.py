

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: globalids_parseidnumber.py
Created: 20200128
Modified: 20200130
About: Parses out the numeric value from the global id into its own numeric field

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
targetlayers = arcpy.GetParameterAsText(0)



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
lyrs = targetlayers.split(";")

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nParsing Numeric Component of Global ID into Numeric Field")
msg("-------------------------------------------------------------------------------\n\n")

# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

for lyr in targetlayers.split(";"):
	if FieldExists(arcpy.ListFields(lyr), "RCL_NGUID"):
		idfld = "RCL_NGUID"
	elif FieldExists(arcpy.ListFields(lyr), "SITE_NGUID"):
		idfld = "Site_NGUID"
	else:
		msg("Invalid Global ID field. Stopping.")
		sys.exit()
	if not FieldExists(arcpy.ListFields(lyr), "GIDNUM"):
		arcpy.AddField_management(lyr, "GIDNUM", "TEXT", "", "", "8", "GIDNUM", "NULLABLE", "NON_REQUIRED", "")
	curfields = [idfld, 'GIDNUM']
	cur = arcpy.da.UpdateCursor(lyr, curfields)	
	for row in cur:
		x = row[0][:row[0].find('@')][1:]
		if not x:
			x = "0"
		row[1] = x.rjust(6, '0')
		cur.updateRow(row)

msg("\n\nDone!\n\n")



	




