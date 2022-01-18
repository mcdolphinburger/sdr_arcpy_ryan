

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
lyrs = targetlyrs.split(";")

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nRemoving NULL values, trimming text attributes, and forcing upper case text values")
msg("======================================================================================\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Get the first N characters in a string: val[:N], where val is a string value

for lyr in lyrs:
	try:
		for fd in arcpy.ListFields(lyr):
			if fd.name[:4] == "STOP":
				msg("Processing field " + fd.name + " in layer " + lyr)
				cur = arcpy.da.UpdateCursor(lyr, fd.name)
				for row in cur:
					row[0] = "****"
					cur.updateRow(row)
			
	except Exception as e:
		row, cur = None, None
		msg("\n---------------------------------------------------------------------------")
		msg("There was an error processing the data.")
		msg("Error message:\n\n" + str(e))
		msg("\n---------------------------------------------------------------------------")
		



msg("\n\nDone!\n\n")



	




