# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Schema_Compare.py
# Created on: 2012-10-11
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
import arcpy, sys, string, datetime
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
lyrA = arcpy.GetParameterAsText(0)			# Layer "A"
lyrB = arcpy.GetParameterAsText(1)			# Layer "B"


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
descA = arcpy.Describe(lyrA)
fiA = descA.fieldInfo
fcA = descA.FeatureClass
fieldsA = arcpy.ListFields(lyrA)
ctA = fiA.count
listA = {}

descB = arcpy.Describe(lyrB)
fiB = descB.fieldInfo
fcB = descB.FeatureClass
fieldsB = arcpy.ListFields(lyrB)
ctB = fiB.count
listB = {}





# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nComparing the schemas of \"" + lyrA + "\" and \"" + lyrB + "\"")
msg("=========================================================================\n\n")









# ==============================================================================================================
#                                                                                         D O   T H E   W O R K
# ==============================================================================================================

i = -1
for f in fieldsA:
	i = i + 1
	listA[i] = [f.name, f.type, f.length, f.precision, f.scale]

i = -1
for f in fieldsB:
	i = i + 1
	listB[i] = [f.name, f.type, f.length, f.precision, f.scale]


if listA == listB:
	msg("** The two sets of fields are identical **")
else:
	msg("    Comparing \"" + lyrA + "\" fields to \"" + lyrB + "\" fields")
	msg("    ---------------------------------------------------------------")
	i=-1
	for fieldA in fieldsA:
		i=i+1
		j=-1
		chk = "bad"
		for fieldB in fieldsB:
			j=j+1
			if listA[i] == listB[j]:
				chk = "ok"
		if chk == "ok":
			msg("    The field \"" + listA[i][0] + "\" is common to both")
		else:
			msg("    The field \"" + listA[i][0] + "\" is specific to \"" + lyrA + "\"")

	msg("\n")
	
	msg("    Comparing \"" + lyrB + "\" fields to \"" + lyrA + "\" fields")
	msg("    ---------------------------------------------------------------")
	i=-1
	for fieldB in fieldsB:
		i=i+1
		j=-1
		chk = "bad"
		for fieldA in fieldsA:
			j=j+1
			if listB[i] == listA[j]:
				chk = "ok"
		if chk == "ok":
			msg("    The field \"" + listB[i][0] + "\" is common to both")
		else:
			msg("    The field \"" + listB[i][0] + "\" is specific to \"" + lyrA + "\"")			
		

msg("\n\n\n")



	




