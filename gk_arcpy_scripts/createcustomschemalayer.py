
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: createcustomschemalayer.py
Created: 2012xxxx
Modified: 20180406
About: Applies the supplied schema to a new, blank feature class.

NOTES:
Re-named the script on 20180406. Was named gk_CreateCustomLayer.py.

"""




# Import modules
# ---------------------------
import arcpy, sys, string, datetime


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================


# TEXT —Names or other textual qualities.
# FLOAT —Numeric values with fractional values within a specific range.
# DOUBLE —Numeric values with fractional values within a specific range.
# SHORT —Numeric values without fractional values within a specific range; coded values.
# LONG —Numeric values without fractional values within a specific range.
# DATE —Date and/or Time.
# BLOB —Images or other multimedia.
# RASTER —Raster images.
# GUID —GUID values
	
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
FL = arcpy.GetParameterAsText(0)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
L = []
L = [
	["USER_NAME","TEXT","32","",""],
	["ASIAUSER","TEXT","10","",""],
	["JOINID","LONG","","",""],
	["FLAG","TEXT","2","",""],
	["PCONST","TEXT","4","",""],
	["RNG_LOW","LONG","","",""],
	["RNG_HIGH","LONG","","",""],
	["DATE_NEW","DATE","","",""],
	["DATE_MOD","DATE","","",""],
	["PREFIX","TEXT","2","",""],
	["PRE_TYPE","TEXT","4","",""],
	["NAME","TEXT","40","",""],
	["SUFFIX","TEXT","4","",""],
	["POSTDIR","TEXT","2","",""],
	["RDNAME","TEXT","64","",""],
	["MAPLABEL","TEXT","25","",""],
	["ALIAS","TEXT","64","",""],
	["ALIAS2","TEXT","64","",""],
	["CLASSIFI","TEXT","32","",""],
	["CODE","TEXT","25","",""],
	["HWY_NUMBER","TEXT","6","",""],
	["LEFT_FROM","LONG","","",""],
	["LEFT_TO","LONG","","",""],
	["RIGHT_FROM","LONG","","",""],
	["RIGHT_TO","LONG","","",""],
	["LEFTRANGE","TEXT","20","",""],
	["RIGHTRANGE","TEXT","20","",""],
	["ZIP_COMM_E","TEXT","32","",""],
	["ZIP_COMM_O","TEXT","32","",""],
	["COMM_L","TEXT","25","",""],
	["COMM_R","TEXT","25","",""],
	["ESN_L","LONG","","",""],
	["ESN_R","LONG","","",""],
	["LAW_L","TEXT","25","",""],
	["LAW_R","TEXT","25","",""],
	["FIRE_L","TEXT","25","",""],
	["FIRE_R","TEXT","25","",""],
	["EMS_L","TEXT","25","",""],
	["EMS_R","TEXT","25","",""],
	["STATE","TEXT","2","",""],
	["CNTYID","TEXT","4","",""],
	["ONEWAY","TEXT","2","",""],
	["LANES","SHORT","","",""],
	["SHOULDER","TEXT","5","",""],
	["SURFACE","TEXT","32","",""],
	["LASTCHANGE","TEXT","128","",""],
	["DATA_SOURCE","TEXT","50","",""],
	["NOTE1","TEXT","254","",""],
	["NOTE2","TEXT","254","",""],
	["RECORDID","LONG","","",""],
	["ROAD_SIGN","TEXT","64","",""],
	["FEATURE_GU","TEXT","38","",""],
	["STOP1","TEXT","4","",""],
	["COMMENT","TEXT","50","",""],
	["STREET","TEXT","50","",""],
	["ESN","LONG","","",""],
	["EESN","SHORT","","",""],
	["OESN","SHORT","","",""],
	["COMM","TEXT","32","",""],
	["ECOMM","TEXT","32","",""],
	["OCOMM","TEXT","32","",""],
	["TELCO","TEXT","4","",""],
	["ETELCO","TEXT","4","",""],
	["OTELCO","TEXT","4","",""],
	["DIR","TEXT","4","",""],
	["FNA","LONG","","",""],
	["TNA","LONG","","",""],
	["ODD","TEXT","1","",""],
	["TYPE","TEXT","6","",""],
	["MSAG_ID","LONG","","",""],
	["CROSS_FR","TEXT","50","",""],
	["CROSS_TO","TEXT","50","",""],
	["CROSS_FR_N","TEXT","50","",""],
	["CROSS_TO_N","TEXT","50","",""]
	]

## Dade County Original Address Point Schema
## -------------------------------------------

## Stone County Original Address Point Schema
## -------------------------------------------
# L = [
	# ["STATE","TEXT","2","",""],
	# ["ZIP","TEXT","12","",""],
	# ["HOUSE__","TEXT","16","",""],
	# ["NEW_ADD","LONG","","10",""],
	# ["RECORDID","DOUBLE","","",""],
	# ["PHONE_3","TEXT","16","",""],
	# ["PHONE_4","TEXT","16","",""],
	# ["PHONE_5","TEXT","16","",""],
	# ["PHONE_6","TEXT","16","",""],
	# ["PHONE_7","TEXT","10","",""],
	# ["PHONE_8","TEXT","8","",""],
	# ["PHONE_9","TEXT","16","",""],
	# ["COUNTY_ID","TEXT","5","",""],
	# ["STATE_ID","TEXT","5","",""],
	# ["LB","LONG","","5",""],
	# ["FLAG","TEXT","2","",""],
	# ["LAST_NAME","TEXT","50","",""],
	# ["FIRST_NAME","TEXT","50","",""],
	# ["PHONE","TEXT","14","",""],
	# ["PHONE2","TEXT","14","",""],
	# ["APT","TEXT","50","",""],
	# ["UNIQUE_","DOUBLE","","",""],
	# ["MAPPAGE","TEXT","5","",""],
	# ["ADDNUMBER","TEXT","20","",""],
	# ["MAIL_CITY","TEXT","32","",""],
	# ["CITY","TEXT","32","",""],
	# ["CELLPHONE","TEXT","15","",""],
	# ["CELLPHONE2","TEXT","15","",""],
	# ["CELLPHONE3","TEXT","15","",""],
	# ["LONGITUDE","DOUBLE","","",""],
	# ["LATITUDE","DOUBLE","","",""],
	# ["X_COORD","DOUBLE","","",""],
	# ["Y_COORD","DOUBLE","","",""],
	# ["NAT_GRID","TEXT","16","",""],
	# ["ALPHA","TEXT","16","",""],
	# ["RDNAME","TEXT","64","",""],
	# ["ALIAS","TEXT","64","",""],
	# ["EXCHANGE","TEXT","4","",""],
	# ["PARITY","TEXT","1","",""],
	# ["PARCEL_ID","TEXT","128","",""],
	# ["EMAIL","TEXT","64","",""],
	# ["TOWNSHIP","TEXT","10","",""],
	# ["FULL_ADDRE","TEXT","64","",""],
	# ["PREFIX","TEXT","2","",""],
	# ["ROAD_NAME","TEXT","32","",""],
	# ["SUFFIX","TEXT","4","",""],
	# ["POSTDIR","TEXT","2","",""],
	# ["FIREDEPT","TEXT","20","",""],
	# ["CITY_COUNT","TEXT","20","",""],
	# ["SITE_","TEXT","32","",""],
	# ["POINT_ID","TEXT","32","",""],
	# ["FEATURE_GU","TEXT","38","",""],
	# ["FEATURE__1","TEXT","38","",""],
	# ["COMP_STR_N","TEXT","50","",""],
	# ["USER_NAME","TEXT","32","",""],
	# ["POST_DIR","TEXT","2","",""],
	# ["PRE_DIR","TEXT","2","",""],
	# ["STREET_TYP","TEXT","4","",""],
	# ["DATE_CREAT","DATE","","",""],
	# ["DATE_MODIF","DATE","","",""],
	# ["USER_INITI","TEXT","3","",""],
	# ["STRUCTURE_","LONG","","10",""],
	# ["FULL_ADD_1","TEXT","64","",""],
	# ["NOTE1","TEXT","254","",""],
	# ["NOTE2","TEXT","254","",""],
	# ["UNIT_TYPE","TEXT","16","",""],
	# ["UNIT_DESIG","TEXT","16","",""],
	# ["SUB_UNIT","TEXT","16","",""],
	# ["STREET_NAM","TEXT","32","",""],
	# ["STREET_T_1","TEXT","4","",""],
	# ["COMP_STR_1","TEXT","64","",""],
	# ["ALIAS1","TEXT","64","",""],
	# ["ALIAS2","TEXT","64","",""],
	# ["LAST_NAME1","TEXT","32","",""],
	# ["FIRST_NA_1","TEXT","32","",""],
	# ["LAST_NAME2","TEXT","32","",""],
	# ["FIRST_NA_2","TEXT","32","",""],
	# ["LL_PHONE1","TEXT","14","",""],
	# ["LL_PHONE2","TEXT","14","",""],
	# ["CELL_PHONE","TEXT","14","",""],
	# ["CELL_PHO_1","TEXT","14","",""],
	# ["MAIL_ADD1","TEXT","8","",""],
	# ["MAIL_ADD2","TEXT","32","",""],
	# ["MAIL_STATE","TEXT","2","",""],
	# ["MAIL_ZIP","TEXT","12","",""],
	# ["E911_COMM","TEXT","32","",""],
	# ["STRUCTURE1","TEXT","32","",""],
	# ["STRUCTUR_1","TEXT","32","",""],
	# ["LAST_CHANG","TEXT","128","",""],
	# ["DATA_SOURC","TEXT","16","",""],
	# ["HOTLINK","TEXT","254","",""],
	# ["FEATURE__2","TEXT","38","",""],
	# ["ESN","LONG","","5",""],
	# ["CLASSIF","TEXT","10","",""],
	# ["CREATED_US","TEXT","254","",""],
	# ["CREATED_DA","DATE","","",""],
	# ["LAST_EDITE","TEXT","254","",""],
	# ["LAST_EDI_1","DATE","","",""]
	# ]


## Osage County MO Cell Sector Schema
## -------------------------------------------
# L = [
	# ["SDR_ID","LONG","","",""],
	# ["SDR_ID2","TEXT","10","",""],
	# ["ADDRESS","TEXT","50","",""],
	# ["COMMUNITY","TEXT","50","",""],
	# ["HOUSE_NO","LONG","","",""],
	# ["HOUSE_SUFF","TEXT","20","",""],
	# ["STR_DIR","TEXT","2","",""],
	# ["STR_NAME","TEXT","50","",""],
	# ["STR_SUFFIX","TEXT","4","",""],
	# ["POST_DIR","TEXT","2","",""],
	# ["STR_NAME_1","TEXT","50","",""],
	# ["STR_NAME_2","TEXT","50","",""],
	# ["CUST_NAME","TEXT","50","",""],
	# ["COMPANY_ID","TEXT","50","",""],
	# ["TOWER_LAT","DOUBLE","","",""],
	# ["TOWER_LONG","DOUBLE","","",""],
	# ["SECT_RAD","DOUBLE","","",""],
	# ["SECT_RAD2","TEXT","50","",""],
	# ["AZIMUTH","DOUBLE","","",""],
	# ["BEAMWID","DOUBLE","","",""],
	# ["L_ANG_1","DOUBLE","","",""],
	# ["R_ANG_1","DOUBLE","","",""],
	# ["TOWER_ID","TEXT","50","",""],
	# ["SECTOR_ID","TEXT","50","",""],
	# ["SUGG_PSAP","TEXT","50","",""],
	# ["NOTES","TEXT","150","",""],
	# ["RTG_SHEET","TEXT","150","",""],
	# ["FT_GUID","TEXT","50","",""]
	# ]


# L = [
	# ["X","DOUBLE","","",""],
	# ["Y","DOUBLE","","",""],
	# ["ADDRESS","TEXT","100","",""],
	# ["STREETNO","DOUBLE","","",""],
	# ["UNITTYPE","TEXT","50","",""],
	# ["UNITNUM","TEXT","50","",""],
	# ["PREDIR","TEXT","2","",""],
	# ["PRETYPE","TEXT","50","",""],
	# ["STREETNAME","TEXT","50","",""],
	# ["STREETSUFF","TEXT","4","",""],
	# ["POSTDIR","TEXT","2","",""],
	# ["CITY","TEXT","50","",""],
	# ["COMMUNITY","TEXT","50","",""],
	# ["EDIT","TEXT","50","",""],
	# ["DATE_ENTER","TEXT","50","",""],
	# ["PRE","TEXT","50","",""],
	# ["LNAME","TEXT","50","",""],
	# ["FNAME","TEXT","50","",""],
	# ["ROUTE","TEXT","50","",""],
	# ["BOX","TEXT","50","",""],
	# ["ZIPCODE","TEXT","9","",""],
	# ["STATE","TEXT","2","",""],
	# ["EXCH","TEXT","50","",""],
	# ["RECTYPE","LONG","","",""],
	# ["COUNTY","LONG","","",""],
	# ["HUTYP","TEXT","50","",""],
	# ["NUMUNITS","LONG","","",""],
	# ["CENTFLAG","LONG","","",""],
	# ["LOCATION","TEXT","50","",""],
	# ["ACCT_NO","TEXT","50","",""],
	# ["HOUSE_DESC","TEXT","100","",""],
	# ["MAIL_ADD","TEXT","50","",""],
	# ["ESN","TEXT","5","",""],
	# ["DATE","DATE","","",""],
	# ["FORMER_ADD","TEXT","100","",""],
	# ["SCHOOL_DIS","TEXT","50","",""],
	# ["NOTES","TEXT","255","",""],
	# ["VERIFIED","TEXT","50","",""],
	# ["VERIFIED_D","DATE","","",""],
	# ["VERIFIED_B","TEXT","50","",""],
	# ["ORIGINAL_D","DATE","","",""],
	# ["ASSIGNED_B","TEXT","50","",""]
    # ]

# L = [
	# ["JOINID", "LONG", ""],
	# ["FLAG", "TEXT", "2"],
	# ["DATE_NEW", "DATE", ""],
	# ["DATE_MOD", "DATE", ""],
	# ["USER_NAME", "TEXT", "32"],
	# ["ASIAUSER", "TEXT", "10"],
	# ["PREFIX", "TEXT", "2"],
	# ["PRE_TYPE", "TEXT", "25"],
	# ["NAME", "TEXT", "40"],
	# ["SUFFIX", "TEXT", "4"],
	# ["POSTDIR", "TEXT", "2"],
	# ["RDNAME", "TEXT", "64"],
	# ["ALIAS", "TEXT", "64"],
	# ["ALIAS2", "TEXT", "64"],
	# ["LEFT_FROM", "LONG", ""],
	# ["LEFT_TO", "LONG", ""],
	# ["RIGHT_FROM", "LONG", ""],
	# ["RIGHT_TO", "LONG", ""],
	# ["CLASSIFI", "TEXT", "32"],
	# ["ZIPCOMM_L", "TEXT", "32"],
	# ["ZIPCOMM_R", "TEXT", "32"],
	# ["ZIP_L", "LONG", ""],
	# ["ZIP_R", "LONG", ""],
	# ["MSAGCOMM_L", "TEXT", "32"],
	# ["MSAGCOMM_R", "TEXT", "32"],
	# ["ESNSDR_L", "SHORT", ""],
	# ["ESNSDR_R", "SHORT", ""],
	# ["TELCO_L", "TEXT", "4"],
	# ["TELCO_R", "TEXT", "4"],
	# ["LASTCHANGE", "TEXT", "128"],
	# ["FEATURE_GUID", "TEXT", "38"],
	# ["NOTE1", "TEXT", "255"],
	# ["NOTE2", "TEXT", "255"],
	# ["LANES", "SHORT", ""],
	# ["SURFACE", "TEXT", "32"],
	# ["ONEWAY", "TEXT", "2"],
	# ["SHOULDER", "TEXT", "5"],
	# ["ROAD_SIGN", "TEXT", "64"],
	# ["DATA_SOURC", "TEXT", "16"],
	# ["PCONST", "TEXT", "4"],
	# ["RNG_LOW", "LONG", ""],
	# ["RNG_HIGH", "LONG", ""],
	# ["STOP1", "TEXT", "4"],
	# ["COMM", "TEXT", "32"],
	# ["ESN", "LONG", ""],
	# ["TELCO", "TEXT", "4"],
	# ["LEFTRANGE", "TEXT", "20"],
	# ["RIGHTRANGE", "TEXT", "20"],
	# ["DIR", "TEXT", "4"],
	# ["RECORDID", "LONG", ""],
	# ["STATE", "TEXT", "2"],
	# ["CNTYID", "TEXT", "4"],
	# ["MAPLABEL", "TEXT", "25"],
	# ["STOP2", "TEXT", "4"],
	# ["FNA", "LONG", ""],
	# ["TNA", "LONG", ""],
	# ["ODD", "TEXT", "1"],
	# ["STREET", "TEXT", "50"],
	# ["TYPE", "TEXT", "6"],
	# ["HWY_NUMBER", "TEXT", "6"],
	# ["CODE", "TEXT", "25"],
	# ["COMM_L", "TEXT", "25"],
	# ["COMM_R", "TEXT", "25"],
	# ["ESN_L", "LONG", ""],
	# ["ESN_R", "LONG", ""],
	# ["LAW_L", "TEXT", "25"],
	# ["LAW_R", "TEXT", "25"],
	# ["FIRE_L", "TEXT", "25"],
	# ["FIRE_R", "TEXT", "25"],
	# ["EMS_L", "TEXT", "25"],
	# ["EMS_R", "TEXT", "25"],
	# ["COMMENT", "TEXT", "50"],
	# ["MSAG_ID", "LONG", ""],
	# ["CROSS_FR", "TEXT", "50"],
	# ["CROSS_TO", "TEXT", "50"],
	# ["CROSS_FR_N", "TEXT", "50"],
	# ["CROSS_TO_N", "TEXT", "50"],
	# ["DATA_SOURCE", "TEXT", "50"]
    # ]


# L = [
	# ["JOINID","LONG",""],
	# ["DATE_CREATED","DATE",""],
	# ["DATE_MODIFIED","DATE",""],
	# ["USER_NAME","TEXT","32"],
	# ["USER_INITIALS","TEXT","3"],
	# ["PRE_DIR","TEXT","2"],
	# ["PRE_TYPE","TEXT","50"],
	# ["NAME","TEXT","50"],
	# ["TYPE","TEXT","4"],
	# ["SUFFIX_DIR","TEXT","2"],
	# ["NAME_FULL","TEXT","100"],
	# ["ALIAS1","TEXT","64"],
	# ["ALIAS2","TEXT","64"],
	# ["ALIAS3","TEXT","64"],
	# ["L_F_ADD","LONG",""],
	# ["L_T_ADD","LONG",""],
	# ["R_F_ADD","LONG",""],
	# ["R_T_ADD","LONG",""],
	# ["CLASS","TEXT","32"],
	# ["LEFT_CITY","TEXT","50"],
	# ["RIGHT_CITY","TEXT","50"],
	# ["E911_COMM_E","TEXT","32"],
	# ["E911_COMM_O","TEXT","32"],
	# ["ESN_E","SHORT",""],
	# ["ESN_O","SHORT",""],
	# ["EXCHANGE_E","TEXT","4"],
	# ["EXCHANGE_O","TEXT","4"],
	# ["LAST_CHANGE","TEXT","128"],
	# ["FLAG","TEXT","2"],
	# ["FEATURE_GUID","TEXT","38"],
	# ["NOTES","TEXT","255"],
	# ["NOTE2","TEXT","255"],
	# ["LANES","SHORT",""],
	# ["SURFACE","TEXT","32"],
	# ["ONEWAY","TEXT","2"],
	# ["SHOULDER","TEXT","1"],
	# ["ROAD_SIGN","TEXT","64"],
	# ["DATA_SOURCE","TEXT","16"],
	# ["STOP","TEXT","4"],
	# ["PROBLEMS","TEXT","100"],
	# ["TOWNSHIP","TEXT","2"],
	# ["TOWN","TEXT","2"],
	# ["COUNTY","TEXT","2"],
	# ["DIRECTION","TEXT","2"],
	# ["ROW_GUID","TEXT","50"],
	# ]

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n\n")


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

msg("                          Field Name, Field Type, Length, Precision, Scale")
msg("-------------------------------------------------------------------------------")


# Arguments: input table, [0]field name, [1]field type, [2]length

for i in L:
	if i[1] == "TEXT":
		msg("  Adding new TEXT field: " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "TEXT", "", "", i[2], i[0], "NULLABLE", "NON_REQUIRED", "")
	elif i[1] == "SHORT":
		msg(" Adding new SHORT field: " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "SHORT", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")
	elif i[1] == "LONG":
		msg("  Adding new LONG field: " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "LONG", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")
	elif i[1] == "DOUBLE":
		msg("Adding new DOUBLE field: " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "DOUBLE", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")
	elif i[1] == "DATE":
		msg("  Adding new DATE field: " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "DATE", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")





msg("\n\nDone!\n\n")



	




