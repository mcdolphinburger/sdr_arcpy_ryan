# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# gk_CalculateLineSegmentDirection.py
# Created on: 2013-09-09
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
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(lyr, fname):
	for fld in arcpy.ListFields(lyr):
		if fld.name == fname:
			return True
	return False
	
def ComputeDirection(dx, m):
	if dx > 0 and m >= -0.087489 and m <= 0.087489:
		return "E"
	elif dx > 0 and m > 0.087489 and m < 0.8391:
		return "ENE"
	elif dx > 0 and m >= 0.8391 and m <= 1.191754:
		return "NE"
	elif dx > 0 and m > 1.191754 and m < 11.430052:
		return "NNE"
	elif dx > 0 and m >= 11.430052:
		return "N"
	elif dx < 0 and m <= 11.430052:
		return "N"
	elif dx < 0 and m > -11.430052 and m < -1.191754:
		return "NNW"
	elif dx < 0 and m >= -1.191754 and m <= -0.8391:
		return "NW"
	elif dx < 0 and m > -0.8391 and m < -0.087489:
		return "WNW"
	elif dx < 0 and m >= -0.087489 and m <= 0.087489:
		return "W"
	elif dx < 0 and m > 0.087489 and m < 0.8391:
		return "SSW"
	elif dx < 0 and m >= 0.8391 and m <= 1.191754:
		return "SW"
	elif dx < 0 and m > 1.191754 and m < 11.430052:
		return "SSW"
	elif dx < 0 and m >= 11.430052:
		return "S"
	elif dx > 0 and m <= -11.430052:
		return "S"
	elif dx > 0 and m > -11.430052 and m < -1.191754:
		return "SSE"
	elif dx > 0 and m >= -1.191754 and m <= -0.8391:
		return "SE"
	elif dx > 0 and m > -0.8391 and m < -0.087489:
		return "ESE"
	else:
		return "--"
	
	

		
		
	


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrL = arcpy.GetParameterAsText(0)					  # Layer of Line features


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
d = arcpy.Describe(lyrL)
spref = d.spatialReference
shapefieldname = d.ShapeFieldName


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n")










# ==============================================================================================================
#                                                                                         D O   T H E   W O R K
# ==============================================================================================================

if FieldExists(lyrL, "DIRECTION"):
	msg("The field [DIRECTION] exists? TRUE\n")
else:
	msg("The field [DIRECTION] exists? FALSE. Creating the field.\n")
	arcpy.AddField_management(lyrL, "DIRECTION", "TEXT", "", "", "16", "DIRECTION", "NULLABLE", "NON_REQUIRED", "")
	

msg("Calculating Line Segment Direction.\n")
cur = arcpy.UpdateCursor(lyrL)
for row in cur:
	feat = row.getValue(shapefieldname)
	frompoint = feat.firstPoint
	topoint = feat.lastPoint
	fx = frompoint.X
	fy = frompoint.Y
	tx = topoint.X
	ty = topoint.Y
	dx = tx - fx
	dy = ty - fy
	if (dx != 0 and dy != 0):
		m = (fy - ty)/(fx - tx)
		dir = ComputeDirection(dx, m)
	elif dy == 0 and dx > 0:
		dir = "E"
	elif dy == 0 and dx < 0:
		dir = "W"
	elif dy > 0 and dx == 0:
		dir = "N"
	elif dy < 0 and dx == 0:
		dir = "S"
	elif dy == 0 and dx == 0:
		dir = "Closed Loop"
	else:
		dir = "<error>"
	row.setValue("DIRECTION", dir)
	cur.updateRow(row)
	
	

	

	






msg("\n\nDone!\n\n")



	




