

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: addaddressit22roadnamefields.py
Created: 2012-07-27
Modified: 2020-01-25
About: Adds the AddressIt 2.3 road name fields.

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
		if fld.Name == fname:
			return True
	return False

def CreateField(fs, fn, len):
	arcpy.AddField_management(lyr, fn, "TEXT", "", "", len, fn, "NULLABLE", "NON_REQUIRED", "")



# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nAdding AddressIt 2.2 Road Name Fields\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)	
doPT= arcpy.GetParameter(1)	

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
desc = arcpy.Describe(lyr)
fc = desc.FeatureClass
fields = fc.Fields


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

CreateField(fields, "PRE_DIR", "2")
if doPT:
	CreateField(fields, "PRE_TYPE", "30")
CreateField(fields, "STREET_NAME", "50")
CreateField(fields, "STREET_TYPE", "4")
CreateField(fields, "POST_DIR", "2")
CreateField(fields, "COMP_STR_NAME", "75")




arcpy.AddMessage("\n\nDone!\n\n")



	




