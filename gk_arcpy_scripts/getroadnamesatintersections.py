
"""

  Author: Glenn Kammerer
   Email: gkammerer@sdrmaps.com
  Script: GetRoadNamesatIntersections.py
 Created: 20170413
Modified: 20170417
   About: For each feature in the layer, writes the road names of all other road features that intersect it.

"""



# Import arcpy module
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)
	

# Strip off the first N characters in a string: val[N:], where val is a string value
def BuildRoadNameString(XX, fs, id):
	v = ""
	curs = arcpy.da.SearchCursor(XX, fs)
	for rw in curs:
		if rw[1] != id:
			v = v + ", " + rw[2]
	curs = None	
	return v[2:]
	
def FieldExists(fields, fname):
    for fld in fields:
        if fld.name == fname:
            return True
    return False
	
def CreateField(fs, fn, len):
	if not FieldExists(fs, fn):
		arcpy.AddField_management(lyr, fn, "TEXT", "", "", len, fn, "NULLABLE", "NON_REQUIRED", "")


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================

# Script arguments
# -------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			# Road centerline layer
fldN = arcpy.GetParameterAsText(1)			# Field containing the compiled street name
fldF = arcpy.GetParameterAsText(2)			# Field to write road names to of roads that intersect the from point
fldT = arcpy.GetParameterAsText(3)			# Field to write road names to of roads that intersect the to point


# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
allfields = arcpy.ListFields(lyr)

# Validate fields for output
if not fldF:
	if FieldExists(allfields, "XSTREET_FROM"):
		fldF = "XSTREET_FROM"
	else:
		arcpy.AddField_management(lyr, "XSTREET_FROM", "TEXT", "", "", 100, "XSTREET_FROM", "NULLABLE", "NON_REQUIRED", "")
		fldF = "XSTREET_FROM"
		
if not fldT:
	if FieldExists(allfields, "XSTREET_TO"):
		fldT = "XSTREET_TO"
	else:
		arcpy.AddField_management(lyr, "XSTREET_TO", "TEXT", "", "", 100, "XSTREET_TO", "NULLABLE", "NON_REQUIRED", "")
		fldF = "XSTREET_TO"
		
curflds = []
curflds = ['SHAPE@', 'OID@', fldN, fldF, fldT]
fldOID = arcpy.Describe(lyr).OIDFieldName

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nWriting roads names for intersections...\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================




cur = arcpy.da.UpdateCursor(lyr, curflds)
for row in cur:
	id = row[1]
	n = row[2]
	ptF = row[0].firstPoint
	ptFgeo = arcpy.PointGeometry(ptF)
	ptT = row[0].lastPoint
	ptTgeo = arcpy.PointGeometry(ptT)
	#msg(ptF.X)
	arcpy.SelectLayerByLocation_management(lyr, "INTERSECT", ptFgeo, "", "NEW_SELECTION")
	val1 = BuildRoadNameString(lyr, curflds, id)
	arcpy.SelectLayerByLocation_management(lyr, "INTERSECT", ptTgeo, "", "NEW_SELECTION")
	val2 = BuildRoadNameString(lyr, curflds, id)
	row[3] = val1
	row[4] = val2
	#msg(str(id)+ ": " + val1 + " | " + val2)
	cur.updateRow(row)
	

	# arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "\"" + fldOID + "\" = " + str(id))
	# arcpy.SelectLayerByLocation_management(Target Layer, "INTERSECT", Selecting Layer, "", "NEW_SELECTION")




msg("\n\nDone!\n\n")


