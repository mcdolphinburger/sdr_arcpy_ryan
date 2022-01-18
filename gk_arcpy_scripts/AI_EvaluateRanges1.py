

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: adds2roads.py
Created: 2012-09-08
Modified: 2020-02-03
About: Evaluates Left ranges, Right ranges, From ranges, and To ranges

"""



# Import modules
# ---------------------------
import arcpy, sys, string, datetime


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(lyr, fname):
	doesexist = False
	for fld in arcpy.ListFields(lyr):
		if fld.name == fname:
			doesexist = True
	return doesexist


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
LF = arcpy.GetParameterAsText(1)
LT = arcpy.GetParameterAsText(2)
RF = arcpy.GetParameterAsText(3)
RT = arcpy.GetParameterAsText(4)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
# LF = "LEFT_FROM"
# LT = "LEFT_TO"
# RF = "RIGHT_FROM"
# RT = "RIGHT_TO"



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nEvaluating layer \"" + lyr + "\" for similarness and sameness.\n\n")






# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if FieldExists(lyr, "RNG_EVAL1"):
	msg("Field [RNG_EVAL1] exists?  TRUE\n")
else:
	arcpy.AddField_management(lyr, "RNG_EVAL1", "TEXT", "", "", "16", "RNG_EVAL1", "NULLABLE", "NON_REQUIRED", "")
	msg("Field [RNG_EVAL1] exists?  FALSE. Field was created.\n")

cur = arcpy.UpdateCursor(lyr)
for feat in cur:
	vLF = feat.getValue(LF)
	vLT = feat.getValue(LT)
	vRF = feat.getValue(RF)
	vRT = feat.getValue(RT)
	
	dL = vLT - vLF							# delta Left
	dR = vRT - vRF							# delta Right
	dF = abs(vLF - vRF)						# delta From
	dT = abs(vLT - vRT)						# delta To
	
	# Left range evaluation.
	#   if X: Left From and Left To both equal 0
	#   if 0: Left From and Left To are equal.
	#   if +: Left From is less than Left To.
	#   if -: Left From is greater than Left To.
	if vLF == 0 and vLT == 0:
		res1 = "X"
	elif dL == 0:
		res1 = "0"
	elif dL > 0:
		res1 = "+"
	else:
		res1 = "-"
	
	# Right range evaluation.
	#   if X: Right From and Right To both equal 0
	#   if 0: Right From and Right To are equal.
	#   if +: Right From is less than Right To.
	#   if -: Right From is greater than Right To.
	if vRF == 0 and vRT == 0:
		res2 = "X"
	elif dR == 0:
		res2 = "0"
	elif dR > 0:
		res2 = "+"
	else:
		res2 = "-"
		
	# From range evaluation.
	#	if X: Right From and Left From both equal 0
	#	if 0: Right From and Left From are equal
	#	if 1: Right From and Left From differ by 1
	#	if +: Right From and Left From differ by more than 1
	if vLF == 0 and vRF == 0:
		res3 = "X"
	elif dF == 0:
		res3 = "0"
	elif dF == 1:
		res3 = "1"
	else:
		res3 = "+"
	
	# To range evaluation
	#	if X: Right To and Left To both equal 0
	#	if 0: Right To and Left To are equal
	#	if 1: Right To and Left To differ by 1
	#	if +: Right To and Left To differ by more than 1
	if vLT == 0 and vRT == 0:
		res4 = "X"
	elif dT == 0:
		res4 = "0"
	elif dT == 1:
		res4 = "1"
	else:
		res4 = "+"
	
	res = res1 + res2 + res3 + res4
	
	feat.setValue("RNG_EVAL1", res)
	cur.updateRow(feat)

del feat, cur


arcpy.AddMessage("\n\nDone!\n\n")



	




