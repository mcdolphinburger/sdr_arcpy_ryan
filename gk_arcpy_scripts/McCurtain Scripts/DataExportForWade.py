# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# DataExportForWade.py
# Created on: 2014-03-21
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


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
version = arcpy.GetParameterAsText(0)
doGo2It = arcpy.GetParameter(1)
doDispatch = arcpy.GetParameter(2)
doPublic = arcpy.GetParameter(3)
doWebmap = arcpy.GetParameter(4)



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
srcGDB = "C:\data\SDR\Projects_Data\OK_McCurtain_County\LIVE\McCurtain_LIVE.gdb"
srcA = "C:\data\SDR\Projects_Data\OK_McCurtain_County\LIVE\McCurtain_LIVE.gdb\AddressIt\Addresses"
srcC = "C:\data\SDR\Projects_Data\OK_McCurtain_County\LIVE\McCurtain_LIVE.gdb\AddressIt\Centerlines"
srcD = "C:\data\SDR\Projects_Data\OK_McCurtain_County\LIVE\McCurtain_LIVE.gdb\AddressIt\Driveways"
srcL = "C:\data\SDR\Projects_Data\OK_McCurtain_County\LIVE\McCurtain_LIVE.gdb\AddressIt\Landmarks"

pathGo = "C:\data\SDR\Projects_Data\OK_McCurtain_County\DATA_TO_WADE\Go2It"
pathDisp = "C:\data\SDR\Projects_Data\OK_McCurtain_County\DATA_TO_WADE\MicroDATA"
pathPub = "C:\data\SDR\Projects_Data\OK_McCurtain_County\DATA_TO_WADE\Public"
pathWeb = "C:\data\SDR\Projects_Data\OK_McCurtain_County\DATA_TO_WADE\Webmap"

FieldsAP = []
FieldsAP = [
	["HOUSE_NUM","LONG",""],
	["HOUSE_SUF","LONG",""],
	["PRE_DIR","TEXT","2"],
	["PRE_TYPE","TEXT","15"],
	["STR_NAME","TEXT","60"],
	["STR_TYPE","TEXT","4"],
	["SUF_DIR","TEXT","2"],
	["BUILD_COMP", "TEXT", "32"],
	["BUILD_TYPE", "TEXT", "32"]
  ]
	
FieldsCP = []
FieldsCP = [
	["PRE_DIR","TEXT","2"],
	["PRE_TYPE","TEXT","15"],
	["STR_NAME","TEXT","60"],
	["STR_TYPE","TEXT","4"],
	["SUF_DIR","TEXT","2"],
	["ALT_NAME","TEXT", "100"],
	["L_ADD_LOW", "LONG", ""],
	["L_ADD_HIGH", "LONG", ""],
	["R_ADD_LOW", "LONG", ""],
	["R_ADD_HIGH", "LONG", ""]
  ]
	
FieldsCL = []
FieldsCL = [
	["TYPE","TEXT","20"],
	["PRE_TYPE","TEXT","15"],
	["STR_NAME","TEXT","60"],
	["STR_TYPE","TEXT","4"],
	["SUF_DIR","TEXT","2"],
	["ALT_NAME","TEXT", "100"],
	["L_ADD_LOW", "LONG", ""],
	["L_ADD_HIGH", "LONG", ""],
	["R_ADD_LOW", "LONG", ""],
	["R_ADD_HIGH", "LONG", ""]
  ]


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nExporting Data for Wade.\n--------------------------------------------------\n\n")










# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if doPublic:
	env.workspace = pathPub
	msg("  Exporting data for Public use.\n")
	msg("    Renaming existing Public shapefiles.")
	arcpy.Rename_management ("Addresses_Public.shp", "Addresses_Public_x.shp", "")
	arcpy.Rename_management ("Centerlines_Public.shp", "Centerlines_Public_x.shp", "")
	arcpy.Rename_management ("Driveways_Public.shp", "Driveways_Public_x.shp", "")
	arcpy.Rename_management ("Landmarks_Public.shp", "Landmarks_Public_x.shp", "")
	
# Arguments: Path, Name, Geo Type, Template Feat Class, Has M vals, has Z vals, Coord Sys, Config Keyword, 
#                      Output Sp Grid1, Output Sp Grid2, Output Sp Grid3
# arcpy.CreateFeatureclass_management(shpPath, shpName, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")

	msg("    Creating new shapefiles.")
	arcpy.CreateFeatureclass_management(pathPub, "Addresses_Public", "POINT", "", "DISABLED", "DISABLED", "Addresses_Public_x.shp", "", "0", "0", "0")
	arcpy.CreateFeatureclass_management(pathPub, "Centerlines_Public", "POLYLINE", "", "DISABLED", "DISABLED", "Addresses_Public_x.shp", "", "0", "0", "0")
	arcpy.CreateFeatureclass_management(pathPub, "Driveways_Public", "POLYLINE", "", "DISABLED", "DISABLED", "Addresses_Public_x.shp", "", "0", "0", "0")
	arcpy.CreateFeatureclass_management(pathPub, "Landmarks_Public", "POINT", "", "DISABLED", "DISABLED", "Addresses_Public_x.shp", "", "0", "0", "0")
	





msg("\n\nDone!\n\n")



	




