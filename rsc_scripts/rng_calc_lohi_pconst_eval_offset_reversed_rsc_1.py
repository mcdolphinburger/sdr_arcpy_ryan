"""
Author: Ryan Saul Cunningham
Email: rcunningham@sdrmaps
Tool: rng_calc_lohi_pconst_eval_offset_reversed_rsc_1.py
Created: 2012-09-08
Modified: 2022-01-10
About: Master road centerlines properties evaluation script: calculates low and high range values, parity constant, ranges evalution check, offset ranges check, reversed ranges check.
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
	for fld in arcpy.ListFields(lyr):
		if fld.name == fname:
			return True
	return False


	
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
fldRES = arcpy.GetParameterAsText(5)
fldREZ = arcpy.GetParameterAsText(6)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
# LF = "LEFT_FROM"
# LT = "LEFT_TO"
# RF = "RIGHT_FROM"
# RT = "RIGHT_TO"



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nEvaluating layer \"" + lyr + " for reversed ranges\n")
#msg("\n\nLooking for reversed ranges\n\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if FieldExists(lyr, fldRES):
	msg("Field " + fldRES + " exists?  TRUE\n")
else:
	arcpy.AddField_management(lyr, fldRES, "TEXT", "", "", "16", fldRES, "NULLABLE", "NON_REQUIRED", "")
	msg("Field " + fldRES + " exists?  FALSE. Field was created.\n")

with arcpy.da.UpdateCursor(lyr, [LF,LT,RF,RT,fldRES]) as cur:
	for row in cur:
		vLF = row[0]
		vLT = row[1]
		vRF = row[2]
		vRT = row[3]
		dL = vLT - vLF							# delta Left
		dR = vRT - vRF							# delta Right
		# Left range evaluation.
		#   X : Left From and Left To both equal 0
		#   S : Left From and Left To are equal.
		#   > : Left From is less than Left To.
		#   < : Left From is greater than Left To.
		if vLF == 0 and vLT == 0:
			res1 = "X"
		elif dL == 0:
			res1 = "S"
		elif dL > 0:
			res1 = ">"
		else:
			res1 = "<"
		
		# Right range evaluation.
		#   X : Right From and Right To both equal 0
		#   S : Right From and Right To are equal.
		#   > : Right From is less than Right To.
		#   < : Right From is greater than Right To.
		if vRF == 0 and vRT == 0:
			res2 = "X"
		elif dR == 0:
			res2 = "S"
		elif dR > 0:
			res2 = ">"
		else:
			res2 = "<"

		row[4] = res1 + res2
		cur.updateRow(row)

del row, cur

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nEvaluating layer \"" + lyr + " for offset ranges\n")
# msg("\n\nLooking for offset ranges\n\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if FieldExists(lyr, fldREZ):
	msg("Field " + fldREZ + " exists?  TRUE\n")
else:
	arcpy.AddField_management(lyr, fldREZ, "TEXT", "", "", "16", fldREZ, "NULLABLE", "NON_REQUIRED", "")
	msg("Field " + fldREZ + " exists?  FALSE. Field was created.\n")

with arcpy.da.UpdateCursor(lyr, [LF,LT,RF,RT,fldREZ]) as cur:
	for row in cur:
		vLF = row[0]
		vLT = row[1]
		vRF = row[2]
		vRT = row[3]
		
		if vLF == 0 or vRF == 0:
			rez1 = "X"
		else:
			rez1 = str(abs(vLF - vRF))
			
		if vLT == 0 or vRT == 0:
			rez2 = "X"
		else:
			rez2 = str(abs(vLT - vRT))
			

		row[4] = rez1 + ":" + rez2
		cur.updateRow(row)

del row, cur

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nEvaluating layer \"" + lyr + "\" for similarity and likeness.\n")



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
		reb1 = "X"
	elif dL == 0:
		reb1 = "0"
	elif dL > 0:
		reb1 = "+"
	else:
		reb1 = "-"
	
	# Right range evaluation.
	#   if X: Right From and Right To both equal 0
	#   if 0: Right From and Right To are equal.
	#   if +: Right From is less than Right To.
	#   if -: Right From is greater than Right To.
	if vRF == 0 and vRT == 0:
		reb2 = "X"
	elif dR == 0:
		reb2 = "0"
	elif dR > 0:
		reb2 = "+"
	else:
		reb2 = "-"
		
	# From range evaluation.
	#	if X: Right From and Left From both equal 0
	#	if 0: Right From and Left From are equal
	#	if 1: Right From and Left From differ by 1
	#	if +: Right From and Left From differ by more than 1
	if vLF == 0 and vRF == 0:
		reb3 = "X"
	elif dF == 0:
		reb3 = "0"
	elif dF == 1:
		reb3 = "1"
	else:
		reb3 = "+"
	
	# To range evaluation
	#	if X: Right To and Left To both equal 0
	#	if 0: Right To and Left To are equal
	#	if 1: Right To and Left To differ by 1
	#	if +: Right To and Left To differ by more than 1
	if vLT == 0 and vRT == 0:
		reb4 = "X"
	elif dT == 0:
		reb4 = "0"
	elif dT == 1:
		reb4 = "1"
	else:
		reb4 = "+"
	
	reb = reb1 + reb2 + reb3 + reb4
	
	feat.setValue("RNG_EVAL1", reb)
	cur.updateRow(feat)

del feat, cur

#msg("\n\nDone!\n\n")
msg("\n\n(>'-')> <('-'<) ^('-')^ v('-')v(>'-')> (^-^)\n\n")