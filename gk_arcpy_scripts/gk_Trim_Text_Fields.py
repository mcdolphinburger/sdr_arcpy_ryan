# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Trim_Text_Fields.py
# Created on: 2012-02-18
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
import arcpy, datetime

def msg(msg):
	arcpy.AddMessage(msg)
	
	

# Introduction message
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nTrim All Text Fields" + "\n" + "Today's Date: " + str(datetime.date.today()) + "\n=======================================\n\n")



# Script arguments
# --------------------------------------------------------------------------------------------------------------
FL1 = arcpy.GetParameterAsText(0)										# Any feature layer

# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
desc = arcpy.Describe(FL1)
fc = desc.FeatureClass
fields = fc.Fields

# Trim all text fields
# --------------------------------------------------------------------------------------------------------------
cur = arcpy.UpdateCursor(FL1)
for field in fields:
	fnam = field.name
	if not fnam == "NAME":
		if field.type == "String":
			msg("   --> trimming " + fnam)
			arcpy.CalculateField_management(FL1, fnam, "!" + fnam + "!.strip()", "PYTHON", "")
			# arcpy.CalculateField_management(FL1, fnam, "TRIM([" + fnam + "])", "VB", "")
			# arcpy.CalculateField_management(FL1, fnam, "TRIM(\"" + fnam + "\")", "VB", "")



arcpy.AddMessage("\n\n\n")



	




