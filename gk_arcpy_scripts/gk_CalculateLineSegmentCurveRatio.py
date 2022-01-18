# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# gk_CalculateLineSegmentCurveRatio.py
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
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput, math
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

if FieldExists(lyrL, "CURVE_RATIO"):
	msg("The field [CURVE_RATIO] exists? TRUE\n")
else:
	msg("The field [CURVE_RATIO] exists? FALSE. Creating the field.\n")
	arcpy.AddField_management(lyrL, "CURVE_RATIO", "DOUBLE", "", "", "", "CURVE_RATIO", "NULLABLE", "NON_REQUIRED", "")
	

msg("Calculating Curve Ratio.\n")
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
	len = feat.length
	disp = math.sqrt((tx - fx)**2 + (ty - fy)**2)
	if disp == 0:
		cratio = 100000
	else:
		cratio = len / disp
	row.setValue("CURVE_RATIO", cratio)
	cur.updateRow(row)
	
	

	

	






msg("\n\nDone!\n\n")



	




