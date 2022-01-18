

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: globalids_addilng911idvalues.py
Created: 202001301
Modified: 20200131
About: Finds the highest or largest used ID number.

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
lyrtyp = arcpy.GetParameterAsText(1)
agencyval = arcpy.GetParameterAsText(2)



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------

# this bit establishes the field the id numbers are in
if lyrtyp == "Centerlines":
	idfld = "RCL_NGUID"
	idkonst = "R"
elif lyrtyp == "Address Points":
	idfld = "Site_NGUID"
	idkonst = "A"
else:
	msg("Unknown Layer Type. Stopping.")
	sys.exit()
	



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if not FieldExists(arcpy.ListFields(lyr), idfld):
	arcpy.AddField_management(lyr, idfld, "TEXT", "", "", "100", idfld, "NULLABLE", "NON_REQUIRED", "")


cur = arcpy.da.UpdateCursor(lyr, idfld)
i = -1
for row in cur:
	i = i + 1
	row[0] = idkonst + str(i).rjust(6, '0') + agencyval
	cur.updateRow(row)





msg("\n\nDone!\n\n")



	




