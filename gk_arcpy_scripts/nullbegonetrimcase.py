

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: nullbegonetrimcase.py
Created: 20130403
Modified: 20161216
About: Loops through all fields in the selected dataset and removes NULL values, trims text attributes, and
       forces all text attributes to upper case.
"""

# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)


#	Receives: describe object
#	 Returns: string indicating the kind of workspace of the input layer
#	---------------------------------------------------------------------------------
def GetWorkspaceType(ds):
	if (ds.dataElement.dataType) == "ShapeFile":
		work = "shape"
	elif (ds.dataElement.dataType) == "FeatureClass":
		p = ds.dataElement.catalogPath
		if ".mdb" in p:
			work = "pers"
		else:
			work = "file"
	else:
		work = "unk"
	return work


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)		       # Input Feature Layer


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
# desc = arcpy.Describe(lyr)
# fc = desc.FeatureClass
# fds = arcpy.ListFields(lyr)

arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION", "")
ct = int(arcpy.GetCount_management(lyr).getOutput(0))


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nRemoving NULL values, trimming text attributes, and forcing upper case text values")
msg("======================================================================================\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

for fd in arcpy.ListFields(lyr):
	if fd.editable:
		if fd.type == "String":
			msg(" Processing field " + str(fd.name).upper() + " (" + fd.type + ")")
			cur = arcpy.da.UpdateCursor(lyr, fd.name)
			for row in cur:
				if row[0] == None:
					row[0] = ""
					cur.updateRow(row)
				else:
					v = row[0]
					v = v.strip()
					v = v.upper()
					row[0] = v
					cur.updateRow(row)
			cur, row = None, None
		elif fd.type == "Double" or fd.type == "Single" or fd.type == "Integer" or fd.type == "SmallInteger":
			msg(" Processing field " + str(fd.name).upper() + " (" + fd.type + ")")
			cur = arcpy.da.UpdateCursor(lyr, fd.name)
			for row in cur:
				if row[0] == None:
					row[0] = 0
					cur.updateRow(row)
			cur, row = None, None
		elif fd.type == "Date":
			msg(" Processing field " + str(fd.name).upper() + " (" + fd.type + ")")
			cur = arcpy.UpdateCursor(lyr)
			for row in cur:
				if row.getValue(fd.name) == None:
					row.setValue(fd.name, datetime.datetime(1899, 12, 31))
					cur.updateRow(row)
			cur, row = None, None
	else:
		msg(" Field " + str(fd.name).upper() + " is not editable")


msg("\n\nDone!\n\n")



	




