# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# BackupProjectData.py
# Created on: 2012-11-08
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
buMCC = arcpy.GetParameter(0)				# Backup McCurtain live geodatabase YES/NO
comMCC = arcpy.GetParameter(1)				# boolean on compact mccurtain geodatabase
buCUS = arcpy.GetParameter(2)				# Backup Custer live geodatabase YES/NO
comCUS = arcpy.GetParameter(3)				# boolean on compact mccurtain geodatabase
buPUS = arcpy.GetParameter(4)				# Backup Push live geodatabase YES/NO
comPUS = arcpy.GetParameter(5)				# boolean on compact mccurtain geodatabase
strDate = arcpy.GetParameterAsText(6)		# Date string to append to backup file name





# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
pathMCC = "W:\Projects_Data\McCurtain_County_Oklahoma\LIVE"
bupathMCC = "W:\Projects_Data\McCurtain_County_Oklahoma\ARCHIVE"
gdbMCC = "W:\Projects_Data\McCurtain_County_Oklahoma\LIVE\MCCURTAIN_LIVE.mdb"
namMCC = "MCCURTAIN_LIVE"
pathCUS = "W:\Projects_Data\Custer_ID\LIVE"
bupathCUS = "W:\Projects_Data\Custer_ID\ARCHIVE"
gdbCUS = "W:\Projects_Data\Custer_ID\LIVE\Custer_LIVE.mdb"
namCUS = "Custer_LIVE"
pathPUS = "W:\Projects_Data\Pushmataha_County_Oklahoma\LIVE\GIS"
bupathPUS = "W:\Projects_Data\Pushmataha_County_Oklahoma\ARCHIVE"
gdbPUS = "W:\Projects_Data\Pushmataha_County_Oklahoma\LIVE\GIS\Pushmataha_LIVE.mdb"
namPUS = "Pushmataha_LIVE"



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\n\nBacking up project data to project Archive folders\n-----------------------------------------------------\n\n")








# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if comMCC:
	msg("Compacting McCurtain Live geodatabase")
	arcpy.Compact_management(gdbMCC)
if buMCC:
	msg("Backing up McCurtain Live geodatabase")
	arcpy.Copy_management(gdbMCC, bupathMCC + "\\" + namMCC + "_" + strDate + ".mdb")

if comCUS:
	msg("Compacting Custer Live geodatabase")
	arcpy.Compact_management(gdbCUS)
if buCUS:
	msg("Backing up Custer Live geodatabase")
	arcpy.Copy_management(gdbCUS, bupathCUS + "\\" + namCUS + "_" + strDate + ".mdb")
	
if comPUS:
	msg("Compacting Push Live geodatabase")
	arcpy.Compact_management(gdbPUS)
if buPUS:
	msg("Backing up Push Live geodatabase")
	arcpy.Copy_management(gdbPUS, bupathPUS + "\\" + namPUS + "_" + strDate + ".mdb")



arcpy.AddMessage("\n\n\n")



	




