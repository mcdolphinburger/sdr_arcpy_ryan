
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: compactgeodatabases.py
Created: 20180308
Modified: 20180308
About: Compacts a list of active geodatabases.

"""



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
thedate = arcpy.GetParameter(0)			# The current date




## Initialize main variables.
## --------------------------------------------------------------------------------------------------------------

CL = []
CL = [
	["MO eCOP Webmap", "E:\Data\SDR\Projects_Data\Missouri\MO_eCOP_Webmap\GIS\LIVE\Missouri_eCOP_Live.gdb"],
	["Carter County, MO", "C:\data\SDR\Projects_Data\Missouri\MO_Foothills\LIVE\GIS\Foothills_Carter_Live.gdb"],
	["Ripley County, MO", "C:\data\SDR\Projects_Data\Missouri\MO_Foothills\LIVE\GIS\Foothills_Ripley_Live.gdb"],
	["Wayne County, MO", "C:\data\SDR\Projects_Data\Missouri\MO_Foothills\LIVE\GIS\Foothills_Wayne_Live.gdb"],
	["Dade County, MO", "C:\data\SDR\Projects_Data\Missouri\MO_Dade_County\LIVE\GIS\AddressIt23.gdb"],
	["Mercy Health Systems, Main", "C:\data\SDR\Projects_Data\Missouri\MO_Mercy_Health_Systems\Data\Live_File_Geodatabase\Mercy_Health_Systems.gdb"],
	["Mercy Health Systems, Benton", "C:\data\SDR\Projects_Data\Missouri\MO_Mercy_Health_Systems\Data\Live_File_Geodatabase\Mercy_Health_Systems_Benton.gdb"],
	["Mercy Health Systems, Greene", "C:\data\SDR\Projects_Data\Missouri\MO_Mercy_Health_Systems\Data\Live_File_Geodatabase\Mercy_Health_Systems_Greene.gdb"],
	["Newton County, MO", "C:\data\SDR\Projects_Data\Missouri\MO_Newton_County\LIVE\GIS\Newton_Live.gdb"],
	["Oregon County, MO", "C:\data\SDR\Projects_Data\Missouri\MO_Oregon_County\LIVE\GIS\Oregon_County.gdb"],
	["Cotton County, OK", "C:\data\SDR\Projects_Data\Oklahoma\OK_Cotton_County\LIVE\GIS\Cotton_Live.gdb"],
	["OK eCOP Webmap", "C:\data\SDR\Projects_Data\Oklahoma\OK_eCOP_Webmap\GIS\_Live\OK_eCOP_Live.gdb"],
	["McCurtain County, OK", "C:\data\SDR\Projects_Data\Oklahoma\OK_McCurtain_County\LIVE\GIS\McCurtain_LIVE.gdb"],
	["Pushmataha County, OK", "C:\data\SDR\Projects_Data\Oklahoma\OK_Pushmataha_County\LIVE\GIS\Pushmataha_LIVE.gdb"]
	]
	
	






# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nCompacting the active project geodatabases.\n--------------------------------------------------\n\n")




# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

for r in CL:
	msg("  Compacting: " + r[0])
	arcpy.Compact_management(r[1])




msg("\n\nDone!\n\n")



	




