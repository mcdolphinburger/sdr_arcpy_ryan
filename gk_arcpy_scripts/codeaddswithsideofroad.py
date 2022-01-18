"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: codeaddswithsideofroad.py
Created: 20190418
Modified: 20190418
About: Writes either Left, Right, or No to address point to say what side of the road it's on.

"""

# Import modules
# ---------------------------
import arcpy, datetime, os, string, arcpy.mapping



# ==============================================================================================================
#                                                                             F   U   N   C   T   I   O   N   S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)


def GetParityAddress(adr):
	if adr == 0:
		return "Z"
	elif adr % 2 == 0:
		return "E"
	else:
		return "O"
		

# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrA = arcpy.GetParameterAsText(0)					# Address Point layer
lyrR = arcpy.GetParameterAsText(1)					# Road centerline layer




# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
fullnameA = "COMP_STR_NAME"
adr = "STRUCTURE_NUM"
rclside = "RCLSIDE"
fullnameR = "COMP_STR_NAME"
pconst = "PCONST"
lw = "RNG_LOW"
hi = "RNG_HIGH"

	


# Introduction message
# -------------------------------------------------------------------------------------------------------------



# ==============================================================================================================
#                                                                             		      D O   T H E   W O R K
# ==============================================================================================================

# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


arcpy.SelectLayerByAttribute_management(lyrA, "CLEAR_SELECTION", "")
arcpy.SelectLayerByAttribute_management(lyrR, "CLEAR_SELECTION", "")

cursorfieldsA = []
cursorfieldsA.append(rclside)
cursorfieldsA.append(fullnameA)
cursorfieldsA.append(adr)

curA = arcpy.da.UpdateCursor(lyrA, cursorfieldsA)

for rowA in curA:
	nama = rowA[1]
	a = rowA[2]
	pa = GetParityAddress(a)
	if a <= 0:
		rowA[0] = "N"
		curA.updateRow(rowA)
	else:
		cursorfieldsR = []
		cursorfieldsR.append(fullnameR)
		cursorfieldsR.append(lw)
		cursorfieldsR.append(hi)
		cursorfieldsR.append(pconst)
		curR = arcpy.da.SearchCursor(lyrR, cursorfieldsR)
		for rowR in curR:
			#pconst = rowR[3]
			pl = rowR[3][:2]
			pr = rowR[3][-2:]
			namr = rowR[0]
			lwr = rowR[1]
			hir = rowR[2]
			if namr == nama and a >= lwr and a <= hir:
				#msg(str(a) + ": " + str(lwr) + " - " + str(hir) + "  (" + str(idr) + ")")
				if pa == "E" and pl == "EE":
					rowA[0] = "L"
					curA.updateRow(rowA)
				elif pa == "E" and pr == "EE":
					rowA[0] = "R"
					curA.updateRow(rowA)
				elif pa == "E" and pl == "XX" and pr == "OO":
					rowA[0] = "L"
					curA.updateRow(rowA)
				elif pa == "E" and pl == "OO" and pr == "XX":
					rowA[0] = "R"
					curA.updateRow(rowA)
				elif pa == "O" and pl == "OO":
					rowA[0] = "L"
					curA.updateRow(rowA)
				elif pa == "O" and pr == "OO":
					rowA[0] = "R"
					curA.updateRow(rowA)
				elif pa == "O" and pl == "XX" and pr == "EE":
					rowA[0] = "L"
					curA.updateRow(rowA)
				elif pa == "O" and pl == "EE" and pr == "XX":
					rowA[0] = "R"
					curA.updateRow(rowA)
				else:
					rowA[0] = "N"
					curA.updateRow(rowA)
				break

				
		
















# # Identify features completely outside the polygons and code accordingly
# # --------------------------------------------------------------------------------------------------------------
# msg("Coding features completely outside all polygons . . .")
# arcpy.SelectLayerByLocation_management(lyrA, "INTERSECT", lyrR, "", "NEW_SELECTION", "INVERT")
# #arcpy.SelectLayerByLocation_management(lyrA, "INTERSECT", lyrR, "", "SWITCH_SELECTION")
# d = arcpy.Describe(lyrA)
# if d.FIDSet:
	# if IsNumericField(ftypeS):
		# #msg("hereA!")
		# arcpy.CalculateField_management(lyrA, fT, "-1", "VB", "")
	# else:
		# #msg("hereB!")
		# arcpy.CalculateField_management(lyrA, fT, "\"OUT\"", "VB", "")
# else:
    # msg("  No features outside the source layer.")
# arcpy.SelectLayerByAttribute_management(lyrA, "CLEAR_SELECTION","")

# # Identify features completely inside the polygons and code accordingly
# # --------------------------------------------------------------------------------------------------------------
# msg("Coding features completely inside all polygons . . .")

# for i in dicS:
    # #msg(i)
    # if wsp == "file" and IsNumericField(ftypeS):
        # wc = "\"" + fS + "\" = " + str(i)
        # msg("here1! : " + wc)
    # elif wsp == "file" and not IsNumericField(ftypeS):
        # wc = "\"" + fS + "\" = '" + str(i) + "'"
        # msg("here2! : " + wc)
    # elif (wsp == "shape" or wsp == "pers") and IsNumericField(ftypeS):
        # wc = "[" + fS + "] = " + str(i)
        # msg("here3! : " + wc)
    # elif (wsp == "shape" or wsp == "pers") and not IsNumericField(ftypeS):
        # wc = "[" + fS + "] = '" + str(i) + "'"
        # msg("here4! : " + wc)
    # else:
        # wc = ""
        # msg("here5! : " + wc)
        
    # arcpy.SelectLayerByAttribute_management(lyrR, "NEW_SELECTION", wc)
    # arcpy.SelectLayerByLocation_management(lyrA, "COMPLETELY_WITHIN", lyrR, "", "NEW_SELECTION")
    
    # if IsANumber(i):
        # arcpy.CalculateField_management(lyrA, fT, i, "VB", "")
    # else:
        # arcpy.CalculateField_management(lyrA, fT, "\"" + i + "\"", "VB", "")
        # #arcpy.CalculateField_management(lyrA, fT, i, "VB", "")
        
    # arcpy.SelectLayerByAttribute_management(lyrA, "CLEAR_SELECTION","")
    # arcpy.SelectLayerByAttribute_management(lyrR, "CLEAR_SELECTION","")
	



msg("\n\nDone!\n\n")



	




