# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# <script name>.py
# Created on: 2012-07-27
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
CreateField(fields, "STREET_NAME", "32")
CreateField(fields, "STREET_TYPE", "4")
CreateField(fields, "POST_DIR", "2")




arcpy.AddMessage("\n\n\n")



	




