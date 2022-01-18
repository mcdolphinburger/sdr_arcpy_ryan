

"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: addaddressit21rclfields.py
Created: 20120907
Modified: 20161216
About: Adds the AddressIt 2.1 street centerline fields to the feature layer that the user chooses.

"""


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
	
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			# Feature layer
typ = arcpy.GetParameterAsText(1)			# string; text value indicating which AddressIt layer to add the fields to


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n\nAdding AddressIt 2.1 RCL fields to " + lyr + "\n\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Add the road name fields
msg("Adding the fields...")
arcpy.AddField_management(lyr, "PREFIX", "TEXT", "", "", "2", "PREFIX", "NULLABLE", "NON_REQUIRED", "")
if typ == "Addresses":
	arcpy.AddField_management(lyr, "ROAD_NAME", "TEXT", "", "", "40", "ROAD_NAME", "NULLABLE", "NON_REQUIRED", "")
else:
	arcpy.AddField_management(lyr, "NAME", "TEXT", "", "", "40", "NAME", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "SUFFIX", "TEXT", "", "", "4", "SUFFIX", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "POSTDIR", "TEXT", "", "", "2", "POSTDIR", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(lyr, "RDNAME", "TEXT", "", "", "51", "RDNAME", "NULLABLE", "NON_REQUIRED", "")


# Calculate default values
msg("Calculating default values...")
arcpy.CalculateField_management(lyr, "PREFIX", "\"\"", "VB", "")
if typ == "Addresses":
	arcpy.CalculateField_management(lyr, "ROAD_NAME", "\"\"", "VB", "")
else:
	arcpy.CalculateField_management(lyr, "NAME", "\"\"", "VB", "")
arcpy.CalculateField_management(lyr, "SUFFIX", "\"\"", "VB", "")
arcpy.CalculateField_management(lyr, "POSTDIR", "\"\"", "VB", "")
arcpy.CalculateField_management(lyr, "RDNAME", "\"\"", "VB", "")







msg("\n\n\n")