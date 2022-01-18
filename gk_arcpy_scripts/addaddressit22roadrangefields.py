

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: addaddressit22roadrangefields.py
Created: 2012-07-27
Modified: 2020-01-25
About: Adds the AddressIt 2.3 road range fields.

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
	doesexist = "FALSE"
	for fld in fields:
		if fld.Name == fname:
			doesexist = "TRUE"
	return doesexist

def CreateField(fs, fn):
	if FieldExists(fs, fn):
		arcpy.AddField_management(lyr, fn, "LONG", "", "", "", fn, "NULLABLE", "NON_REQUIRED", "")



# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nAdding AddressIt 2.2 Road Range Fields\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)	


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
desc = arcpy.Describe(lyr)
fc = desc.FeatureClass
fields = fc.Fields


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

CreateField(fields, "LEFT_FROM")
CreateField(fields, "LEFT_TO")
CreateField(fields, "RIGHT_FROM")
CreateField(fields, "RIGHT_TO")




arcpy.AddMessage("\n\n\n")



	




