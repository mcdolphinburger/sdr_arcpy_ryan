#
# RangeLowHigh.py
# Created on: 2012-02-04
#
#
# Description: 
# ----------------
#  
# 
# 
# 
# *******************************************************************************************************
# *******************************************************************************************************


#                                                                                          Import Modules
# -------------------------------------------------------------------------------------------------------
# from __future__ import division
import arcpy


#                                                                                               Functions
# -------------------------------------------------------------------------------------------------------

def FieldExists(fields, fname):
	doesexist = "FALSE"
	for fld in fields:
		if fld.Name == fname:
			doesexist = "TRUE"
	return doesexist

def CreateTextField(lyr, fname, len):
	arcpy.AddField_management(lyr, fname, "TEXT", "", "", len, fname, "NULLABLE", "NON_REQUIRED", "")
	
def CreateLongField(lyr, fname):
	arcpy.AddField_management(lyr, fname, "LONG", "", "", "", fname, "NULLABLE", "NON_REQUIRED", "")
	
def CalculatePCONST(x1, x2, y1, y2):
	if x1 == 0:
		cLF = "X"
	elif x1/2 == int(x1/2):
		cLF = "E"
	else:
		cLF = "O"
	if x2 == 0:
		cLT = "X"
	elif x2/2 == int(x2/2):
		cLT = "E"
	else:
		cLT = "O"
	if y1 == 0:
		cRF = "X"
	elif y1/2 == int(y1/2):
		cRF = "E"
	else:
		cRF = "O"
	if y2 == 0:
		cRT = "X"
	elif y2/2 == int(y2/2):
		cRT = "E"
	else:
		cRT = "O"
		
	return cLF + cLT + cRF + cRT

	
#                                                                                               B E G I N
# -------------------------------------------------------------------------------------------------------

arcpy.AddMessage("\n\nCalculating Range LOW/HIGH Values")
arcpy.AddMessage("=================================" + "\n\n")


#                                                                                        Script arguments
# -------------------------------------------------------------------------------------------------------
FL1 = arcpy.GetParameterAsText(0)
LF = arcpy.GetParameterAsText(1)
LT = arcpy.GetParameterAsText(2)
RF = arcpy.GetParameterAsText(3)
RT = arcpy.GetParameterAsText(4)




#                                                                               Initialize some variables
# -------------------------------------------------------------------------------------------------------
desc1 = arcpy.Describe(FL1)
fc1 = desc1.FeatureClass
fields1 = fc1.Fields
PC = "PCONST"



#                                        Check centerline layer for required fields, add them if necessary
# --------------------------------------------------------------------------------------------------------
if FieldExists(fields1, "PCONST") != "TRUE":
	CreateTextField(FL1, "PCONST", "4")
	arcpy.AddMessage("Range Parity Constant [PCONST] exists?  FALSE (field created)")
else:
	arcpy.AddMessage("Range Parity Constant [PCONST] exists?  TRUE")
	
if FieldExists(fields1, "RNG_LOW") != "TRUE":
	CreateLongField(FL1, "RNG_LOW")
	arcpy.AddMessage("Low Range [RNG_LOW] exists?  FALSE (field created)")
else:
	arcpy.AddMessage("Low Range [RNG_LOW] exists?  TRUE")
	
if FieldExists(fields1, "RNG_HIGH") != "TRUE":
	CreateLongField(FL1, "RNG_HIGH")
	arcpy.AddMessage("High Range [RNG_HIGH] exists?  FALSE (field created)")
else:
	arcpy.AddMessage("High Range [RNG_HIGH] exists?  TRUE")
	

#                                                                  Create and write Range Parity Constants
# --------------------------------------------------------------------------------------------------------
arcpy.AddMessage("\nUpdating Range Parity Constants...")
cur1 = arcpy.UpdateCursor(FL1)
for feat1 in cur1:
	vLF = float(feat1.getValue(LF))
	vLT = float(feat1.getValue(LT))
	vRF = float(feat1.getValue(RF))
	vRT = float(feat1.getValue(RT))
	feat1.PCONST = CalculatePCONST(vLF, vLT, vRF, vRT)	
	cur1.updateRow(feat1)
	

#                                                                                  Writing LOW/HIGH values
# --------------------------------------------------------------------------------------------------------
arcpy.AddMessage("Updating/Calculating LOW and HIGH fields...")
cur2 = arcpy.UpdateCursor(FL1)	
for feat2 in cur2:
	pc = feat2.getValue("PCONST")
	pcl = pc[0:2]
	pcr = pc[2:len(pc)]
	vLF = float(feat2.getValue(LF))
	vLT = float(feat2.getValue(LT))
	vRF = float(feat2.getValue(RF))
	vRT = float(feat2.getValue(RT))
	if pc == "XXXX":
		lw = 0
		hi = 0
	elif pcl != "XX" and pcr == "XX":
		lw = min(vLF, vLT)
		hi = max(vLF, vLT)
	elif pcl == "XX" and pcr != "XX":
		lw = min(vRF, vRT)
		hi = max(vRF, vRT)
	else:
		lw = min(vLF, vLT, vRF, vRT)
		hi = max(vLF, vLT, vRF, vRT)
	feat2.RNG_LOW = lw
	feat2.RNG_HIGH = hi
	cur2.updateRow(feat2)

	
		
		
arcpy.AddMessage("\n" + "\n" + "\n")



