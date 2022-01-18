
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: createintersectionpoints.py
Created: 20180128
Modified: 20180128
About: Writes the intersecting road names to the centerline attribute table.
	   
"""



# Import arcpy module
# (my scripts are always stubbed out with these imports. obviously not all are used)
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)

		
def GetStreetNameString(lay):
# receives a layer with selected features. very few will be selected and only those selected
# will be in the cursor.
	cr = None								# cr = cursor
	v = ""									# v = value
	cf = []									# cf = cursor fields
	cf.append(fldN)                         # fldN is one of the original inputs
	cr = arcpy.da.SearchCursor(lay, cf)
	for rw in cr:
		v = v + ", " + rw[0]
	return v[2:]


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================

# Script arguments
# -------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			# Street Centerlines layer
fldN = arcpy.GetParameterAsText(1)			# Field in Centerlines containing compiled street name


# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
spref = arcpy.Describe(lyr).featureClass.SpatialReference
oidfld = arcpy.Describe(lyr).OIDFieldName


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nAdding street names of intersection street centerlines features to street centerline attribute table.")
msg("---------------------------------------------------------------------------------------------------------------\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================



# STEP 1: Add fields for intersection street names to existing centerline layer
# -------------------------------------------------------------------------------------------------------------------------
msg("Adding fields for street name values of intersection street centerline features.")
if arcpy.ListFields(lyr, "ISECT_FROM"):  
    msg("  ISECT_FROM field exists? True")
else:  
	msg("  ISECT_FROM field exists? False, added field")
	arcpy.AddField_management(lyr, "ISECT_FROM", "TEXT", "", "", "255", "ISECT_FROM", "NULLABLE", "NON_REQUIRED", "")
	
if arcpy.ListFields(lyr, "ISECT_TO"):  
    msg("  ISECT_TO field exists? True")
else:  
    msg("  ISECT_TO field exists? False, added field")
    arcpy.AddField_management(lyr, "ISECT_TO", "TEXT", "", "", "255", "ISECT_TO", "NULLABLE", "NON_REQUIRED", "")
	
	

# STEP 2: Add the street names to the attribute table
# -------------------------------------------------------------------------------------------------------------------------
msg("Adding intersecting street name values to the street centerline attribute table.")
curflds = []
curflds = ['SHAPE@', 'OID@', fldN, "ISECT_FROM", "ISECT_TO"]
cur = arcpy.da.SearchCursor(lyr, curflds, None, spref)

for row in cur:
	void = row[1]
	ptFgeo = arcpy.PointGeometry(row[0].firstPoint)
	ptTgeo = arcpy.PointGeometry(row[0].lastPoint)
	arcpy.SelectLayerByLocation_management(lyr, "INTERSECT", ptFgeo, "", "NEW_SELECTION")
	wc = oidfld + " = " + str(void)
	arcpy.SelectLayerByAttribute_management(lyr, "REMOVE_FROM_SELECTION", wc)
	ct = int(arcpy.GetCount_management(lyr).getOutput(0))









# # Select the centerline features intersecting each point, get that count, get a comma separated list of
# # the intersecting road names, and write all that to the point layer.
# # -------------------------------------------------------------------------------------------------------	
# msg(" Getting intersecting features count and road names at intersections, writing them to the Intersection Point layer.")	
# curfields = []
# curfields = ['SHAPE@', "ISECT_CT", "STR_NAMES"]
# cur = arcpy.da.UpdateCursor(isectlyr, curfields)
# for row in cur:
	# pt = row[0]
	# arcpy.SelectLayerByLocation_management(lyr, "INTERSECT", pt, "", "NEW_SELECTION")
	# ct = int(arcpy.GetCount_management(lyr).getOutput(0))
	# row[1] = ct
	# row[2] = GetStreetNameString(lyr)
	# cur.updateRow(row)
	
	
	
	
	
	
	
	
	
	
	

# # Create a dictionary of intersection coordinates. A dictionary object serves to eliminate duplicate intersection points.
# # -------------------------------------------------------------------------------------------------------------------------
# msg(" Creating dictionary of intersection coordinates.")
# cur = arcpy.da.SearchCursor(lyr, curflds, None, spref)
# for row in cur:
	# k = []                                      # tuple to hold long/lat coordinates
	# ptF = row[0].firstPoint
	# ptT = row[0].lastPoint
	# ptFgeo = arcpy.PointGeometry(ptF)			# creates a point geometry object that is the beginning point of the current line feature
	# ptTgeo = arcpy.PointGeometry(ptT)			# creates a point geometry object that is the end point of the current line feature
	# k.append(ptF.X)
	# k.append(ptF.Y)
	# ky = str(ptF.X) + "," + str(ptF.Y)          # coordinates as a string to serve as the key in the dictionary
	# if not ky in coordsdict:
		# coordsdict[ky] = k
	# k = None
	# k = []
	# k.append(ptT.X)
	# k.append(ptT.Y)
	# ky = str(ptT.X) + "," + str(ptT.Y)
	# if not ky in coordsdict:
		# coordsdict[ky] = k
	# k = None	

# # Create the Intersection Point layer, add it to the map, and add a few fields to it
# # -------------------------------------------------------------------------------------
# msg(" Creating the Intersection Point layer, adding fields and adding it to the map.")
# mxd = arcpy.mapping.MapDocument("CURRENT")
# df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
# if GetWorkSpace(ws) == "shape":
	# arcpy.CreateFeatureclass_management(ws, "Intersection_Points", "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	# isectlyr = arcpy.mapping.Layer(ws + "\\Intersection_Points.shp")
# elif GetWorkSpace(ws) == "gdb":
	# arcpy.CreateFeatureclass_management(ws, "Intersection_Points", "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	# isectlyr = arcpy.mapping.Layer(ws + "\\Intersection_Points")
# else:
	# arcpy.CreateFeatureclass_management(ws, "Intersection_Points", "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
	# isectlyr = arcpy.mapping.Layer(ws + "\\Intersection_Points")
# arcpy.mapping.AddLayer(df, isectlyr,"BOTTOM")	
# arcpy.AddField_management(isectlyr, "ISECT_CT", "SHORT", "", "", "", "ISECT_CT", "NULLABLE", "NON_REQUIRED", "")
# arcpy.AddField_management(isectlyr, "STR_NAMES", "TEXT", "", "", "255", "STR_NAMES", "NULLABLE", "NON_REQUIRED", "")


# # Add the intersection coordinates from coordsdict to the points layer as point features
# # -------------------------------------------------------------------------------------
# msg(" Creating point features in the Intersection Point layer from the intersection coordinates.")
# cur = arcpy.da.InsertCursor(isectlyr, ['SHAPE@XY'])
# for c in coordsdict:
	# cur.insertRow([coordsdict[c]])
# cur = None	


	
	
	
	
	
	
	
	
	


	# # Get the last N characters in a string: val[-N:], where val is a string value	
	# # arcpy.CreateFeatureclass_management(shpPath, shpName, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	# # arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "\"" + fldOID + "\" = " + str(id))
	# # arcpy.SelectLayerByLocation_management(Target Layer, "INTERSECT", Selecting Layer, "", "NEW_SELECTION")

msg("\n\nDone!\n\n")


