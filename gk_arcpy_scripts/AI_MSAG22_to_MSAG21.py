# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# AI_MSAG22_to_MSAG21.py
# Created on: 2012-07-30
#
#
# Description: 
# ----------------
#  
# Converts the Community, ESN and Exchange fields from the AddressIt 2.2 model to the AddressIt 2.1 model 
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
	for fld in fields:
		if fld.name == fname:
			return True
	return False
	
# full shapefile path, name, type, precision, scale, length, alias)
def CreateMyField(lyr, n, t, p, s, l, a):
	arcpy.AddField_management(lyr, n, t, p, s, l, a, "NULLABLE", "NON_REQUIRED", "")

	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrR = arcpy.GetParameterAsText(0)
doC = arcpy.GetParameter(1)
doN = arcpy.GetParameter(2)
doX = arcpy.GetParameter(3)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyrR)


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nAdding/Updating AddressIt 2.1 MSAG fields based on AddressIt 2.2 MSAG fields")
msg("-----------------------------------------------------------------------------\n\n")


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if doC:
	msg("Updating AddressIt 2.1 Community fields . . .")
	if not FieldExists(fields, "COMM"):
		msg("  AddressIt 2.1 field COMM doesn't exist. Creating it.")
		CreateMyField(lyrR, "COMM", "TEXT", "", "", "32", "COMM")
	if not FieldExists(fields, "ECOMM"):
		msg("  AddressIt 2.1 field ECOMM doesn't exist. Creating it.")
		CreateMyField(lyrR, "ECOMM", "TEXT", "", "", "32", "ECOMM")
	if not FieldExists(fields, "OCOMM"):
		msg("  AddressIt 2.1 field OCOMM doesn't exist. Creating it.")
		CreateMyField(lyrR, "OCOMM", "TEXT", "", "", "32", "OCOMM")
	cur = arcpy.UpdateCursor(lyrR)
	for feat in cur:
		cmE = feat.getValue("E911_COMM_E")
		cmO = feat.getValue("E911_COMM_O")
		if cmE == cmO:
			feat.setValue("COMM", cmE)
			feat.setValue("ECOMM", "")
			feat.setValue("OCOMM", "")
			cur.updateRow(feat)
		else:
			feat.setValue("COMM", "")
			feat.setValue("ECOMM", cmE)
			feat.setValue("OCOMM", cmO)		
			cur.updateRow(feat)

del cur, feat
			
			
if doN:
	msg("Updating AddressIt 2.1 ESN fields . . .")
	if not FieldExists(fields, "ESN"):
		msg("  AddressIt 2.1 field ESN doesn't exist. Creating it.")
		CreateMyField(lyrR, "ESN", "LONG", "", "", "", "ESN")
	if not FieldExists(fields, "EESN"):
		msg("  AddressIt 2.1 field EESN doesn't exist. Creating it.")
		CreateMyField(lyrR, "EESN", "LONG", "", "", "", "EESN")
	if not FieldExists(fields, "OESN"):
		msg("  AddressIt 2.1 field OESN doesn't exist. Creating it.")
		CreateMyField(lyrR, "OESN", "LONG", "", "", "", "OESN")
	cur = arcpy.UpdateCursor(lyrR)
	for feat in cur:
		esE = feat.getValue("ESN_E")
		esO = feat.getValue("ESN_O")
		if esE == esO:
			feat.setValue("ESN", esE)
			feat.setValue("EESN", 0)
			feat.setValue("OESN", 0)
			cur.updateRow(feat)
		else:
			feat.setValue("ESN", 0)
			feat.setValue("EESN", esE)
			feat.setValue("OESN", esO)		
			cur.updateRow(feat)
del cur, feat
			
			
if doX:
	msg("Updating AddressIt 2.1 Exchange fields . . .")
	if not FieldExists(fields, "TELCO"):
		msg("  AddressIt 2.1 field TELCO doesn't exist. Creating it.")
		CreateMyField(lyrR, "TELCO", "TEXT", "", "", "4", "TELCO")
	if not FieldExists(fields, "ETELCO"):
		msg("  AddressIt 2.1 field ETELCO doesn't exist. Creating it.")
		CreateMyField(lyrR, "ETELCO", "TEXT", "", "", "4", "ETELCO")
	if not FieldExists(fields, "OTELCO"):
		msg("  AddressIt 2.1 field OTELCO doesn't exist. Creating it.")
		CreateMyField(lyrR, "OTELCO", "TEXT", "", "", "4", "OTELCO")
	cur = arcpy.UpdateCursor(lyrR)
	for feat in cur:
		exE = feat.getValue("EXCHANGE_E")
		exO = feat.getValue("EXCHANGE_O")
		if exE == exO:
			feat.setValue("TELCO", exE)
			feat.setValue("ETELCO", "")
			feat.setValue("OTELCO", "")
			cur.updateRow(feat)
		else:
			feat.setValue("TELCO", "")
			feat.setValue("ETELCO", exE)
			feat.setValue("OTELCO", exO)		
			cur.updateRow(feat)
del cur, feat



arcpy.AddMessage("\n\n\n")



	




