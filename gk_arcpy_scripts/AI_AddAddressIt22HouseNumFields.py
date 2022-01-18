
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: createcustomschemalayer.py
Created: 2016-06-20
Modified: 2019-11-05
About: Adds basic AddressIt Structure Number fields to the chosen dataset

NOTES:


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
			break
	return False





# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nAdding AddressIt 2.2 House Number Fields\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)	


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
# desc = arcpy.Describe(lyr)
# fc = desc.FeatureClass
# fields = fc.Fields
fields = arcpy.ListFields(lyr)


# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

if not FieldExists(fields, "STRUCTURE_NUM"):
	arcpy.AddField_management(lyr, "STRUCTURE_NUM", "LONG", "", "", "", "STRUCTURE_NUM", "NULLABLE", "NON_REQUIRED", "")

if not FieldExists(fields, "UNIT_DESIG"):
	arcpy.AddField_management(lyr, "UNIT_DESIG", "TEXT", "", "", "16", "UNIT_DESIG", "NULLABLE", "NON_REQUIRED", "")





arcpy.AddMessage("\n\nDone!\n\n")



	




