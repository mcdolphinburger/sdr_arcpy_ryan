# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# _Script.py
# Created on: 2012-11-09
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
from arcpy import env, mapping


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
msg("hey")

# Script arguments
# --------------------------------------------------------------------------------------------------------------
# lyr = arcpy.GetParameterAsText(0)				# Feature Layer object



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
# d = arcpy.Describe(theFC)
# spref = d.spatialReference
FC = "C:\data\SDR\Projects_Data\Oklahoma\OK_McCurtain_County\LIVE\GIS\McCurtain_LIVE.gdb\AddressIt\Centerlines"
arcpy.MakeFeatureLayer_management(FC, "layer")
symblyr = "C:\data\Scripting_Python\Layer_Symbology_Files\ROADS_Classification.lyr"

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	


arcpy.ApplySymbologyFromLayer_management("layer", symblyr)


# msg("\n\n")
# msg(spref.name)
# msg(spref.alias)
# msg(spref.abbreviation)
# msg(spref.domain)
# msg(spref.type)
# msg(spref.PCSName)








# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


			




arcpy.AddMessage("\n\n\n")



	




