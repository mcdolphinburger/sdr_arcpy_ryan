"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: codefieldwithpolygonvalues2.py
Created: 20200212
Modified: 20200212
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
idfld = arcpy.GetParameterAsText(4)					# Field from Target Layer that will be used to join data from output back to the target data
overwrite = arcpy.GetParameter(5)					# Boolean in whether to overwrite previous results



# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
#output = arcpy.Describe(lyrT).FeatureClass.Name + "_spjoin"
output = arcpy.Describe(lyrT).catalogPath + "_spjoin"
msg(output)




# Introduction message
# -------------------------------------------------------------------------------------------------------------
msg("\n\n")
msg("Target Layer (lines or points): " + lyrT)
msg("                  Target Field: " + fT)
msg("               Target ID field: " + idfld)
msg("\n")
msg("       Source Layer (polygons): " + lyrS)
msg("                  Source Field: " + fS)
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


# performs the spatial join. Fileds from the Source Layer will be added to the fields of the 
# Target layer to create a new featureclass
# **********************************************************************************************

# SpatialJoin(target_features, join_features, out_feature_class, {join_operation}, {join_type}, {field_mapping}, {match_option}, {search_radius}, {distance_field_name})

msg("\nPerforming Spatial Join")
arcpy.SpatialJoin_analysis(lyrT, lyrS, output)

keepfields = [fS, idfld]
dropfields = []
for fd in arcpy.ListFields(output):
	if not fd.name in keepfields and not fd.required:
		dropfields.append(fd.name)

msg("Deleting fields")
arcpy.DeleteField_management(output, dropfields)







# # Identify features completely outside the polygons and code accordingly
# # --------------------------------------------------------------------------------------------------------------
# msg("Coding features completely outside all polygons . . .")
# arcpy.SelectLayerByLocation_management(lyrT, "INTERSECT", lyrS, "", "NEW_SELECTION", "INVERT")
# #arcpy.SelectLayerByLocation_management(lyrT, "INTERSECT", lyrS, "", "SWITCH_SELECTION")
# d = arcpy.Describe(lyrT)
# if d.FIDSet:
	# if IsNumericField(ftypeS):
		# #msg("hereA!")
		# arcpy.CalculateField_management(lyrT, fT, "-1", "VB", "")
	# else:
		# #msg("hereB!")
		# arcpy.CalculateField_management(lyrT, fT, "\"OUT\"", "VB", "")
# else:
    # msg("  No features outside the source layer.")
# arcpy.SelectLayerByAttribute_management(lyrT, "CLEAR_SELECTION","")

# # Identify features completely inside the polygons and code accordingly
# # --------------------------------------------------------------------------------------------------------------
# msg("Coding features completely inside all polygons . . .")

# # this bit creates a where clause expression depending on the workspace types involved
# # **************************************************************************************
# for i in dicS:
    # #msg(i)
    # if wsp == "file" and IsNumericField(ftypeS):
        # wc = "\"" + fS + "\" = " + str(i)
        # #msg("here1! : " + wc)
    # elif wsp == "file" and not IsNumericField(ftypeS):
        # wc = "\"" + fS + "\" = '" + str(i) + "'"
        # #msg("here2! : " + wc)
    # elif (wsp == "shape" or wsp == "pers") and IsNumericField(ftypeS):
        # wc = "[" + fS + "] = " + str(i)
        # #msg("here3! : " + wc)
    # elif (wsp == "shape" or wsp == "pers") and not IsNumericField(ftypeS):
        # wc = "[" + fS + "] = '" + str(i) + "'"
        # #msg("here4! : " + wc)
    # else:
        # wc = ""
        # #msg("here5! : " + wc)
        
    # arcpy.SelectLayerByAttribute_management(lyrS, "NEW_SELECTION", wc)
    # arcpy.SelectLayerByLocation_management(lyrT, "COMPLETELY_WITHIN", lyrS, "", "NEW_SELECTION")
    
    # if IsANumber(i):
        # arcpy.CalculateField_management(lyrT, fT, i, "VB", "")
    # else:
        # arcpy.CalculateField_management(lyrT, fT, "\"" + i + "\"", "VB", "")
        # #arcpy.CalculateField_management(lyrT, fT, i, "VB", "")
        
    # arcpy.SelectLayerByAttribute_management(lyrT, "CLEAR_SELECTION","")
    # arcpy.SelectLayerByAttribute_management(lyrS, "CLEAR_SELECTION","")
	



msg("\n\nDone!\n\n")



	




