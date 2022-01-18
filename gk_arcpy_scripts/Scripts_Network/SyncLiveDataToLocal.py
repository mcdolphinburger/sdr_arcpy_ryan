# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# SyncLiveDataToLocal.py
# Created on: 2014-04-02
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
buName = arcpy.GetParameterAsText(0)			  # Text value: geodatabase name



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------

netgdb = "W:\Projects_Data\OK_McCurtain_County\LIVE\GIS\McCurtain_LIVE.gdb"
locgdb = "C:\data\SDR\Projects_Data\OK_McCurtain_County\LIVE\GIS\McCurtain_LIVE.gdb"
locgdbrn = "C:\data\SDR\Projects_Data\OK_McCurtain_County\LIVE\GIS\McCurtain_LIVE_x.gdb"




# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nUpdating Local McCurtain Live geodatabase from the Network")
msg("--------------------------------------------------------------------\n\n")




# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# Rename existing Live McCurtain Geodatabase
# ------------------------------------------------------------------------------
msg("    Re-naming existing Live McCurtain geodatabase.")
arcpy.Rename_management (locgdb, locgdbrn, "")
	

arcpy.AddMessage("\nDone!\n")
