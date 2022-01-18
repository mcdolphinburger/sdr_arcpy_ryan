# ===============================================================================================
#
# CodeRoadsForMSAG.py
# Created on: 2012-02-03
# Usage: 
# 
# Description: 
# Codes the COMMUNITY, ESN and EXCHANGE fields based on boundary info
#
# ===============================================================================================

















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
layerRCL = arcpy.GetParameterAsText(0)
layerCOM = arcpy.GetParameterAsText(1)
fldCOM = arcpy.GetParameterAsText(2)
layerESN = arcpy.GetParameterAsText(3)
fldESN = arcpy.GetParameterAsText(4)
layerTEL = arcpy.GetParameterAsText(5)
fldTEL = arcpy.GetParameterAsText(6)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
descRCL = arcpy.Describe(layerRCL)
descCOM = arcpy.Describe(layerCOM)
descESN = arcpy.Describe(layerESN)
descTEL = arcpy.Describe(layerTEL)
fcRCL = descRCL.FeatureClass
fcCOM = descCOM.Featureclass
fcESN = descESN.FeatureClass
fcTEL = descTEL.Featureclass


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg = "\n\n" + layerRCL + "\n" + layerCOM + "\n" + layerESN + "\n" + layerTEL+ "\n" + "\n"
msg(msg)








# ==============================================================================================================
#                                                                                        D O   T H E   W O R K
# ==============================================================================================================





bdy = "<>"
cross = "><"


# Code COMMUNITY
# -------------------------------------------------------------
if layerCom:
	msg("Coding Centerline layer with COMMUNITY values.")
	row, cur = None, None
	cur = arcpy.SearchCursor(layerCOM)
	for row in cur:
		vcom = row.getValue(fldCOM)
		arcpy.SelectLayerByAttribute_management(layerCOM, "NEW_SELECTION", "[" + fldCOM + "] = '" + vcom + "'")
		arcpy.SelectLayerByLocation_management(layerRCL, "WITHIN_CLEMENTINI", layerCOM, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "E911_COMM_E", "\"" + vcom + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "E911_COMM_O", "\"" + vcom + "\"", "VB", "")
		arcpy.SelectLayerByLocation_management(layerRCL, "SHARE_A_LINE_SEGMENT_WITH", layerCOM, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "E911_COMM_E", "\"" + bdy + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "E911_COMM_O", "\"" + bdy + "\"", "VB", "")
		arcpy.SelectLayerByLocation_management(layerRCL, "CROSSED_BY_THE_OUTLINE_OF", layerCOM, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "E911_COMM_E", "\"" + cross + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "E911_COMM_O", "\"" + cross + "\"", "VB", "")
else:
	msg("User opted to skip coding of COMMUNITY values.")
	
# Code ESN
# -------------------------------------------------------------
if layerESN:
	msg("Coding Centerline layer with ESN values.")
	row, cur = None, None
	cur = arcpy.SearchCursor(layerESN)
	for row in cur:
		vesn = int(row.getValue(fldESN))
		arcpy.SelectLayerByAttribute_management(layerESN, "NEW_SELECTION", "[" + fldESN + "] = " + str(vesn))
		arcpy.SelectLayerByLocation_management(layerRCL, "WITHIN_CLEMENTINI", layerESN, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "ESN_E", "\"" + str(vesn) + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "ESN_O", "\"" + str(vesn) + "\"", "VB", "")
		arcpy.SelectLayerByLocation_management(layerRCL, "SHARE_A_LINE_SEGMENT_WITH", layerESN, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "ESN_E", "\"" + str(-1) + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "ESN_O", "\"" + str(-1) + "\"", "VB", "")
		arcpy.SelectLayerByLocation_management(layerRCL, "CROSSED_BY_THE_OUTLINE_OF", layerESN, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "ESN_E", "\"" + str(-2) + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "ESN_O", "\"" + str(-2) + "\"", "VB", "")
else:
	msg("User opted to skip coding of ESN values.")
	
# Code EXCHANGE
# -------------------------------------------------------------
if layerTEL:
	msg("Coding Road layer with Telco Exchange values.")
	row, cur = None, None
	cur = arcpy.SearchCursor(layerTEL)
	for row in cur:
		vtel = row.getValue(fldTEL)
		arcpy.SelectLayerByAttribute_management(layerTEL, "NEW_SELECTION", "[" + fldTEL + "] = '" + vtel + "'")
		arcpy.SelectLayerByLocation_management(layerRCL, "WITHIN_CLEMENTINI", layerTEL, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "EXCHANGE_E", "\"" + vtel + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "EXCHANGE_O", "\"" + vtel + "\"", "VB", "")
		arcpy.SelectLayerByLocation_management(layerRCL, "SHARE_A_LINE_SEGMENT_WITH", layerTEL, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "EXCHANGE_E", "\"" + bdy + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "EXCHANGE_O", "\"" + bdy + "\"", "VB", "")
		arcpy.SelectLayerByLocation_management(layerRCL, "CROSSED_BY_THE_OUTLINE_OF", layerTEL, "", "NEW_SELECTION")
		arcpy.CalculateField_management(layerRCL, "EXCHANGE_E", "\"" + cross + "\"", "VB", "")
		arcpy.CalculateField_management(layerRCL, "EXCHANGE_O", "\"" + cross + "\"", "VB", "")
else:
	msg("User opted to skip coding of TELCO values.")
	



