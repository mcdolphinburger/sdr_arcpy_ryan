# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# BackupLocalData.py
# Created on: 2014-04-29
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
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def GeodatabaseSelected(s):
	if len(s) > 0:
		return True
	else:
		return False
		
def BuildNewPath(n):
	x = n[:-4]
	x = x + "_" + yyyymmdd + "_" + init + n[-4:]
	x = outfolder + "\\" + x
	return x


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
gdbP = arcpy.GetParameterAsText(0)						# Pushmataha geodatabase
gdbM = arcpy.GetParameterAsText(1)						# McCurtain geodatabase
gdbS = arcpy.GetParameterAsText(2)						# Stephens geodatabase
outfolder = arcpy.GetParameterAsText(3)				# the destination folder for the backups
init = arcpy.GetParameterAsText(4)						# user's initials



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
yyyymmdd = time.strftime("%Y") + time.strftime("%m") + time.strftime("%d")
pathP, fileP = os.path.split(gdbP)
pathM, fileM = os.path.split(gdbM)
pathS, fileS = os.path.split(gdbS)


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nThe Output Backup location is:\n---------------------------------------------------")
msg(outfolder + "\n")











# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# arcpy.Copy_management (in_data, out_data, {data_type})

if GeodatabaseSelected(gdbP):
	msg("Copying Pushmataha geodatabase from Local to Backup location.")
	N = BuildNewPath(fileP)
	arcpy.Copy_management(gdbP, N)
else:
	msg("Skipping the Pushmataha Geodatabase.")
	
if GeodatabaseSelected(gdbM):
	msg("Copying McCurtain geodatabase from Local to Backup location.")
	N = BuildNewPath(fileM)
	arcpy.Copy_management(gdbM, N)
else:
	msg("Skipping the McCurtain Geodatabase.")
	
if GeodatabaseSelected(gdbS):
	msg("Copying Stephens geodatabase from Local to Backup location.")
	N = BuildNewPath(fileS)
	arcpy.Copy_management(gdbS, N)
else:
	msg("Skipping the Stephens Geodatabase.")


msg("\n\nDone!\n\n")



	




