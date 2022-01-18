# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# gk_CreatePLSSFields.py
# Created on: 2014-03-16
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
lyr = arcpy.GetParameterAsText(0)



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nAdding Fields to PLSS layer\n")


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

arcpy.AddField_management(lyr, "TSP1", "SHORT", "", "", "", "TSP1", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "TSP2", "TEXT", "", "", "2", "TSP2", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "TSP3", "TEXT", "", "", "3", "TSP3", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "NS", "TEXT", "", "", "1", "NS", "NULLABLE", "NON_REQUIRED", "")

arcpy.AddField_management(lyr, "RNG1", "SHORT", "", "", "", "RNG1", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "RNG2", "TEXT", "", "", "2", "RNG2", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "RNG3", "TEXT", "", "", "3", "RNG3", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "EW", "TEXT", "", "", "1", "EW", "NULLABLE", "NON_REQUIRED", "")

arcpy.AddField_management(lyr, "SEC1", "SHORT", "", "", "", "SEC1", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "SEC2", "TEXT", "", "", "2", "SEC2", "NULLABLE", "NON_REQUIRED", "")

arcpy.AddField_management(lyr, "TSPRNG", "TEXT", "", "", "9", "TSPRNG", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "TSPRNGSEC", "TEXT", "", "", "12", "TSPRNGSEC", "NULLABLE", "NON_REQUIRED", "")





msg("\nDone!\n")



	




