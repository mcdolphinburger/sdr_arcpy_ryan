# ---------------------------------------------------------------------------
# Shapefile_Merger.py
# Created on: 2012-02-01
#
# Description: 
#
#
#
#
#
# ---------------------------------------------------------------------------

# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime
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
inShapes = arcpy.GetParameterAsText(0)								# delimited list of the three shapefile inputs [Table View]
outName = arcpy.GetParameterAsText(1) + ".shp"				# output shapefile name [String]
outFolder = arcpy.GetParameterAsText(2)								# output folder [Folder]


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
outputdata = outFolder + "\\" + outName
inS = []
for s in inShapes.split(';'):
	inS.append(s)






# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n\n")









# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

msg(inS[2])
msg(outputdata)								# visual feedback, remove when this works
msg("\n\n")

arcpy.Merge_management(inS, outputdata)


arcpy.AddMessage("\n\nDone!\n\n")










