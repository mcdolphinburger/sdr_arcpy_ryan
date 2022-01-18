"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: codefieldwithpolygonvalues.py
Created: 20161219
Modified: 20180807
About: Writes values from the specified field in the source polygon layer to the specified 
       field in the target line or point layer.

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
			
def GetWorkspaceType(d):
	if (d.dataElement.dataType) == "ShapeFile":
		return "shape"
	elif (d.dataElement.dataType) == "FeatureClass":
		p = d.dataElement.catalogPath
		if ".mdb" in p:
			return "pers"
		else:
			return "file"
	else:
		return "unk"

def GetSelectionCount(lyr):
	sourcecount = int(arcpy.GetCount_management(fc1).getOutput(0))
    

def IsANumber(n):
	try:
		float(n)
		return True
	except ValueError:
		try:
			Fraction(n)
			return True
		except ValueError:
			return False
            
		

# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	

	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrT = arcpy.GetParameterAsText(0)					# Target Feature Layer (layer getting coded)
fT = arcpy.GetParameterAsText(1)					# Target field to receive values
lyrS = arcpy.GetParameterAsText(2)					# Source Feature Layer (selecting layer)
fS = arcpy.GetParameterAsText(3)					# Source field to derive values from
overwrite = arcpy.GetParameter(4)					# Boolean in whether to overwrite previous results



# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
ftypeT = GetFieldType(lyrT, fT)
ftypeS = GetFieldType(lyrS, fS)
ctT = int(arcpy.GetCount_management(lyrT).getOutput(0))
ctS = int(arcpy.GetCount_management(lyrS).getOutput(0))
desc = arcpy.Describe(lyrS)
wsp = GetWorkspaceType(desc)

# Getting a dictionary of all the values in the Source polygon layer
dicS = {}
cur = arcpy.da.SearchCursor(lyrS, fS)
for row in cur:
	v = row[0]
	if not v in dicS:
		dicS[v] = v
		#msg(dicS[v])
	


# Introduction message
# -------------------------------------------------------------------------------------------------------------
msg("\n\n")
msg("Target Layer (lines or points): " + lyrT)
msg("                  Target Field: " + fT)
msg("             Target Field Type: " + ftypeT)
msg("\n")
msg("       Source Layer (polygons): " + lyrS)
msg("                  Source Field: " + fS)
msg("             Source Field Type: " + ftypeS)
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

arcpy.SelectLayerByAttribute_management(lyrT, "CLEAR_SELECTION", "")
arcpy.SelectLayerByAttribute_management(lyrS, "CLEAR_SELECTION", "")


# Identify features completely outside the polygons and code accordingly
# --------------------------------------------------------------------------------------------------------------
msg("Coding features completely outside all polygons . . .")
arcpy.SelectLayerByLocation_management(lyrT, "INTERSECT", lyrS, "", "NEW_SELECTION", "INVERT")
#arcpy.SelectLayerByLocation_management(lyrT, "INTERSECT", lyrS, "", "SWITCH_SELECTION")
d = arcpy.Describe(lyrT)
if d.FIDSet:
	if IsNumericField(ftypeS):
		#msg("hereA!")
		arcpy.CalculateField_management(lyrT, fT, "-1", "VB", "")
	else:
		#msg("hereB!")
		arcpy.CalculateField_management(lyrT, fT, "\"OUT\"", "VB", "")
else:
    msg("  No features outside the source layer.")
arcpy.SelectLayerByAttribute_management(lyrT, "CLEAR_SELECTION","")

# Identify features completely inside the polygons and code accordingly
# --------------------------------------------------------------------------------------------------------------
msg("Coding features completely inside all polygons . . .")

for i in dicS:
    #msg(i)
    if wsp == "file" and IsNumericField(ftypeS):
        wc = "\"" + fS + "\" = " + str(i)
        #msg("here1! : " + wc)
    elif wsp == "file" and not IsNumericField(ftypeS):
        wc = "\"" + fS + "\" = '" + str(i) + "'"
        #msg("here2! : " + wc)
    elif (wsp == "shape" or wsp == "pers") and IsNumericField(ftypeS):
        wc = "[" + fS + "] = " + str(i)
        #msg("here3! : " + wc)
    elif (wsp == "shape" or wsp == "pers") and not IsNumericField(ftypeS):
        wc = "[" + fS + "] = '" + str(i) + "'"
        #msg("here4! : " + wc)
    else:
        wc = ""
        #msg("here5! : " + wc)
        
    arcpy.SelectLayerByAttribute_management(lyrS, "NEW_SELECTION", wc)
    arcpy.SelectLayerByLocation_management(lyrT, "COMPLETELY_WITHIN", lyrS, "", "NEW_SELECTION")
    
    if IsANumber(i):
        arcpy.CalculateField_management(lyrT, fT, i, "VB", "")
    else:
        arcpy.CalculateField_management(lyrT, fT, "\"" + i + "\"", "VB", "")
        #arcpy.CalculateField_management(lyrT, fT, i, "VB", "")
        
    arcpy.SelectLayerByAttribute_management(lyrT, "CLEAR_SELECTION","")
    arcpy.SelectLayerByAttribute_management(lyrS, "CLEAR_SELECTION","")
	



msg("\n\nDone!\n\n")



	




