

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: globalids_findhighestusednumber.py
Created: 20200130
Modified: 20200130
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


# TEXT �Names or other textual qualities.
# FLOAT �Numeric values with fractional values within a specific range.
# DOUBLE �Numeric values with fractional values within a specific range.
# SHORT �Numeric values without fractional values within a specific range; coded values.
# LONG �Numeric values without fractional values within a specific range.
# DATE �Date and/or Time.
# BLOB �Images or other multimedia.
# RASTER �Raster images.
# GUID �GUID values

# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value	
	
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
targetlayers = arcpy.GetParameterAsText(0)
fld = arcpy.GetParameterAsText(1)
donewids = arcpy.GetParameter(2)




# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
lyrs = targetlayers.split(";")

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

for lyr in lyrs:
	msg("Finding the highest id number used in " + lyr)
	
	# this bit finds the highest id number in use
	cur = arcpy.da.SearchCursor(lyr, fld)	
	maxid = 0
	for row in cur:
		x = row[0]
		if x > maxid:
			maxid = x
	
	msg("\n\nMax ID Number used is: " + str(maxid))
	
	# this bit creates new id numbers for rows that don't have an id number
	if donewids:
		msg("\n\nCreating new id numbers, if needed.")
		cur = arcpy.da.UpdateCursor(lyr, fld)	
		for row in cur:
			if not row[0]:
				maxid = maxid + 1
				row[0] = maxid
				cur.updateRow(row)
					
			


msg("\n\nDone!\n\n")



	




