

"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: convertevenodd2leftright.py
Created: 20170220
Modified: 20180228
About: Converts Even/Odd fields to Left/Rifght fields, and vice-versa.

"""



# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)


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


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
bolType = arcpy.GetParameterAsText(0)			# Boolean specifying which type of conversion to do, L-R to E-O or the opposite
lyr = arcpy.GetParameterAsText(1)			  	# Feature Layer containing compiled road name attributes
fldE = arcpy.GetParameterAsText(2)				# Field containing Even attributes
fldD = arcpy.GetParameterAsText(3)				# Field containing Odd attributes
fldL = arcpy.GetParameterAsText(4)				# Field containing Left attributes
fldR = arcpy.GetParameterAsText(5)				# Field containing Right attributes



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fldLF = "LEFT_FROM"
fldLT = "LEFT_TO"
fldRF = "RIGHT_FROM"
fldRT = "RIGHT_TO"



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	










# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


try:

	#fds = ["'" + fld1 + "', '" + fld2 + "'"]
	fds = []
	fds.append(fldE)
	fds.append(fldD)
	fds.append(fldL)
	fds.append(fldR)
	fds.append(fldLF)
	fds.append(fldLT)
	fds.append(fldRF)
	fds.append(fldRT)

	cur, row = None, None
	cur = arcpy.da.UpdateCursor(lyr, fds)
	for row in cur:
		vE = row[0]
		vD = row[1]
		vL = row[2]
		vR = row[3]
		vlf = row[4]
		vlt = row[5]
		vrf = row[6]
		vrt = row[7]
		pconst = CalculatePCONST(vlf, vlt, vrf, vrt)
		#msg(pconst + ":" + str(vlf) + ":" + str(vlt) + ":" + str(vrf) + ":" + str(vrt))
		if bolType == "E-O ---> L-R":
			# convert Evens/Odds to Lefts/Rights
			if vE == vD or pconst == "EEOO" or pconst == "EEXX" or pconst == "XXOO" or pconst == "EEEO" or pconst == "EEOE":
				row[2] = vE
				row[3] = vD
			elif pconst == "OOEE" or pconst == "OOXX" or pconst == "XXEE" or pconst == "OOEO" or pconst == "OOOE":
				row[2] = vD
				row[3] = vE
			else:
				row[2] = vE
				row[3] = vD
		else:
			# convert Lefts/Rights to Evens/Odds
			if vL == vR or pconst == "EEOO" or pconst == "EEXX" or pconst == "XXOO" or pconst == "EEEO" or pconst == "EEOE":
				row[0] = vL
				row[1] = vR
			elif pconst == "OOEE" or pconst == "OOXX" or pconst == "XXEE" or pconst == "OOEO" or pconst == "OOOE":
				row[2] = vR
				row[3] = vL
			else:
				row[2] = vE
				row[3] = vD
		cur.updateRow(row)
			

	cur, row = None, None	


except Exception as e:
	msg("\nThere was an error converting Evens/Odds and Lefts/Rights.")
	msg("\n  Error message:\n  " + str(e))
	row, cur = None, None





arcpy.AddMessage("\n\n\nDone!\n\n\n")



	




