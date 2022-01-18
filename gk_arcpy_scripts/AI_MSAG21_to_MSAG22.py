# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# MSAG21_to_MSAG22.py
# Created on: 2012-08-24
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
import sys, os, arcpy, string, datetime


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)

def FieldExists(fields, fname):
	doesexist = "FALSE"
	for fld in fields:
		if fld.Name == fname:
			doesexist = "TRUE"
	return doesexist

	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrR = arcpy.GetParameterAsText(0)			# The Road Centerline layer
doC = arcpy.GetParameterAsText(1)
doN = arcpy.GetParameterAsText(2)
doX = arcpy.GetParameterAsText(3)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
desc = arcpy.Describe(lyrR)
fc = desc.FeatureClass
fields = fc.Fields


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nConverting version 2.1 MSAG fields to version 2.2 MSAG fields")
msg("-------------------------------------------------------------\n\n")


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if doC == "YES":
	msg("Updating AddressIt 2.2 Community fields . . .")
	cur = arcpy.UpdateCursor(lyrR)
	for feat in cur:
		B = feat.getValue("COMM")
		E = feat.getValue("ECOMM")
		D = feat.getValue("OCOMM")
		if B == "":
			feat.setValue("E911_COMM_E", E)
			feat.setValue("E911_COMM_O", D)
			cur.updateRow(feat)
		else:
			feat.setValue("E911_COMM_E", B)
			feat.setValue("E911_COMM_O", B)
			cur.updateRow(feat)
del cur, feat
			
			
			
if doN == "YES":
	msg("Updating AddressIt 2.2 ESN fields . . .")
	cur = arcpy.UpdateCursor(lyrR)
	for feat in cur:
		B = feat.getValue("ESN")
		E = feat.getValue("EESN")
		D = feat.getValue("OESN")
		if B == 0:
			feat.setValue("ESN_E", E)
			feat.setValue("ESN_O", D)
			cur.updateRow(feat)
		else:
			feat.setValue("ESN_E", B)
			feat.setValue("ESN_O", B)
			cur.updateRow(feat)
del cur, feat
			
			
if doX == "YES":
	msg("Updating AddressIt 2.2 Exchange fields . . .")
	cur = arcpy.UpdateCursor(lyrR)
	for feat in cur:
		B = feat.getValue("TELCO")
		E = feat.getValue("ETELCO")
		D = feat.getValue("OTELCO")
		if B == "":
			feat.setValue("EXCHANGE_E", E)
			feat.setValue("EXCHANGE_O", D)
			cur.updateRow(feat)
		else:
			feat.setValue("EXCHANGE_E", B)
			feat.setValue("EXCHANGE_O", B)
			cur.updateRow(feat)
del cur, feat



arcpy.AddMessage("\n\nDone!\n\n")



	




