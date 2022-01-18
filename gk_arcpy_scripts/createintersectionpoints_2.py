
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: createintersectionpoints2.py
Created: 20170417
Modified: xxx
About: Creates a point shapefile or feature class at the intersections of all line segments in
	   a street centerline feature layer.
	   
"""



# Import arcpy module
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


"""
GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision
"""

# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)

def GetWorkSpace(t):
	if ".mdb" in t or ".gdb" in t:
		if t[-4:] == ".mdb" or t[-4:] == ".gdb":
			return "gdb"  # in a geodatabase, no feature dataset
		else:
			return "fds" # in a feature dataset in a geodatabase
	else:
		return "shape" 
		
def GetStreetNameCount(lay):
# receives a layer with selected features. very few will be selected and only those selected
# will be in the cursor.
	namelist = []
	cr = None								# initialize cursor	
	cf = []									# initialize cursor fields list
	cf.append(fldN)                         # fldN is one of the original inputs
	cr = arcpy.da.SearchCursor(lay, cf)
	for rw in cr:
		namelist.append(rw[0])
	namecount = len(set(namelist))
	return namecount
		
def GetStreetNameString(lay):
# receives a layer with selected features. very few will be selected and only those selected
# will be in the cursor.
	cr = None
	v = ""
	cf = []
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
outName = arcpy.GetParameterAsText(3)		# The output Feature Class for the intersection points


# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
curflds = []
curflds = ['SHAPE@', 'OID@']
coordsdict = {}
spref = arcpy.Describe(lyr).spatialReference


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nCreating Intersection Points layer.\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Create a dictionary of intersection coordinates. A dictionary object serves to eliminate duplicate intersection points.
# -------------------------------------------------------------------------------------------------------------------------
msg(" Creating dictionary of intersection coordinates.")
cur = arcpy.da.SearchCursor(lyr, curflds, None, spref)
for row in cur:
	k = []                                      # tuple to hold long/lat coordinates
	ptF = row[0].firstPoint
	ptT = row[0].lastPoint
	ptFgeo = arcpy.PointGeometry(ptF)
	ptTgeo = arcpy.PointGeometry(ptT)
	k.append(ptF.X)
	k.append(ptF.Y)
	ky = str(ptF.X) + "," + str(ptF.Y)          # coordinates as a string to serve as the key in the dictionary
	if not ky in coordsdict:
		coordsdict[ky] = k
	k = None
	k = []
	k.append(ptT.X)
	k.append(ptT.Y)
	ky = str(ptT.X) + "," + str(ptT.Y)
	if not ky in coordsdict:
		coordsdict[ky] = k
	k = None	

# Create the Intersection Point layer, add it to the map, and add a few fields to it
# -------------------------------------------------------------------------------------
msg(" Creating the Intersection Point layer, adding fields and adding it to the map.")
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
if GetWorkSpace(ws) == "shape":
	arcpy.CreateFeatureclass_management(ws, outName, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	isectlyr = arcpy.mapping.Layer(ws + "\\" + outName)
elif GetWorkSpace(ws) == "gdb":
	arcpy.CreateFeatureclass_management(ws, outName, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	isectlyr = arcpy.mapping.Layer(ws + "\\" + outName)
else:
	arcpy.CreateFeatureclass_management(ws, outName, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
	isectlyr = arcpy.mapping.Layer(ws + "\\" + outName)
arcpy.mapping.AddLayer(df, isectlyr,"BOTTOM")	
arcpy.AddField_management(isectlyr, "FEAT_COUNT", "SHORT", "", "", "", "FEAT_COUNT", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(isectlyr, "NAME_COUNT", "SHORT", "", "", "", "NAME_COUNT", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(isectlyr, "STR_NAMES", "TEXT", "", "", "255", "STR_NAMES", "NULLABLE", "NON_REQUIRED", "")


# Add the intersection coordinates from coordsdict to the points layer as point features
# -------------------------------------------------------------------------------------
msg(" Creating point features in the Intersection Point layer from the intersection coordinate.")
cur = arcpy.da.InsertCursor(isectlyr, ['SHAPE@XY'])
for c in coordsdict:
	cur.insertRow([coordsdict[c]])
cur = None	

# Select the centerline features intersecting each point, get that count, get a comma separated list of
# the intersecting road names, and write all that to the point layer.
# -------------------------------------------------------------------------------------------------------	
msg(" Getting intersecting features count and road names at intersections, writing them to the Intersection Point layer.")	
curfields = []
curfields = ['SHAPE@', "FEAT_COUNT", "NAME_COUNT", "STR_NAMES"]
cur = arcpy.da.UpdateCursor(isectlyr, curfields)
for row in cur:
	pt = row[0]
	arcpy.SelectLayerByLocation_management(lyr, "INTERSECT", pt, "", "NEW_SELECTION")
	ct = int(arcpy.GetCount_management(lyr).getOutput(0))
	row[1] = ct
	row[2] = GetStreetNameCount(lyr)
	row[3] = GetStreetNameString(lyr)
	cur.updateRow(row)
    
	
	
	
	
	
	
	
	
	


	# Get the last N characters in a string: val[-N:], where val is a string value	
	# arcpy.CreateFeatureclass_management(shpPath, shpName, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	# arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "\"" + fldOID + "\" = " + str(id))
	# arcpy.SelectLayerByLocation_management(Target Layer, "INTERSECT", Selecting Layer, "", "NEW_SELECTION")

msg("\n\nDone!\n\n")


