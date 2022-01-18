# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# gk_RecreateField.py
# Created on: 2013-01-21
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


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)
  

# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
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
	
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
oldfld  = arcpy.GetParameterAsText(1)
newtype = arcpy.GetParameterAsText(2)
newlen = arcpy.GetParameterAsText(3)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
newfld = oldfld.upper()
lf = arcpy.ListFields(lyr)
for f in lf:
  if f.name == oldfld:
    fd = f
    oldtype = fd.type
    oldlen = fd.length

    
    
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n\n")


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================
# Arguments: input table, field name, field type, precision, scale, length, field alias, is nullable, is required, domain
# Arguments: input table, field name, expression, expression type, code block
if fd.type == "String":
  msg("Adding backup field")
  arcpy.AddField_management(lyr, "temptext", "TEXT", "", "", fd.length, "temptext", "NULLABLE", "NON_REQUIRED", "")
  msg("Populating backup field")
  arcpy.CalculateField_management(lyr, "temptext", "!" + oldfld + "!", "PYTHON", "")
  msg("Deleting original field")
  arcpy.DeleteField_management(lyr, oldfld)
  if newtype == "TEXT":
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", newlen, newfld, "NULLABLE", "NON_REQUIRED", "")
  else:
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", "", newfld, "NULLABLE", "NON_REQUIRED", "")
  msg("Populating re-created field")
  arcpy.CalculateField_management(lyr, newfld, "!temptext!", "PYTHON", "")
  msg("Deleting backup field")
  arcpy.DeleteField_management(lyr, "temptext")
elif fd.type == "Integer":
  msg("Adding backup field")
  arcpy.AddField_management(lyr, "templong", "LONG", "", "", "", "templong", "NULLABLE", "NON_REQUIRED", "")
  msg("Populating backup field")
  arcpy.CalculateField_management(lyr, "templong", "!" + oldfld + "!", "PYTHON", "")
  msg("Deleting original field")
  arcpy.DeleteField_management(lyr, oldfld)
  if newtype == "TEXT":
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", newlen, newfld, "NULLABLE", "NON_REQUIRED", "")
  else:
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", "", newfld, "NULLABLE", "NON_REQUIRED", "")
  msg("Populating re-created field")
  arcpy.CalculateField_management(lyr, newfld, "!templong!", "PYTHON", "")
  msg("Deleting backup field")
  arcpy.DeleteField_management(lyr, "templong")
elif fd.type == "SmallInteger":
  msg("Adding backup field")
  arcpy.AddField_management(lyr, "tempshort", "SHORT", "", "", "", "tempshort", "NULLABLE", "NON_REQUIRED", "")
  msg("Populating backup field")
  arcpy.CalculateField_management(lyr, "tempshort", "!" + oldfld + "!", "PYTHON", "")
  msg("Deleting original field")
  arcpy.DeleteField_management(lyr, oldfld)
  if newtype == "TEXT":
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", newlen, newfld, "NULLABLE", "NON_REQUIRED", "")
  else:
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", "", newfld, "NULLABLE", "NON_REQUIRED", "")
  msg("Populating re-created field")
  arcpy.CalculateField_management(lyr, newfld, "!tempshort!", "PYTHON", "")
  msg("Deleting backup field")
  arcpy.DeleteField_management(lyr, "tempshort")
elif fd.type == "Double":
  msg("Adding backup field")
  arcpy.AddField_management(lyr, "tempdouble", "DOUBLE", "", "", "", "tempdouble", "NULLABLE", "NON_REQUIRED", "")
  msg("Populating backup field")
  arcpy.CalculateField_management(lyr, "tempdouble", "!" + oldfld + "!", "PYTHON", "")
  msg("Deleting original field")
  arcpy.DeleteField_management(lyr, oldfld)
  if newtype == "TEXT":
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", newlen, newfld, "NULLABLE", "NON_REQUIRED", "")
  else:
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", "", newfld, "NULLABLE", "NON_REQUIRED", "")
  msg("Populating re-created field")
  arcpy.CalculateField_management(lyr, newfld, "!tempdouble!", "PYTHON", "")
  msg("Deleting backup field")
  arcpy.DeleteField_management(lyr, "tempdouble")
elif fd.type == "Date":
  msg("Adding backup field")
  arcpy.AddField_management(lyr, "tempdate", "DATE", "", "", "", "tempdate", "NULLABLE", "NON_REQUIRED", "")
  msg("Populating backup field")
  arcpy.CalculateField_management(lyr, "tempdate", "!" + oldfld + "!", "PYTHON", "")
  msg("Deleting original field")
  arcpy.DeleteField_management(lyr, oldfld)
  if newtype == "TEXT":
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", newlen, newfld, "NULLABLE", "NON_REQUIRED", "")
  else:
    msg("Re-creating original field with new properties")
    arcpy.AddField_management(lyr, newfld, newtype, "", "", "", newfld, "NULLABLE", "NON_REQUIRED", "")
  msg("Populating re-created field")
  arcpy.CalculateField_management(lyr, newfld, "!tempdate!", "PYTHON", "")
  msg("Deleting backup field")
  arcpy.DeleteField_management(lyr, "tempdate")




		





msg("\n\n\n")



	




