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
WS = arcpy.GetParameterAsText(0)
LN = arcpy.GetParameterAsText(1)
FL = arcpy.GetParameterAsText(2)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
L = []
L = [
    ["JOIN_ID","TEXT","16","0","0"],
    ["SOURCE","TEXT","50","0","0"],
		["UPDATED","DATE","N/A","0","0"],
    ["PREDIR","TEXT","2","0","0"],
    ["PRETYPE","TEXT","4","0","0"],
    ["STREETNAME","TEXT","40","0","0"],
    ["STREETTYPE","TEXT","4","0","0"],
    ["SUFFIX","TEXT","2","0","0"],
    ["L_FROM_ADD","LONG","N/A","0","0"],
    ["L_TO_ADD","LONG","N/A","0","0"],
    ["R_FROM_ADD","LONG","N/A","0","0"],
    ["R_TO_ADD","LONG","N/A","0","0"],
    ["L_COMMUNITY","TEXT","40","0","0"],
    ["R_COMMUNITY","TEXT","40","0","0"],
    ] 

  
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n\n")


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

msg("                          Field Name, Field Type, Length, Precision, Scale")
msg("-------------------------------------------------------------------------------")
for i in range(0, ct):
	R = L[i]
	if R[1] == "TEXT":
		msg("Adding new TEXT field:   " + str(R))
		arcpy.AddField_management(FL, R[0], "TEXT", "", "", R[2], R[0], "NULLABLE", "NON_REQUIRED", "")
	elif R[1] == "SHORT":
		msg("Adding new SHORT field:  " + str(R))
		arcpy.AddField_management(FL, R[0], "SHORT", R[3], R[4], "", R[0], "NULLABLE", "NON_REQUIRED", "")
	elif R[1] == "LONG":
		msg("Adding new LONG field:   " + str(R))
		arcpy.AddField_management(FL, R[0], "LONG", R[3], R[4], "", R[0], "NULLABLE", "NON_REQUIRED", "")
	elif R[1] == "DOUBLE":
		msg("Adding new DOUBLE field: " + str(R))
		arcpy.AddField_management(FL, R[0], "DOUBLE", R[3], R[4], "", R[0], "NULLABLE", "NON_REQUIRED", "")
	elif R[1] == "DATE":
		msg("Adding new DATE field:   " + str(R))
		arcpy.AddField_management(FL, R[0], "DATE", "", "", "", R[0], "NULLABLE", "NON_REQUIRED", "")


		





msg("\n\n\n")



	




