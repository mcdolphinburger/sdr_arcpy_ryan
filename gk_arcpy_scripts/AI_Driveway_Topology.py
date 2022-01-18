# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Driveway_Topology.py
# Created on: 2013-01-01
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
import sys, arcpy, string, datetime
from arcpy import mapping


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
	
def FieldExists(fname):
	doesexist = False
	for fld in arcpy.ListFields(lyrD):
		if fld.name == fname:
			doesexist = True
	return doesexist
  
def GetSelectionCount(lyr):
	return int(arcpy.GetCount_management(lyr).getOutput(0))
	
# Tests a layer to see if it has a selection. Returns TRUE if there is an existing selection, and
# returns FALSE if there is no selection.
# -------------------------------------------------------------------------------------------------
def SelectionExists(lyr):
	d = arcpy.Describe(lyr)
	if not d.FIDSet  == '':
		return True
	else:
		return False


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrD = arcpy.GetParameterAsText(0)
lyrR = arcpy.GetParameterAsText(1)
lyrA = arcpy.GetParameterAsText(2)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
lyrDS = "Driveway_Selection_Layer"



# ==============================================================================================================
#                                                                                         D O   T H E   W O R K
# ==============================================================================================================

try:

	# Delete the temporary in-memory layer, if it exists
	# -----------------------------------------------------------------------------------------------------------------
	if arcpy.Exists(lyrDS):
		msg("Deleting virtual Driveway Selection layer.\n")
		arcpy.Delete_management(lyrDS)


	# Make sure the needed fields are present. Add them if needed.
	# -----------------------------------------------------------------------------------------------------------------
	msg("Checking for the right fields.")

	if FieldExists("toADDS"):
		msg("  * The field toADDS exists?   TRUE")
	else:
		arcpy.AddField_management(lyrD, "toADDS", "TEXT", "", "", "32", "toADDS", "NULLABLE", "NON_REQUIRED", "")
		msg("  * The field toADDS exists?   FALSE, field created")
		
	if FieldExists("toROADS"):
		msg("  * The field toROADS exists?   TRUE")
	else:
		arcpy.AddField_management(lyrD, "toROADS", "TEXT", "", "", "32", "toROADS", "NULLABLE", "NON_REQUIRED", "")
		msg("  * The field toROADS exists?   FALSE, field created")
		
	if FieldExists("toBOTH"):
		msg("  * The field toBOTH exists?   TRUE\n")
	else:
		arcpy.AddField_management(lyrD, "toBOTH", "TEXT", "", "", "32", "toBOTH", "NULLABLE", "NON_REQUIRED", "")
		msg("  * The field toBOTH exists?   FALSE, field created\n")
		
		
	# Clear selections from addresses and roads, if any.
	# -----------------------------------------------------------------------------------------------------------------
	arcpy.SelectLayerByAttribute_management(lyrA, "CLEAR_SELECTION", "")
	arcpy.SelectLayerByAttribute_management(lyrR, "CLEAR_SELECTION", "")


	# If driveway layer selection count is greater than zero, create a selection layer based on the current 
	# selection. Otherwise, make the selection layer equal to the entire driveway layer.
	# -----------------------------------------------------------------------------------------------------------------
	if SelectionExists(lyrD):
		msg("Creating virtual Driveway Selection layer.\n")
		arcpy.MakeFeatureLayer_management(lyrD, lyrDS)
	else:
		msg("Using existing Driveway layer.\n")
		lyrDS = lyrD
	arcpy.SelectLayerByAttribute_management(lyrD, "CLEAR_SELECTION", "")
	arcpy.SelectLayerByAttribute_management(lyrDS, "CLEAR_SELECTION", "")


	# =================================================================================================================
	# Evaluating and calculating Driveway vs Address Point topology
	# =================================================================================================================
	msg("Checking Driveways against Address Points.")

	msg("  * Selecting Driveways that intersect an address point.")
	arcpy.SelectLayerByLocation_management(lyrDS, "INTERSECT", lyrA, "", "NEW_SELECTION")
	if GetSelectionCount(lyrDS) > 0:
		msg("  * Calculating those selected driveway features as GOOD.")
		arcpy.CalculateField_management(lyrDS, "toADDS", "\"GOOD\"", "PYTHON", "")
		msg("  * Switching the selection on the driveways.")
		arcpy.SelectLayerByAttribute_management(lyrDS, "SWITCH_SELECTION", "")
		msg("  * Calculating this selection of driveways as OFF.")
		arcpy.CalculateField_management(lyrDS, "toADDS", "\"OFF\"", "PYTHON", "")
		msg("  * Clearing any remaining selection on the driveways.\n")
		arcpy.SelectLayerByAttribute_management(lyrDS, "CLEAR_SELECTION", "")
	else:
		msg("  * No driveways were selected, so calculating all driveways as OFF.\n")
		arcpy.CalculateField_management(lyrDS, "toADDS", "\"OFF\"", "PYTHON", "")


		
	# # =================================================================================================================	
	# # Evaluating and calculating Driveway vs Road Centerline topology
	# # =================================================================================================================
	# msg("Checking Driveways against Road Centerlines.")

	# # Select all driveway features that intersect a centerline feature. These will either be GOOD or OVER. If they don't
	# # intersect then they must be UNDER.
	# msg("  * Selecting driveways that intersect the centerlines.")
	# arcpy.SelectLayerByLocation_management(lyrDS, "INTERSECT", lyrR, "", "NEW_SELECTION")
	# msg("  * Calculating the intersected driveways as ISECT.")
	# arcpy.CalculateField_management(lyrDS, "toROADS", "\"ISECT\"", "PYTHON", "")
	# msg("  * Switching the selection on driveways.")
	# arcpy.SelectLayerByAttribute_management(lyrDS, "SWITCH_SELECTION", "")
	# msg("  * Calculating all driveways that didn't intersect a centerline as UNDER.")
	# arcpy.CalculateField_management(lyrDS, "toROADS", "\"UNDER\"", "PYTHON", "")

	# # Now select all driveway features that intersected a centerline feature. If they cross the outline of a centerline
	# # feature then they are OVER.
	# msg("  * Selecting driveways that are snapped to a centerline.")
	# arcpy.SelectLayerByLocation_management(lyrDS, "BOUNDARY_TOUCHES", lyrR, "", "NEW_SELECTION")
	# msg("  * Calculating this selection as GOOD.")
	# arcpy.CalculateField_management(lyrDS, "toROADS", "\"GOOD\"", "PYTHON", "")
	# msg("  * Selecting all driveways still marked as ISECT.")
	# arcpy.SelectLayerByAttribute_management(lyrDS, "NEW_SELECTION", "[toROADS] = 'ISECT'")
	# msg("  * Calculating this selection as OVER.")
	# arcpy.CalculateField_management(lyrDS, "toROADS", "\"OVER\"", "PYTHON", "")
	# msg("  * Clearing any remaining selection on the driveways.\n")
	# arcpy.SelectLayerByAttribute_management(lyrDS, "CLEAR_SELECTION", "")

	msg("Calculating the combination of toADD values and toROADS values.\n")
	arcpy.CalculateField_management(lyrDS, "toBOTH", "[toADDS] & \"-\" & [toROADS]", "VB", "")

	# msg("Clearing all selections.\n")
	# arcpy.SelectLayerByAttribute_management(lyrD, "CLEAR_SELECTION", "")
	# arcpy.SelectLayerByAttribute_management(lyrDS, "CLEAR_SELECTION", "")
	# arcpy.SelectLayerByAttribute_management(lyrA, "CLEAR_SELECTION", "")
	# arcpy.SelectLayerByAttribute_management(lyrR, "CLEAR_SELECTION", "")	
		
	if arcpy.Exists("Driveway_Selection_Layer"):
		msg("Deleting virtual Driveway Selection layer")
		arcpy.Delete_management(lyrDS)


	msg("\n\nDone!\n\n")


except Exception as e:
	msg("\nThis script encountered a fatal error. Fuck.\n" + e.message)
	if arcpy.Exists("Driveway_Selection_Layer"):
		msg("\nDeleting virtual Driveway Selection layer.\n")
		arcpy.Delete_management(lyrDS)



	




