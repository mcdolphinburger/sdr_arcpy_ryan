
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: exportaddressitlayertoshapefile.py
Created: 20191113
Modified: 20191113
About: Exports and AddressIt address point or centerline layer to a shapefile with shapefile-friendly field names.

"""




# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


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





# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)
outshp = arcpy.GetParameterAsText(1)

FL = []
FL = [
	["DATE_CREATED", "DATENEW"],
	["DATE_MODIFIED", "DATEMOD"],
	["USER_INITIALS", "USER_INIT"],
	["STRUCTURE_NUM", "HOUSE_NUM"],
	["STREET_NAME", "STR_NAME"],
	["STREET_TYPE", "STR_TYPE"],
	["COMP_STR_NAME", "FULL_NAME"],
	["FULL_ADDRESS", "FULL_ADD"],
	["FIRST_NAME1", "FIRSTNAME1"],
	["FIRST_NAME2", "FIRSTNAME2"],
	["CELL_PHONE1", "CELLPHONE1"],
	["CELL_PHONE2", "CELLPHONE2"],
	["STRUCTURE_COMP", "STRUCTCOMP"],
	["STRUCTURE_TYPE", "STRUCTTYPE"],
	["LAST_CHANGE", "LAST_EDIT"],
	["DATA_SOURCE", "DATASOURCE"],
	["FEATURE_GUID", "FEAT_GUID"],
	["CLASSIFICATION", "STR_CLASS"],
	#["E911_COMM_E", "E911COMME"],
	#["E911_COMM_O", "E911COMMO"],
	["E911_COMM_L", "E911COMML"],
	["E911_COMM_R", "E911COMMR"]
	]
	


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
lyrfc = arcpy.Describe(lyr).FeatureClass				# input feature class
lyrfcnew = lyrfc.catalogPath + "_tocopy"				# output feature class
head, tail = os.path.split(lyrfc.catalogPath)			# path and feature class name for input feature class
outshppath, outshpname = os.path.split(outshp)			# path and shapefile name for output shapefile
msg(outshpname)


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n")

	

# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# copy AddressIt Feature Class and do actions on it. Will delete at the end.
msg("Backing up feature class to be exported.")
arcpy.FeatureClassToFeatureClass_conversion(lyr, head, tail + "_tocopy")
fds = arcpy.ListFields(lyrfcnew)

# Re-name fields in feature class copy prior to exporting
msg("Re-naming fields.")
for i in FL:
	if FieldExists(fds, i[0]):
		msg(" Renaming field " + str(i[0]) + " to " + str(i[1]))
		arcpy.AlterField_management(lyrfcnew, i[0], i[1], i[1])

# Export copied feature class to shapefile
msg("Exporting to shapefile.")
arcpy.FeatureClassToFeatureClass_conversion(lyrfcnew, outshppath, outshpname)

# delete the backup
msg("Deleting the backup.")
arcpy.Delete_management(lyrfcnew)




arcpy.AddMessage("\n\nDone!\n\n")



	




