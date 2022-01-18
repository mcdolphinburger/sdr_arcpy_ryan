

"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: nullbegonetrimcase_multilayer.py
Created: 20130413
Modified: 20181101
About: Removes null attributes, trims leading or trailing spaces, and forces all text to upper case

"""

# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime
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
targetlyrs = arcpy.GetParameterAsText(0)		       # Input Feature Layer


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------


#arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION", "")

lyrs = targetlyrs.split(";")

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nRemoving NULL values, trimming text attributes, and forcing upper case text values")
msg("======================================================================================\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

for lyr in lyrs:
	try:
		msg("\nProcessing layer: " + lyr + "\n")
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
	except Exception as e:
		row, cur = None, None
		msg("\n---------------------------------------------------------------------------")
		msg("There was an error processing the data.")
		msg("Error message:\n\n" + str(e))
		msg("\n---------------------------------------------------------------------------")
		



msg("\n\nDone!\n\n")



	




