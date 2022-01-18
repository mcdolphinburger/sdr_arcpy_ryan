
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: createcustomschemalayer.py
Created: 20180904
Modified: 20201102
About: Applies the OK NG9-1-1 Schema to blank layers

NOTES:
Was named createcustomschemalayer.py prior to 20180904

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
lyr = arcpy.GetParameterAsText(0)
lyrtyp = arcpy.GetParameterAsText(1)



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
L = []

L = [
	["CENTERLINES","DISCRPAGID","TEXT","75"],
	["CENTERLINES","NGUID_RDCL","TEXT","254"],
	["CENTERLINES","AGENCY_ID","TEXT","100"],
	["CENTERLINES","FULLNAME","TEXT","50"],
	["CENTERLINES","LABEL","TEXT","50"],
	["CENTERLINES","ADD_L_PRE","TEXT","15"],
	["CENTERLINES","ADD_R_PRE","TEXT","15"],
	["CENTERLINES","ADD_L_FROM","LONG",""],
	["CENTERLINES","ADD_L_TO","LONG",""],
	["CENTERLINES","ADD_R_FROM","LONG",""],
	["CENTERLINES","ADD_R_TO","LONG",""],
	["CENTERLINES","PARITY_L","TEXT","1"],
	["CENTERLINES","PARITY_R","TEXT","1"],
	["CENTERLINES","PREMOD","TEXT","15"],
	["CENTERLINES","PREDIR","TEXT","9"],
	["CENTERLINES","PRETYPE","TEXT","50"],
	["CENTERLINES","PRETYPESEP","TEXT","20"],
	["CENTERLINES","STREET","TEXT","60"],
	["CENTERLINES","STREETTYPE","TEXT","50"],
	["CENTERLINES","SUFDIR","TEXT","9"],
	["CENTERLINES","SUFMOD","TEXT","25"],
	["CENTERLINES","COUNTRY_L","TEXT","2"],
	["CENTERLINES","COUNTRY_R","TEXT","2"],
	["CENTERLINES","STATE_L","TEXT","2"],
	["CENTERLINES","STATE_R","TEXT","2"],
	["CENTERLINES","COUNTY_L","TEXT","40"],
	["CENTERLINES","COUNTY_R","TEXT","40"],
	["CENTERLINES","CITY_L","TEXT","100"],
	["CENTERLINES","CITY_R","TEXT","100"],
	["CENTERLINES","UNINCCOMML","TEXT","100"],
	["CENTERLINES","UNINCCOMMR","TEXT","100"],
	["CENTERLINES","NBRHDCOMML","TEXT","100"],
	["CENTERLINES","NBRHDCOMMR","TEXT","100"],
	["CENTERLINES","ESN_L","TEXT","5"],
	["CENTERLINES","ESN_R","TEXT","5"],
	["CENTERLINES","PSAP_L","TEXT","25"],
	["CENTERLINES","PSAP_R","TEXT","25"],
	["CENTERLINES","MSAGCOMM_L","TEXT","30"],
	["CENTERLINES","MSAGCOMM_R","TEXT","30"],
	["CENTERLINES","ZIPCODE_L","TEXT","7"],
	["CENTERLINES","ZIPCODE_R","TEXT","7"],
	["CENTERLINES","ZIPCODE4_L","TEXT","4"],
	["CENTERLINES","ZIPCODE4_R","TEXT","4"],
	["CENTERLINES","POSTCOMM_L","TEXT","40"],
	["CENTERLINES","POSTCOMM_R","TEXT","40"],
	["CENTERLINES","ROADCLASS","TEXT","15"],
	["CENTERLINES","ONEWAY","TEXT","2"],
	["CENTERLINES","SPEEDLIMIT","SHORT",""],
	["CENTERLINES","INITISRCE","TEXT","75"],
	["CENTERLINES","INITIDATE","DATE",""],
	["CENTERLINES","REVEDITOR","TEXT","75"],
	["CENTERLINES","REVDATE","DATE",""],
	["CENTERLINES","EFFECTDATE","DATE",""],
	["CENTERLINES","EXPIREDATE","DATE",""],
	["CENTERLINES","COMMENT","TEXT","100"],
	["CENTERLINES","ALTSTNAME1","TEXT","50"],
	["CENTERLINES","ALTSTNAME2","TEXT","50"],
	["CENTERLINES","ALTSTNAME3","TEXT","50"],
	["CENTERLINES","LGCYPREDIR","TEXT","2"],
	["CENTERLINES","LGCYSTREET","TEXT","75"],
	["CENTERLINES","LGCYTYPE","TEXT","4"],
	["CENTERLINES","LGCYSUFDIR","TEXT","2"],
	["CENTERLINES","FROMLEVEL","TEXT","10"],
	["CENTERLINES","TOLEVEL","TEXT","10"],
	["CENTERLINES","BOUNDLANE","TEXT","9"],
	["CENTERLINES","ROADLENGTH","DOUBLE","15"],
	["CENTERLINES","DRIVETIME","DOUBLE","15"],
	["CENTERLINES","DEADEND","TEXT","1"],
	["CENTERLINES","SURFACE","TEXT","10"],
	["CENTERLINES","LANES","TEXT","5"],
	["CENTERLINES","TOLL","TEXT","1"],
	["CENTERLINES","LTDACCESS","TEXT","1"],
	["CENTERLINES","VALID_L","TEXT","1"],
	["CENTERLINES","VALID_R","TEXT","1"],
	["CENTERLINES","SUBMIT","TEXT","1"],
	["CENTERLINES","TOPOEXCEPT","TEXT","20"],
	["CENTERLINES","GEOMSAG_L","TEXT","1"],
	["CENTERLINES","GEOMSAG_R","TEXT","1"],
	["ADDRESS","DISCRPAGID","TEXT","75"],
	["ADDRESS","NGUID_ADD","TEXT","254"],
	["ADDRESS","AGENCY_ID","TEXT","100"],
	["ADDRESS","FULLADDR","TEXT","100"],
	["ADDRESS","FULLNAME","TEXT","50"],
	["ADDRESS","LABEL","TEXT","50"],
	["ADDRESS","ADDPRE","TEXT","15"],
	["ADDRESS","ADDRESS","LONG","6"],
	["ADDRESS","ADDSUF","TEXT","15"],
	["ADDRESS","PREMOD","TEXT","15"],
	["ADDRESS","PREDIR","TEXT","9"],
	["ADDRESS","PRETYPE","TEXT","50"],
	["ADDRESS","PRETYPESEP","TEXT","20"],
	["ADDRESS","STREET","TEXT","60"],
	["ADDRESS","STREETTYPE","TEXT","50"],
	["ADDRESS","SUFDIR","TEXT","9"],
	["ADDRESS","SUFMOD","TEXT","25"],
	["ADDRESS","COUNTRY","TEXT","2"],
	["ADDRESS","STATE","TEXT","2"],
	["ADDRESS","COUNTY","TEXT","40"],
	["ADDRESS","CITY","TEXT","100"],
	["ADDRESS","UNINCCOMM","TEXT","100"],
	["ADDRESS","NBRHDCOMM","TEXT","100"],
	["ADDRESS","ESN","TEXT","5"],
	["ADDRESS","PSAP","TEXT","25"],
	["ADDRESS","MSAGCOMM","TEXT","30"],
	["ADDRESS","POSTCOMM","TEXT","40"],
	["ADDRESS","ZIPCODE","TEXT","7"],
	["ADDRESS","ZIPCODE4","TEXT","4"],
	["ADDRESS","LANDMKNAME","TEXT","150"],
	["ADDRESS","ADDTNLLOC","TEXT","225"],
	["ADDRESS","BLDGNAME","TEXT","75"],
	["ADDRESS","FLOOR","TEXT","75"],
	["ADDRESS","BLDGUNIT","TEXT","75"],
	["ADDRESS","ROOM","TEXT","75"],
	["ADDRESS","SEAT","TEXT","75"],
	["ADDRESS","GRPQUARTER","TEXT","1"],
	["ADDRESS","OCCUPTIME","TEXT","50"],
	["ADDRESS","STRMSHELTR","TEXT","25"],
	["ADDRESS","BASEMENT","TEXT","1"],
	["ADDRESS","PLACETYPE","TEXT","50"],
	["ADDRESS","PLACEMENT","TEXT","25"],
	["ADDRESS","MILEPOST","TEXT","150"],
	["ADDRESS","LONGITUDE","DOUBLE","15"],
	["ADDRESS","LATITUDE","DOUBLE","15"],
	["ADDRESS","ELEVATION","DOUBLE","6"],
	["ADDRESS","ADDDATAURI","TEXT","254"],
	["ADDRESS","INITISRCE","TEXT","75"],
	["ADDRESS","INITIDATE","DATE","20"],
	["ADDRESS","REVEDITOR","TEXT","75"],
	["ADDRESS","REVDATE","DATE","20"],
	["ADDRESS","EFFECTDATE","DATE","20"],
	["ADDRESS","EXPIREDATE","DATE","20"],
	["ADDRESS","COMMENT","TEXT","100"],
	["ADDRESS","LGCYADD","TEXT","100"],
	["ADDRESS","LGCYPREDIR","TEXT","2"],
	["ADDRESS","LGCYSTREET","TEXT","75"],
	["ADDRESS","LGCYTYPE","TEXT","4"],
	["ADDRESS","LGCYSUFDIR","TEXT","2"],
	["ADDRESS","SUBMIT","TEXT","1"],
	["ADDRESS","RCLMATCH","TEXT","254"],
	["ADDRESS","RCLSIDE","TEXT","1"]
    ]



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
	if lyrtyp == "CENTERLINES" and i[0] == "CENTERLINES":
		if i[2] == "TEXT":
			msg("Adding new TEXT field:   " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "TEXT", "", "", i[3], i[1], "NULLABLE", "NON_REQUIRED", "")
		elif i[2] == "SHORT":
			msg("Adding new SHORT field:  " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "SHORT", "", "", "", i[1], "NULLABLE", "NON_REQUIRED", "")
		elif i[2] == "LONG":
			msg("Adding new LONG field:   " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "LONG", "", "", "", i[1], "NULLABLE", "NON_REQUIRED", "")
		elif i[2] == "DOUBLE":
			msg("Adding new DOUBLE field: " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "DOUBLE", "", "", "", i[1], "NULLABLE", "NON_REQUIRED", "")
		elif i[2] == "DATE":
			msg("Adding new DATE field:   " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "DATE", "", "", "", i[1], "NULLABLE", "NON_REQUIRED", "")
	elif lyrtyp == "ADDRESS" and i[0] == "ADDRESS":
		if i[2] == "TEXT":
			msg("Adding new TEXT field:   " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "TEXT", "", "", i[3], i[1], "NULLABLE", "NON_REQUIRED", "")
		elif i[2] == "SHORT":
			msg("Adding new SHORT field:  " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "SHORT", "", "", "", i[1], "NULLABLE", "NON_REQUIRED", "")
		elif i[2] == "LONG":
			msg("Adding new LONG field:   " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "LONG", "", "", "", i[1], "NULLABLE", "NON_REQUIRED", "")
		elif i[2] == "DOUBLE":
			msg("Adding new DOUBLE field: " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "DOUBLE", "", "", "", i[1], "NULLABLE", "NON_REQUIRED", "")
		elif i[2] == "DATE":
			msg("Adding new DATE field:   " + str(i[1]))
			arcpy.AddField_management(lyr, i[1], "DATE", "", "", "", i[1], "NULLABLE", "NON_REQUIRED", "")





msg("\n\nDone!\n\n")



	




