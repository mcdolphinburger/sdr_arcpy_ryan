"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: codeaddswithrclid.py
Created: 20190418
Modified: 20190418
About: Writes centerline id values to the address points for the segment of road that the address is on.

"""

# Import modules
# ---------------------------
import arcpy, datetime, os, string, arcpy.mapping, _My_Python_Functions
from _My_Python_Functions import IsNumericField
from fractions import Fraction


# ==============================================================================================================
#                                                                             F   U   N   C   T   I   O   N   S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)

def GetFieldType(lyr, nam):
	for fd in arcpy.ListFields(lyr):
		if fd.name == nam:
			return fd.type
			
 
		

# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	

	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrA = arcpy.GetParameterAsText(0)					# Address Point layer
fA = arcpy.GetParameterAsText(1)					# RCLID field in the Address Points
lyrR = arcpy.GetParameterAsText(2)					# Road centerline layer
fR = arcpy.GetParameterAsText(3)					# RCLID field in the centerlines
overwrite = arcpy.GetParameter(4)					# Boolean in whether to overwrite previous results



# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
fullnameA = "COMP_STR_NAME"
fullnameR = "COMP_STR_NAME"
adr = "STRUCTURE_NUM"
lw = "RNG_LOW"
hi = "RNG_HIGH"

	


# Introduction message
# -------------------------------------------------------------------------------------------------------------
msg("\n\n")
msg("                Address Layer: " + lyrA)
msg("          Address RCLID Field: " + fA)
msg("\n")
msg("             Centerline Layer: " + lyrR)
msg("       Centerline RCLID Field: " + fR)
msg("\n\n")




# ==============================================================================================================
#                                                                             		      D O   T H E   W O R K
# ==============================================================================================================

# TEXT —Names or other textual qualities.
# FLOAT —Numeric values with fractional values within a specific range.
# DOUBLE —Numeric values with fractional values within a specific range.
# SHORT —Numeric values without fractional values within a specific range; coded values.
# LONG —Numeric values without fractional values within a specific range.
# DATE —Date and/or Time.
# BLOB —Images or other multimedia.
# RASTER —Raster images.
# GUID —GUID values

# Arguments: Layer Name or Table View, Selection Type, Expression
# arcpy.SelectLayerByAttribute_management(Layer, "NEW_SELECTION", "[COMP_STR_NAME] = '10TH ST'")

arcpy.SelectLayerByAttribute_management(lyrA, "CLEAR_SELECTION", "")
arcpy.SelectLayerByAttribute_management(lyrR, "CLEAR_SELECTION", "")

cursorfieldsA = []
cursorfieldsA.append(fA)
cursorfieldsA.append(fullnameA)
cursorfieldsA.append(adr)


curA = arcpy.da.UpdateCursor(lyrA, cursorfieldsA)

for rowA in curA:
	nama = rowA[1]
	a = rowA[2]
	cursorfieldsR = []
	cursorfieldsR.append(fR)
	cursorfieldsR.append(fullnameR)
	cursorfieldsR.append(lw)
	cursorfieldsR.append(hi)
	curR = arcpy.da.SearchCursor(lyrR, cursorfieldsR)
	for rowR in curR:
		idr = rowR[0]
		namr = rowR[1]
		lwr = rowR[2]
		hir = rowR[3]
		if namr == nama and a >= lwr and a <= hir:
			#msg(str(a) + ": " + str(lwr) + " - " + str(hir) + "  (" + str(idr) + ")")
			rowA[0] = idr
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



	




