# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# UpdateAnyRoadName.py
# Created on: 2014-05-01
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


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(fields, fname):
	doesexist = False
	for fld in fields:
		if fld.name == fname:
			doesexist = True
	return doesexist
	
def CalculateRoadName(rn1, rn2, rn3, rn4, rn5):
	rn = (rn1 + " " + rn2).strip()
	rn = (rn + " " + rn3).strip()
	rn = (rn + " " + rn4).strip()
	rn = (rn + " " + rn5).strip()
	return rn


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------
msg("\n\nCalculating/Updating Compiled Road Name\n---------------------------------------------------------------\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
indata = arcpy.GetParameterAsText(0)		# input feature layer
fd1 = arcpy.GetParameterAsText(1)			# pre directional
fd2 = arcpy.GetParameterAsText(2)			# pre type
fd3 = arcpy.GetParameterAsText(3)			# street name
fd4 = arcpy.GetParameterAsText(4)			# street type
fd5 = arcpy.GetParameterAsText(5)			# post directional
fd6 = arcpy.GetParameterAsText(6)			# complete street name
trm = arcpy.GetParameter(7)					# trim fields yes/no

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fds = arcpy.ListFields(indata)




# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================




# Trimming all road name fields in the layer
# --------------------------------------------------------------------------------------------------------------
if trm:
	msg("Trimming layer road name fields...")
	if fd1:
		arcpy.CalculateField_management(indata, fd1, "!" + fd1 + "!.strip()", "PYTHON", "")
	if fd2:
		arcpy.CalculateField_management(indata, fd2, "!" + fd2 + "!.strip()", "PYTHON", "")
	arcpy.CalculateField_management(indata, fd3, "!" + fd3 + "!.strip()", "PYTHON", "")
	if fd4:
		arcpy.CalculateField_management(indata, fd4, "!" + fd4 + "!.strip()", "PYTHON", "")
	if fd5:
		arcpy.CalculateField_management(indata, fd5, "!" + fd5 + "!.strip()", "PYTHON", "")

# Calculating layer road name values
# --------------------------------------------------------------------------------------------------------------
msg("Calculating road names in layer...")
cur = arcpy.UpdateCursor(indata)	
for feat in cur:
	if fd1:
		PRE = feat.getValue(fd1)
	else:
		PRE = ""
	if fd2:
		PTY = feat.getValue(fd2)
	else:
		PTY = ""
	NAM = feat.getValue(fd3)
	if fd4:
		SUF = feat.getValue(fd4)
	else:
		SUF = ""
	if fd5:
		PDR = feat.getValue(fd5)
	else:
		PDR = ""
	val = CalculateRoadName(PRE, PTY, NAM, SUF, PDR)
	feat.setValue(fd6, val)
	cur.updateRow(feat)

	

	
	
arcpy.AddMessage("\n\nDone!\n\n")



	




