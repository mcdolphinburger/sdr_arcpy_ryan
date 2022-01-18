
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: labelscripts.py
Created: xxxxxxxx
Modified: 20170829
About: Script that creates AddressIt ready feature classes.

"""




# Import arcpy modules and toolboxes
# --------------------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


## ==============================================================================================================
##                                                                     F U N C T I O N S / D E F I N I T I O N S
## ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)




## ==============================================================================================================
##                                                                           I N I T I A L I Z E   S C R I P T
## ==============================================================================================================

# Script arguments
# --------------------------------------------------------------------------------------------------------------
ws = arcpy.GetParameterAsText(0)						# Target Workspace
spref = arcpy.GetParameterAsText(1)						# Feature Layer Coordinate System
side = arcpy.GetParameterAsText(2)					    # Create Even/Odd fields or Left/Right fields
lyR = arcpy.GetParameter(3)					  			# Create Road Centerlines Yes/No
lyA = arcpy.GetParameter(4)					 			# Create Addresses Yes/No
lyD = arcpy.GetParameter(5)								# Create Driveways Yes/No
lyL = arcpy.GetParameter(6)								# Create Landmarks Yes/No
lyH = arcpy.GetParameter(7)					   			# Create Hydrants Yes/No
lyC = arcpy.GetParameter(8)					    		# Create Cell Towers Yes/No
lyB = arcpy.GetParameter(9)					    		# Create Bridges Yes/No


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
# Get the last N characters in a string: val[-N:], where val is a string value
if ws[-4:] != ".gdb" and ws[-4:] != ".mdb":
	spref = ""
rcl_nam = "xCenterlines"
add_nam = "xAddresses"
dwy_nam = "xDriveways"
lmk_nam = "xLandmarks"
hyd_nam = "xHydrants"
tow_nam = "xCellTowers"
brg_nam = "xBridges"

schema_roads = []
schema_roads = [
	["JOINID","LONG",""],
	["PCONST","TEXT","4"],
	["RNG_LOW","LONG",""],
	["RNG_HIGH","LONG",""],
	["FLAG","TEXT","2"],
	["DATE_CREATED","DATE",""],
	["DATE_MODIFIED","DATE",""],
	["USER_NAME","TEXT","32"],
	["USER_INITIALS","TEXT","3"],
	["PRE_DIR","TEXT","2"],
	["PRE_TYPE","TEXT","20"],
	["STREET_NAME","TEXT","32"],
	["STREET_TYPE","TEXT","4"],
	["POST_DIR","TEXT","2"],
	["COMP_STR_NAME","TEXT","64"],
	["ALIAS1","TEXT","64"],
	["ALIAS2","TEXT","64"],
	["LEFT_FROM","LONG",""],
	["LEFT_TO","LONG",""],
	["RIGHT_FROM","LONG",""],
	["RIGHT_TO","LONG",""],
	["CLASSIFICATION","TEXT","32"],
	["CLASSIFICATION2","TEXT","32"],
	["PARITY_L","TEXT","2"],
	["PARITY_R","TEXT","2"],
	["COUNTY_L","TEXT","40"],
	["COUNTY_R","TEXT","40"],
	["STATE_L","TEXT","2"],
	["STATE_R","TEXT","2"],
	["ZIP_L","TEXT","5"],
	["ZIP_R","TEXT","5"],
	["ZIP_COMM_L","TEXT","32"],
	["ZIP_COMM_R","TEXT","32"],
	["E911_COMM_L","TEXT","32"],
	["E911_COMM_R","TEXT","32"],
	["ESN_L","SHORT",""],
	["ESN_R","SHORT",""],
	["EXCHANGE_L","TEXT","4"],
	["EXCHANGE_R","TEXT","4"],
	["LAST_CHANGE","TEXT","128"],
	["FEATURE_GUID","TEXT","38"],
	["NOTE1","TEXT","255"],
	["NOTE2","TEXT","255"],
	["LANES","SHORT",""],
	["SURFACE","TEXT","32"],
	["ONE_WAY","TEXT","1"],
	["SHOULDER","TEXT","1"],
	["ROAD_SIGN","TEXT","64"],
	["DATA_SOURCE","TEXT","16"],
	["NGGUID","TEXT","100"],
	["NGGUID_NUM","DOUBLE",""],
	["NGGUID_NUM2","DOUBLE",""],
	["STOP1","TEXT","4"]]
	
schema_adds = []
schema_adds = [
	["JOINID","LONG",""],
	["FLAG","TEXT","2"],
	["DATE_CREATED","DATE",""],
	["DATE_MODIFIED","DATE",""],
	["POINT_ID","TEXT","32"],
	["USER_NAME","TEXT","32"],
	["USER_INITIALS","TEXT","3"],
	["STRUCTURE_NUM","LONG",""],
	["UNIT_TYPE","TEXT","16"],
	["UNIT_DESIG","TEXT","16"],
	["SUB_UNIT","TEXT","16"],
	["UNIT_BLDG","TEXT","75"],
	["UNIT_FLOOR","TEXT","75"],
	["UNIT_DESIG2","TEXT","75"],
	["UNIT_ROOM","TEXT","75"],
	["UNIT_SEAT","TEXT","75"],
	["PRE_DIR","TEXT","2"],
	["PRE_TYPE","TEXT","20"],
	["STREET_NAME","TEXT","32"],
	["STREET_TYPE","TEXT","4"],
	["POST_DIR","TEXT","2"],
	["COMP_STR_NAME","TEXT","64"],
	["ALIAS1","TEXT","64"],
	["ALIAS2","TEXT","64"],
	["FULL_ADDRESS","TEXT","64"],
	["LAST_NAME1","TEXT","32"],
	["FIRST_NAME1","TEXT","32"],
	["LAST_NAME2","TEXT","32"],
	["FIRST_NAME2","TEXT","32"],
	["LL_PHONE1","TEXT","14"],
	["LL_PHONE2","TEXT","14"],
	["CELL_PHONE1","TEXT","14"],
	["CELL_PHONE2","TEXT","14"],
	["MAIL_ADD1","TEXT","8"],
	["MAIL_ADD2","TEXT","32"],
	["MAIL_CITY","TEXT","32"],
	["MAIL_STATE","TEXT","2"],
	["MAIL_ZIP","TEXT","12"],
	["CITY","TEXT","32"],
	["STATE","TEXT","2"],
	["ZIP","TEXT","12"],
	["E911_COMM","TEXT","32"],
	["ESN","SHORT",""],
	["EXCHANGE","TEXT","4"],
	["PARITY","TEXT","1"],
	["PARCEL_ID","TEXT","128"],
	["STRUCTURE_COMP","TEXT","32"],
	["STRUCTURE_TYPE","TEXT","32"],
	["LAST_CHANGE","TEXT","128"],
	["DATA_SOURCE","TEXT","16"],
	["HOTLINK","TEXT","255"],
	["EMAIL","TEXT","64"],
	["NOTE1","TEXT","255"],
	["NOTE2","TEXT","255"],
	["LONGITUDE","DOUBLE",""],
	["LATITUDE","DOUBLE",""],
	["X_COORD","DOUBLE",""],
	["Y_COORD","DOUBLE",""],
	["NAT_GRID","TEXT","16"],
	["FEATURE_GUID","TEXT","38"],
	["ADD_CHECK","TEXT","50"],
	["NGGUID","TEXT","100"],
	["NGGUID_NUM","DOUBLE",""],
	["STOP1","TEXT","4"]]



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nCreating new AddressIt feature classes.\n===============================================================\n\n")


"""
Default spatial reference value
 PROJCS["NAD_1983_UTM_Zone_15N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-93.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0],AUTHORITY["EPSG",26915]]
"""


# MAINLINE
# =========================================================================================================================


# Create FeatureClasses
# -------------------------------------------------------
if lyR:
	msg("Creating Street Centerline FeatureClass")
	arcpy.CreateFeatureclass_management(ws, rcl_nam, "POLYLINE", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	msg("Adding fields to Street Centerlines")
	IL = ws + "\\" + rcl_nam
	for i in schema_roads:
		arcpy.AddField_management(IL, i[0], i[1], "", "", i[2], i[0], "NULLABLE", "NON_REQUIRED", "")
if lyA:
	msg("Creating Address FeatureClass")
	arcpy.CreateFeatureclass_management(ws, add_nam, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
	msg("Adding fields to Address Points")
	IL = ws + "\\" + add_nam
	for i in schema_adds:
		arcpy.AddField_management(IL, i[0], i[1], "", "", i[2], i[0], "NULLABLE", "NON_REQUIRED", "")
if lyD:
	msg("Creating Driveway FeatureClass")
	arcpy.CreateFeatureclass_management(ws, dwy_nam, "POLYLINE", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
if lyL:
	msg("Creating Landmark FeatureClass")
	arcpy.CreateFeatureclass_management(ws, lmk_nam, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
if lyH:
	msg("Creating Hydrant FeatureClass")
	arcpy.CreateFeatureclass_management(ws, hyd_nam, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
if lyC:
	msg("Creating Cell Tower FeatureClass")
	arcpy.CreateFeatureclass_management(ws, tow_nam, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
if lyB:
	msg("Creating Bridge FeatureClass")
	arcpy.CreateFeatureclass_management(ws, brg_nam, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")





# Add Driveway Fields
# -------------------------------------------------------
if lyD:
	msg("Adding Driveway Layer Fields...")
	IL = ws + "\\" + dwy_nam
	arcpy.AddField_management(IL, "FLAG", "TEXT", "", "", "2", "FLAG", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_CREATED", "DATE", "", "", "", "DATE_CREATED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_MODIFIED", "DATE", "", "", "", "DATE_MODIFIED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "POINT_ID", "TEXT", "", "", "32", "POINT_ID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "STOP1", "TEXT", "", "", "4", "STOP1", "NULLABLE", "NON_REQUIRED", "")




# Add Landmark Fields
# -------------------------------------------------------
if lyL:
	msg("Adding Landmark Layer Fields...")
	IL = ws + "\\" + lmk_nam
	arcpy.AddField_management(IL, "JOINID", "LONG", "", "", "", "JOINID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FLAG", "TEXT", "", "", "2", "FLAG", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_CREATED", "DATE", "", "", "", "DATE_CREATED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_MODIFIED", "DATE", "", "", "", "DATE_MODIFIED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATA_SOURCE", "TEXT", "", "", "16", "DATA_SOURCE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "USER_NAME", "TEXT", "", "", "32", "USER_NAME", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "USER_INITIALS", "TEXT", "", "", "3", "USER_INITIALS", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "POINT_ID", "TEXT", "", "", "32", "POINT_ID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "TYPE", "TEXT", "", "", "20", "TYPE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "CONDITION", "TEXT", "", "", "20", "CONDITION", "NULLABLE", "REQUIRED", "")
	arcpy.AddField_management(IL, "LAST_CHANGE", "TEXT", "", "", "128", "LAST_CHANGE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NOTE1", "TEXT", "", "", "255", "NOTE1", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NOTE2", "TEXT", "", "", "255", "NOTE2", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LONGITUDE", "DOUBLE", "", "", "", "LONGITUDE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LATITUDE", "DOUBLE", "", "", "", "LATITUDE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "X_COORD", "DOUBLE", "", "", "", "X_COORD", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "Y_COORD", "DOUBLE", "", "", "", "Y_COORD", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NAT_GRID", "TEXT", "", "", "16", "NAT_GRID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FEATURE_GUID", "TEXT", "", "", "38", "FEATURE_GUID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "STOP1", "TEXT", "", "", "4", "STOP1", "NULLABLE", "NON_REQUIRED", "")




# Add Hydrant Fields
# -------------------------------------------------------
if lyH:
	msg("Adding Hydrant Layer Fields...")
	IL = ws + "\\" + hyd_nam
	arcpy.AddField_management(IL, "JOINID", "LONG", "", "", "", "JOINID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FLAG", "TEXT", "", "", "2", "FLAG", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_CREATED", "DATE", "", "", "", "DATE_CREATED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_MODIFIED", "DATE", "", "", "", "DATE_MODIFIED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "POINT_ID", "TEXT", "", "", "32", "POINT_ID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "USER_NAME", "TEXT", "", "", "32", "USER_NAME", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "USER_INITIALS", "TEXT", "", "", "3", "USER_INITIALS", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATA_SOURCE", "TEXT", "", "", "16", "DATA_SOURCE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LAST_CHANGE", "TEXT", "", "", "128", "LAST_CHANGE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "CONSTRUCTION", "TEXT", "", "", "20", "CONSTRUCTION", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "CONDITION", "TEXT", "", "", "20", "CONDITION", "NULLABLE", "REQUIRED", "")
	arcpy.AddField_management(IL, "CAPACITY", "TEXT", "", "", "32", "CAPACITY", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "SERVICED", "DATE", "", "", "", "SERVICED", "NULLABLE", "REQUIRED", "")
	arcpy.AddField_management(IL, "NOTE1", "TEXT", "", "", "255", "NOTE1", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NOTE2", "TEXT", "", "", "255", "NOTE2", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LONGITUDE", "DOUBLE", "", "", "", "LONGITUDE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LATITUDE", "DOUBLE", "", "", "", "LATITUDE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "X_COORD", "DOUBLE", "", "", "", "X_COORD", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "Y_COORD", "DOUBLE", "", "", "", "Y_COORD", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NAT_GRID", "TEXT", "", "", "16", "NAT_GRID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FEATURE_GUID", "TEXT", "", "", "38", "FEATURE_GUID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "STOP1", "TEXT", "", "", "4", "STOP1", "NULLABLE", "NON_REQUIRED", "")



# Add Cell Tower Fields
# -------------------------------------------------------
if lyC:
	msg("Adding Cell Tower Layer Fields...")
	IL = ws + "\\" + tow_nam
	arcpy.AddField_management(IL, "JOINID", "LONG", "", "", "", "JOIN_ID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FLAG", "TEXT", "", "", "2", "FLAG", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_CREATED", "DATE", "", "", "", "DATE_CREATED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_MODIFIED", "DATE", "", "", "", "DATE_MODIFIED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "POINT_ID", "TEXT", "", "", "32", "POINT_ID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "USER_NAME", "TEXT", "", "", "32", "USER_NAME", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "USER_INITIALS", "TEXT", "", "", "3", "USER_INITIALS", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATA_SOURCE", "TEXT", "", "", "16", "DATA_SOURCE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LAST_CHANGE", "TEXT", "", "", "128", "LAST_CHANGE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "CONSTRUCTION", "TEXT", "", "", "20", "CONSTRUCTION", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "CONDITION", "TEXT", "", "", "20", "CONDITION", "NULLABLE", "REQUIRED", "")
	arcpy.AddField_management(IL, "OWNER", "TEXT", "", "", "32", "OWNER", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "HEIGHT", "DOUBLE", "", "", "", "HEIGHT", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FACE_DIR", "TEXT", "", "", "2", "FACE_DIR", "NULLABLE", "REQUIRED", "")
	arcpy.AddField_management(IL, "NOTE1", "TEXT", "", "", "255", "NOTE1", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NOTE2", "TEXT", "", "", "255", "NOTE2", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LONGITUDE", "DOUBLE", "", "", "", "LONGITUDE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LATITUDE", "DOUBLE", "", "", "", "LATITUDE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "X_COORD", "DOUBLE", "", "", "", "X_COORD", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "Y_COORD", "DOUBLE", "", "", "", "Y_COORD", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NAT_GRID", "TEXT", "", "", "16", "NAT_GRID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FEATURE_GUID", "TEXT", "", "", "38", "FEATURE_GUID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "STOP1", "TEXT", "", "", "4", "STOP1", "NULLABLE", "NON_REQUIRED", "")

	
	
# Add Bridges Fields
# -------------------------------------------------------
if lyB:
	msg("Adding Bridges Layer Fields...")
	IL = ws + "\\" + brg_nam
	arcpy.AddField_management(IL, "JOINID", "LONG", "", "", "", "JOIN_ID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FLAG", "TEXT", "", "", "2", "FLAG", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_CREATED", "DATE", "", "", "", "DATE_CREATED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATE_MODIFIED", "DATE", "", "", "", "DATE_MODIFIED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "POINT_ID", "TEXT", "", "", "32", "POINT_ID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "USER_NAME", "TEXT", "", "", "32", "USER_NAME", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "USER_INITIALS", "TEXT", "", "", "3", "USER_INITIALS", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "DATA_SOURCE", "TEXT", "", "", "16", "DATA_SOURCE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LAST_CHANGE", "TEXT", "", "", "128", "LAST_CHANGE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "CONSTRUCTION", "TEXT", "", "", "20", "CONSTRUCTION", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "CONDITION", "TEXT", "", "", "20", "CONDITION", "NULLABLE", "REQUIRED", "")
	arcpy.AddField_management(IL, "CAPACITY", "TEXT", "", "", "32", "CAPACITY", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "WIDTH", "DOUBLE", "", "", "", "WIDTH", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "SURFACE", "TEXT", "", "", "32", "SURFACE", "NULLABLE", "REQUIRED", "")
	arcpy.AddField_management(IL, "LENGTH", "DOUBLE", "", "", "", "LENGTH", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "BUILD_DATE", "DATE", "", "", "", "BUILD_DATE", "NULLABLE", "REQUIRED", "")
	arcpy.AddField_management(IL, "NOTE1", "TEXT", "", "", "255", "NOTE1", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NOTE2", "TEXT", "", "", "255", "NOTE2", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LONGITUDE", "DOUBLE", "", "", "", "LONGITUDE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "LATITUDE", "DOUBLE", "", "", "", "LATITUDE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "X_COORD", "DOUBLE", "", "", "", "X_COORD", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "Y_COORD", "DOUBLE", "", "", "", "Y_COORD", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "NAT_GRID", "TEXT", "", "", "16", "NAT_GRID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "FEATURE_GUID", "TEXT", "", "", "38", "FEATURE_GUID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(IL, "STOP1", "TEXT", "", "", "4", "STOP1", "NULLABLE", "NON_REQUIRED", "")
	
	
	
	
	
	
	
	



msg("\n\nDone!\n\n")
