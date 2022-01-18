
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: createintersectionpoints.py
Created: 20170417
Modified: 20180928
About: Creates a point shapefile or feature class at the intersections of all line segments in
	   a street centerline feature layer.
	   
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

# dtermines the workspace type for the user-chosen save location. If it's windows folder, then we have a shapefile, if the path ends
# in .gdb or .mdb, it's a geodatabase, and if it's neither it must be a feature dataset inside a geodatabase.
def GetWorkSpace(t):
	if ".mdb" in t or ".gdb" in t:
		# 
		if t[-4:] == ".mdb" or t[-4:] == ".gdb":
			return "gdb"  # in a geodatabase, no feature dataset
		else:
			return "fds" # in a feature dataset in a geodatabase
	else:
		return "shape"
		
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
ws = arcpy.GetParameterAsText(0)			# Workspace to save the Intersections Points to
lyr = arcpy.GetParameterAsText(1)			# Street Centerlines layer
fldN = arcpy.GetParameterAsText(2)			# Field in Centerlines containing compiled street name
spref = arcpy.GetParameterAsText(3)			# the spatial reference for the Intersection Points (if not saved in Feature Dataset)


# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nCreating Intersection Points layer.\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Create a dictionary of intersection coordinates. A dictionary object serves to eliminate duplicate intersection points.
# -------------------------------------------------------------------------------------------------------------------------
curflds = []
curflds = ['SHAPE@', 'OID@']

coordsdict = {}									# dictionary of distinct coordinate pairs for street centerline feature end points

msg(" Creating dictionary of intersection coordinates.")
cur = arcpy.da.SearchCursor(lyr, curflds, None, spref)
for row in cur:
	k = []                                      # tuple to hold long/lat coordinates
	ptF = row[0].firstPoint
	ptT = row[0].lastPoint
	ptFgeo = arcpy.PointGeometry(ptF)			# creates a point geometry object that is the beginning point of the current line feature
	ptTgeo = arcpy.PointGeometry(ptT)			# creates a point geometry object that is the end point of the current line feature
	k.append(ptF.X)								# adds the from point X coordinate to the tuple
	k.append(ptF.Y)								# adds the from point Y coordinate to the tuple
	ky = str(ptF.X) + "," + str(ptF.Y)          # sets the coordinates as a string to serve as the key in the dictionary
	if not ky in coordsdict:					# tests if the coordinates are already in the dictionary
		coordsdict[ky] = k						# adds the string of the coordinate pair to the coordinate dictionary
		
	k = None									# clears the tuple
	k = []										# re-initializes the tuple
	
	k.append(ptT.X)								# adds the to point X coordinate to the tuple
	k.append(ptT.Y)								# adds the to point Y coordinate to the tuple
	ky = str(ptT.X) + "," + str(ptT.Y)			# sets the coordinates as a string to serve as the key in the dictionary
	if not ky in coordsdict:					# tests if the coordinates are already in the dictionary
		coordsdict[ky] = k						# adds the string of the coordinate pair to the coordinate dictionary
		
	k = None									# clears the tuple
	
	

# Create the Intersection Point layer, add it to the map, and add a few fields to it
# -------------------------------------------------------------------------------------
msg(" Creating the Intersection Point layer, adding fields and adding it to the map.")
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
if GetWorkSpace(ws) == "shape":
	arcpy.CreateFeatureclass_management(ws, "Intersection_Points", "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	isectlyr = arcpy.mapping.Layer(ws + "\\Intersection_Points.shp")
elif GetWorkSpace(ws) == "gdb":
	arcpy.CreateFeatureclass_management(ws, "Intersection_Points", "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	isectlyr = arcpy.mapping.Layer(ws + "\\Intersection_Points")
else:
	arcpy.CreateFeatureclass_management(ws, "Intersection_Points", "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
	isectlyr = arcpy.mapping.Layer(ws + "\\Intersection_Points")
arcpy.mapping.AddLayer(df, isectlyr,"BOTTOM")	
arcpy.AddField_management(isectlyr, "ISECT_CT", "SHORT", "", "", "", "ISECT_CT", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(isectlyr, "STR_NAMES", "TEXT", "", "", "255", "STR_NAMES", "NULLABLE", "NON_REQUIRED", "")


# Add the intersection coordinates from coordsdict to the points layer as point features
# -------------------------------------------------------------------------------------
msg(" Creating point features in the Intersection Point layer from the intersection coordinates.")
cur = arcpy.da.InsertCursor(isectlyr, ['SHAPE@XY'])
for c in coordsdict:
	cur.insertRow([coordsdict[c]])
cur = None	

# Select the centerline features intersecting each point, get that count, get a comma separated list of
# the intersecting road names, and write all that to the point layer.
# -------------------------------------------------------------------------------------------------------	
msg(" Getting intersecting features count and road names at intersections, writing them to the Intersection Point layer.")	
curfields = []
curfields = ['SHAPE@', "ISECT_CT", "STR_NAMES"]
cur = arcpy.da.UpdateCursor(isectlyr, curfields)
for row in cur:
	pt = row[0]
	arcpy.SelectLayerByLocation_management(lyr, "WITHIN_A_DISTANCE", pt, "1 Meters", "NEW_SELECTION")
	#arcpy.SelectLayerByLocation_management(lyr, "INTERSECT", pt, "", "NEW_SELECTION")
	ct = int(arcpy.GetCount_management(lyr).getOutput(0))
	row[1] = ct
	row[2] = GetStreetNameString(lyr)
	cur.updateRow(row)
	
	
	
	
	
	
	
	
	


	# Get the last N characters in a string: val[-N:], where val is a string value	
	# arcpy.CreateFeatureclass_management(shpPath, shpName, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	# arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "\"" + fldOID + "\" = " + str(id))
	# arcpy.SelectLayerByLocation_management(Target Layer, "INTERSECT", Selecting Layer, "", "NEW_SELECTION")

msg("\n\nDone!\n\n")


