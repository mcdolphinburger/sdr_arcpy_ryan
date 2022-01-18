# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# gk_CreateCustomLayer.py
# Created on: 2012-xx-xx
#
#
# Description: 
# ----------------
#  
# 
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: gk_CreateCustomLayer.py
Created: 2012xxxx
Modified: 20170622
About: Creates a new feature class with the supplied schema.

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
    ["DATE_NEW","DATE",""],
    ["DATE_MOD","DATE",""],
    ["USER_NAME","TEXT","32"],
    ["ASIAUSER","TEXT","10"],
    ["PREFIX","TEXT","2"],
    ["NAME","TEXT","40"],
    ["SUFFIX","TEXT","4"],
    ["POSTDIR","TEXT","2"],
    ["STREET1","TEXT","64"],
    ["ALIAS","TEXT","64"],
    ["ALIAS2","TEXT","64"],
    ["FROMLEFT","LONG",""],
    ["TOLEFT","LONG",""],
    ["FROMRIGHT","LONG",""],
    ["TORIGHT","LONG",""],
    ["CLASSIFI","TEXT","32"],
    ["ZIP_COMM_E","TEXT","32"],
    ["ZIP_COMM_O","TEXT","32"],
    ["ECOMM","TEXT","32"],
    ["OCOMM","TEXT","32"],
    ["EESN","SHORT",""],
    ["OESN","SHORT",""],
    ["ETELCO","TEXT","4"],
    ["OTELCO","TEXT","4"],
    ["LAST_CHANGE","TEXT","128"],
    ["FLAG","TEXT","2"],
    ["FEATURE_GUID","TEXT","38"],
    ["NOTE1","TEXT","255"],
    ["NOTE2","TEXT","255"],
    ["LANES","SHORT",""],
    ["SURFACE","TEXT","32"],
    ["ONE_WAY","TEXT","1"],
    ["SHOULDER","TEXT","5"],
    ["ROAD_SIGN","TEXT","64"],
    ["DATA_SOURCE","TEXT","16"],
    ["STOP","TEXT","4"],
    ["STREET","TEXT","50"],
    ["ZIP_LEFT","TEXT","5"],
    ["ZIP_RIGHT","TEXT","5"],
    ["CITY","TEXT","40"],
    ["ESN","TEXT","10"],
    ["CENTERXY","TEXT","20"],
    ["UNIQUEID","TEXT","30"],
    ["STATE","TEXT","2"],
    ["STOP2","TEXT","5"],
    ["FRANKLIN","TEXT","1"],
    ["STREET_NAME","TEXT","32"]
    ]


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

# Arguments: input table, [0]field name, [2]field type, [4]precision, [5]scale, [3]length, [1]field alias, is nullable, is required, domain

# for i in L:
	# if i[1] == "TEXT":
		# msg("Adding new TEXT field:   " + str(i[0]))
		# arcpy.AddField_management(FL, i[0], "TEXT", "", "", i[2], i[0], "NULLABLE", "NON_REQUIRED", "")
	# elif i[1] == "SHORT":
		# msg("Adding new SHORT field:  " + str(i[0]))
		# arcpy.AddField_management(FL, i[0], "SHORT", i[3], i[4], "", i[0], "NULLABLE", "NON_REQUIRED", "")
	# elif i[1] == "LONG":
		# msg("Adding new LONG field:   " + str(i[0]))
		# arcpy.AddField_management(FL, i[0], "LONG", i[3], i[4], "", i[0], "NULLABLE", "NON_REQUIRED", "")
	# elif i[1] == "DOUBLE":
		# msg("Adding new DOUBLE field: " + str(i[0]))
		# arcpy.AddField_management(FL, i[0], "DOUBLE", i[3], i[4], "", i[0], "NULLABLE", "NON_REQUIRED", "")
	# elif i[1] == "DATE":
		# msg("Adding new DATE field:   " + str(i[0]))
		# arcpy.AddField_management(FL, i[0], "DATE", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")
		
		
# Arguments: input table, [0]field name, [1]field type, [2]length

for i in L:
	if i[1] == "TEXT":
		msg("Adding new TEXT field:   " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "TEXT", "", "", i[2], i[0], "NULLABLE", "NON_REQUIRED", "")
	elif i[1] == "SHORT":
		msg("Adding new SHORT field:  " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "SHORT", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")
	elif i[1] == "LONG":
		msg("Adding new LONG field:   " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "LONG", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")
	elif i[1] == "DOUBLE":
		msg("Adding new DOUBLE field: " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "DOUBLE", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")
	elif i[1] == "DATE":
		msg("Adding new DATE field:   " + str(i[0]))
		arcpy.AddField_management(FL, i[0], "DATE", "", "", "", i[0], "NULLABLE", "NON_REQUIRED", "")





msg("\n\nDone!\n\n")



	




