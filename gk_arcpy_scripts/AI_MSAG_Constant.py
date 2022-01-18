# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# MSAG_Constant.py
# Created on: 2012-02-04
#
#
# Description: 
# ----------------
#  
# 
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import arcpy module
# from __future__ import division
import arcpy


def build_rdname(fet):
	rd1 = fet.getValue("PRE_DIR").strip()
	rd2 = fet.getValue("STREET_NAME").strip()
	rd3 = fet.getValue("STREET_TYPE").strip()	
	rd4 = fet.getValue("POST_DIR").strip()
	rn = (rd1 + " " + rd2).strip()
	rn = (rn + " " + rd3).strip()
	rn = (rn + " " + rd4).strip()
	return rn
	
def msgshow(msg):
	arcpy.AddMessage(msg)
	

arcpy.AddMessage("\n" + "\n" + "Creating MSAG Constant Values, AddressIt version 2.2")
arcpy.AddMessage("====================================================" + "\n" + "\n")


# Script parameters
# --------------------------------------------------------------------------------------------------------------
layerRCL = arcpy.GetParameterAsText(0)										# Road centerline feature layer
if layerRCL == '#' or not layerRCL:
   layerRCL = "Roads"  # provide a default value if unspecified
desc1 = arcpy.Describe(layerRCL)
fcRCL = desc1.FeatureClass
fields1 = fcRCL.Fields


# Check centerline layer for MCONST field. Add it if necessary.
# --------------------------------------------------------------------------------------------------------------
fieldexists = "False"
for field in fields1:
	if field.Name == "MCONST":
		fieldexists = "True"
		break
if fieldexists == "False":
	arcpy.AddField_management(layerRCL, "MCONST", "TEXT", "", "", "255", "MSAG CONSTANT", "NULLABLE", "NON_REQUIRED", "")
	
arcpy.AddMessage("MSAG Constant field [MCONST] already exists? " + fieldexists + "\n" + "\n")


# Create and write Range Parity Constants.
# --------------------------------------------------------------------------------------------------------------
arcpy.AddMessage("Creating and writing MSAG constants . . .")
cur = arcpy.UpdateCursor(layerRCL)
for feat in cur:
	rnam = build_rdname(feat)
	come = feat.getValue("E911_COMM_E")
	como = feat.getValue("E911_COMM_O")
	exche = feat.getValue("EXCHANGE_E")
	excho = feat.getValue("EXCHANGE_O")
	esne = str(feat.getValue("ESN_E"))
	esno = str(feat.getValue("ESN_O"))
	mconst = rnam + ":" + come + ":" + como + ":" + exche + ":" + excho + ":" + esne + ":" + esno
	msgshow(mconst)
	
	
	
	feat.MCONST = mconst
	cur.updateRow(feat)

	
		
		
arcpy.AddMessage("\n" + "\n" + "\n")



