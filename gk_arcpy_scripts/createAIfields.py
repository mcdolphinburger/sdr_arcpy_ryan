
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: createAIfields.py
Created: 20190517
Modified: 20190517
About: Script that adds AddressIt fields to the specified feature classes.

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
fc = arcpy.GetParameterAsText(0)						# Target Feature Class
fctype = arcpy.GetParameterAsText(1)					# The type of AddressIt layer (Address points or Centerlines)
side = arcpy.GetParameterAsText(2)					    # Create Even/Odd fields or Left/Right fields



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
# Get the last N characters in a string: val[-N:], where val is a string value



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nAdding AddressIt fields to Feature Class.\n===============================================================\n\n")





# MAINLINE
# =========================================================================================================================





# Add Road Centerline Fields
# -------------------------------------------------------
if fctype == "Roads":
	msg("Adding Road Centerline Layer Fields...")
	arcpy.AddField_management(fc, "JOINID", "LONG", "", "", "", "JOINID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "PCONST", "TEXT", "", "", "4", "PCONST", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "RNG_LOW", "LONG", "", "", "", "RNG_LOW", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "RNG_HIGH", "LONG", "", "", "", "RNG_HIGH", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "FLAG", "TEXT", "", "", "2", "FLAG", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "DATE_CREATED", "DATE", "", "", "", "DATE_CREATED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "DATE_MODIFIED", "DATE", "", "", "", "DATE_MODIFIED", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "USER_NAME", "TEXT", "", "", "32", "USER_NAME", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "USER_INITIALS", "TEXT", "", "", "3", "USER_INITIALS", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "PRE_DIR", "TEXT", "", "", "2", "PRE_DIR", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "PRE_TYPE", "TEXT", "", "", "20", "PRE_TYPE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "STREET_NAME", "TEXT", "", "", "32", "STREET_NAME", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "STREET_TYPE", "TEXT", "", "", "4", "STREET_TYPE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "POST_DIR", "TEXT", "", "", "2", "POST_DIR", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "COMP_STR_NAME", "TEXT", "", "", "64", "COMP_STR_NAME", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "ALIAS1", "TEXT", "", "", "64", "ALIAS1", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "ALIAS2", "TEXT", "", "", "64", "ALIAS2", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "LEFT_FROM", "LONG", "", "", "", "LEFT_FROM", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "LEFT_TO", "LONG", "", "", "", "LEFT_TO", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "RIGHT_FROM", "LONG", "", "", "", "RIGHT_FROM", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "RIGHT_TO", "LONG", "", "", "", "RIGHT_TO", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "CLASSIFICATION", "TEXT", "", "", "32", "CLASSIFICATION", "NULLABLE", "NON_REQUIRED", "")
	if side == "Even/Odd":
		arcpy.AddField_management(fc, "ZIP_E", "TEXT", "", "", "10", "ZIP_E", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ZIP_O", "TEXT", "", "", "10", "ZIP_O", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ZIP_COMM_E", "TEXT", "", "", "32", "ZIP_COMM_E", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ZIP_COMM_O", "TEXT", "", "", "32", "ZIP_COMM_O", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "E911_COMM_E", "TEXT", "", "", "32", "E911_COMM_E", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "E911_COMM_O", "TEXT", "", "", "32", "E911_COMM_O", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ESN_E", "SHORT", "", "", "", "ESN_E", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ESN_O", "SHORT", "", "", "", "ESN_O", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "EXCHANGE_E", "TEXT", "", "", "4", "EXCHANGE_E", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "EXCHANGE_O", "TEXT", "", "", "4", "EXCHANGE_O", "NULLABLE", "NON_REQUIRED", "")
	else:
		arcpy.AddField_management(fc, "ZIP_L", "TEXT", "", "", "10", "ZIP_L", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ZIP_R", "TEXT", "", "", "10", "ZIP_R", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ZIP_COMM_L", "TEXT", "", "", "32", "ZIP_COMM_L", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ZIP_COMM_R", "TEXT", "", "", "32", "ZIP_COMM_R", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "E911_COMM_L", "TEXT", "", "", "32", "E911_COMM_L", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "E911_COMM_R", "TEXT", "", "", "32", "E911_COMM_R", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ESN_L", "SHORT", "", "", "", "ESN_L", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "ESN_R", "SHORT", "", "", "", "ESN_R", "NULLABLE", "NON_REQUIRED", "")
		# arcpy.AddField_management(fc, "FIRE_L", "TEXT", "", "", "10", "FIRE_L", "NULLABLE", "NON_REQUIRED", "")
		# arcpy.AddField_management(fc, "FIRE_R", "TEXT", "", "", "10", "FIRE_R", "NULLABLE", "NON_REQUIRED", "")
		# arcpy.AddField_management(fc, "LAW_L", "TEXT", "", "", "10", "LAW_L", "NULLABLE", "NON_REQUIRED", "")
		# arcpy.AddField_management(fc, "LAW_R", "TEXT", "", "", "10", "LAW_R", "NULLABLE", "NON_REQUIRED", "")
		# arcpy.AddField_management(fc, "EMS_L", "TEXT", "", "", "10", "EMS_L", "NULLABLE", "NON_REQUIRED", "")
		# arcpy.AddField_management(fc, "EMS_R", "TEXT", "", "", "10", "EMS_R", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "EXCHANGE_L", "TEXT", "", "", "4", "EXCHANGE_L", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(fc, "EXCHANGE_R", "TEXT", "", "", "4", "EXCHANGE_R", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "LAST_CHANGE", "TEXT", "", "", "128", "LAST_CHANGE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "FEATURE_GUID", "TEXT", "", "", "38", "FEATURE_GUID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "NOTE1", "TEXT", "", "", "255", "NOTE1", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "NOTE2", "TEXT", "", "", "255", "NOTE2", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "LANES", "SHORT", "", "", "", "LANES", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "SURFACE", "TEXT", "", "", "32", "SURFACE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "ONE_WAY", "TEXT", "", "", "1", "ONE_WAY", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "SHOULDER", "TEXT", "", "", "1", "SHOULDER", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "ROAD_SIGN", "TEXT", "", "", "64", "ROAD_SIGN", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "DATA_SOURCE", "TEXT", "", "", "16", "DATA_SOURCE", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "NGGUID", "TEXT", "", "", "100", "NGGUID", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "NGGUID_NUM", "DOUBLE", "", "", "", "NGGUID_NUM", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(fc, "STOP1", "TEXT", "", "", "4", "STOP1", "NULLABLE", "NON_REQUIRED", "")

	
	

# Add Address Fields
# -------------------------------------------------------
if fctype == "Addresses":
    arcpy.AddField_management(fc, "JOINID", "LONG", "", "", "", "JOINID", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "FLAG", "TEXT", "", "", "2", "FLAG", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "DATE_CREATED", "DATE", "", "", "", "DATE_CREATED", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "DATE_MODIFIED", "DATE", "", "", "", "DATE_MODIFIED", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "POINT_ID", "TEXT", "", "", "32", "POINT_ID", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "USER_NAME", "TEXT", "", "", "32", "USER_NAME", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "USER_INITIALS", "TEXT", "", "", "3", "USER_INITIALS", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "STRUCTURE_NUM", "LONG", "", "", "", "STRUCTURE_NUM", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "UNIT_TYPE", "TEXT", "", "", "16", "UNIT_TYPE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "UNIT_DESIG", "TEXT", "", "", "16", "UNIT_DESIG", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "SUB_UNIT", "TEXT", "", "", "16", "SUB_UNIT", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "PRE_DIR", "TEXT", "", "", "2", "PRE_DIR", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "PRE_TYPE", "TEXT", "", "", "20", "PRE_TYPE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "STREET_NAME", "TEXT", "", "", "32", "STREET_NAME", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "STREET_TYPE", "TEXT", "", "", "4", "STREET_TYPE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "POST_DIR", "TEXT", "", "", "2", "POST_DIR", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "COMP_STR_NAME", "TEXT", "", "", "64", "COMP_STR_NAME", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "ALIAS1", "TEXT", "", "", "64", "ALIAS1", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "ALIAS2", "TEXT", "", "", "64", "ALIAS2", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "FULL_ADDRESS", "TEXT", "", "", "64", "FULL_ADDRESS", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "LAST_NAME1", "TEXT", "", "", "32", "LAST_NAME1", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "FIRST_NAME1", "TEXT", "", "", "32", "FIRST_NAME1", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "LAST_NAME2", "TEXT", "", "", "32", "LAST_NAME2", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "FIRST_NAME2", "TEXT", "", "", "32", "FIRST_NAME2", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "LL_PHONE1", "TEXT", "", "", "14", "LL_PHONE1", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "LL_PHONE2", "TEXT", "", "", "14", "LL_PHONE2", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "CELL_PHONE1", "TEXT", "", "", "14", "CELL_PHONE1", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "CELL_PHONE2", "TEXT", "", "", "14", "CELL_PHONE2", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "MAIL_ADD1", "TEXT", "", "", "8", "MAIL_ADD1", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "MAIL_ADD2", "TEXT", "", "", "32", "MAIL_ADD2", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "MAIL_CITY", "TEXT", "", "", "32", "MAIL_CITY", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "MAIL_STATE", "TEXT", "", "", "2", "MAIL_STATE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "MAIL_ZIP", "TEXT", "", "", "12", "MAIL_ZIP", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "CITY", "TEXT", "", "", "32", "CITY", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "STATE", "TEXT", "", "", "2", "STATE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "ZIP", "TEXT", "", "", "12", "ZIP", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "E911_COMM", "TEXT", "", "", "32", "E911_COMM", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "ESN", "SHORT", "", "", "", "ESN", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "EXCHANGE", "TEXT", "", "", "4", "EXCHANGE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "PARITY", "TEXT", "", "", "1", "PARITY", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "PARCEL_ID", "TEXT", "", "", "128", "PARCEL_ID", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "STRUCTURE_COMP", "TEXT", "", "", "32", "STRUCTURE_COMP", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "STRUCTURE_TYPE", "TEXT", "", "", "32", "STRUCTURE_TYPE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "LAST_CHANGE", "TEXT", "", "", "128", "LAST_CHANGE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "DATA_SOURCE", "TEXT", "", "", "16", "DATA_SOURCE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "HOTLINK", "TEXT", "", "", "255", "HOTLINK", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "EMAIL", "TEXT", "", "", "64", "EMAIL", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "NOTE1", "TEXT", "", "", "255", "NOTE1", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "NOTE2", "TEXT", "", "", "255", "NOTE2", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "LONGITUDE", "DOUBLE", "", "", "", "LONGITUDE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "LATITUDE", "DOUBLE", "", "", "", "LATITUDE", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "X_COORD", "DOUBLE", "", "", "", "X_COORD", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "Y_COORD", "DOUBLE", "", "", "", "Y_COORD", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "NAT_GRID", "TEXT", "", "", "16", "NAT_GRID", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "FEATURE_GUID", "TEXT", "", "", "38", "FEATURE_GUID", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "ADD_CHECK", "TEXT", "", "", "50", "ADD_CHECK", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "NGGUID", "TEXT", "", "", "100", "NGGUID", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "NGGUID_NUM", "DOUBLE", "", "", "", "NGGUID_NUM", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "STOP1", "TEXT", "", "", "4", "STOP1", "NULLABLE", "NON_REQUIRED", "")





msg("\n\nDone!\n\n")
