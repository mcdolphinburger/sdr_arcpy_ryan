
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: addeditortrackingfields.py
Created: 20171207
Modified: 20171207
About: Adds fields for ArMap's built-in Editor Tracking.

"""




# Import modules
# ---------------------------
import sys, arcpy, string, datetime


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)
	
	
def FieldExists(fields, fname):
	for fld in fields:
		if fld.name == fname:
			return True
	return False

def CreateField(fn, len):
	arcpy.AddField_management(lyr, fn, "TEXT", "", "", len, fn, "NULLABLE", "NON_REQUIRED", "")
	
def CreateDField(fn):
	arcpy.AddField_management(lyr, fn, "DATE", "", "", "", fn, "NULLABLE", "NON_REQUIRED", "")



# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nAdding Editor Tracking Fields\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)	


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
desc = arcpy.Describe(lyr)
fc = desc.FeatureClass
fields = arcpy.ListFields(lyr)


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

CreateField("CREATED_BY", "50")
CreateDField("CREATE_DATE")
CreateField("EDITED_BY", "50")
CreateDField("EDIT_DATE")




arcpy.AddMessage("\n\n\n")



	




