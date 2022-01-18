# ===============================================================================================
#
# CodePointWithPoly.py
# Created on: 2015-05-06
# Usage: 
# 
# Description: 
# Codes point features with polygon attribute of the polygon the point is in
#
# ===============================================================================================



# Import arcpy module
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env




def msg(msg):
	arcpy.AddMessage(msg)




# Script arguments
# -------------------------------------------------------------
ptlyr = arcpy.GetParameterAsText(0)			# Point layer containing field needing populating
ptfld = arcpy.GetParameterAsText(1)			# The Point field to be populated
plylyr = arcpy.GetParameterAsText(2)		# Polygon layer containing attributes to populate into points
plyfld = arcpy.GetParameterAsText(3)		# The polygon field with the attributes to populate



# Layer objects
# -------------------------------------------------------------
descADD = arcpy.Describe(layerADD)
descCOM = arcpy.Describe(layerCOM)
descESN = arcpy.Describe(layerESN)
descTEL = arcpy.Describe(layerTEL)
fcADD = descADD.FeatureClass
fcCOM = descCOM.Featureclass
fcESN = descESN.FeatureClass
fcTEL = descTEL.Featureclass

msg = "\n\n" + layerADD + "\n" + layerCOM + "\n" + layerESN + "\n" + layerTEL+ "\n\n"
msg(msg)


# Code COMMUNITY
# -------------------------------------------------------------
msg("Coding Address layer with COMMUNITY values . . .")
ccur = arcpy.SearchCursor(layerCOM)
for featC in ccur:
	vcom = featC.getValue(fldCOM)
	arcpy.SelectLayerByAttribute_management(layerCOM, "NEW_SELECTION", "[" + fldCOM + "] = '" + vcom + "'")
	arcpy.SelectLayerByLocation_management(layerADD, "INTERSECT", layerCOM, "", "NEW_SELECTION")
	arcpy.CalculateField_management(layerADD, "E911_COMM", "\"" + vcom + "\"", "VB", "")
	
# Code ESN
# -------------------------------------------------------------
msg("Coding Address layer with ESN values . . .")
ecur = arcpy.SearchCursor(layerESN)
for featE in ecur:
	vesn = int(featE.getValue(fldESN))
	arcpy.SelectLayerByAttribute_management(layerESN, "NEW_SELECTION", "[" + fldESN + "] = " + str(vesn))
	arcpy.SelectLayerByLocation_management(layerADD, "INTERSECT", layerESN, "", "NEW_SELECTION")
	arcpy.CalculateField_management(layerADD, "ESN", "\"" + str(vesn) + "\"", "VB", "")
	
# Code EXCHANGE
# -------------------------------------------------------------
msg("Coding Address layer with Telco Exchange values . . .")
tcur = arcpy.SearchCursor(layerTEL)
for featT in tcur:
	vtel = featT.getValue(fldTEL)
	arcpy.SelectLayerByAttribute_management(layerTEL, "NEW_SELECTION", "[" + fldTEL + "] = '" + vtel + "'")
	arcpy.SelectLayerByLocation_management(layerADD, "INTERSECT", layerTEL, "", "NEW_SELECTION")
	arcpy.CalculateField_management(layerADD, "EXCHANGE", "\"" + vtel + "\"", "VB", "")


msg("\n\nDone!\n\n")


