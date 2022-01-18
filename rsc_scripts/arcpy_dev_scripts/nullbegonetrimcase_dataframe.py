"""
Author: Ryan Saul Cunningham
Email: rcunningham@sdrmaps.com
Script: nullbegonetrimcase_dataframe.py
Created: 20130413
Modified: 20220113
About: Removes null attributes, trims whitespace and forces uppercase for all string values.
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
#	Returns: string indicating the kind of workspace of the input layer
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
mxd = arcpy.mapping.MapDocument("CURRENT")             # selects the project's mxd
df = arcpy.mapping.ListDataFrames(mxd, '')[0]          # selects the project mxd's first dataframe


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------

lyrs = arcpy.mapping.ListLayers(mxd, '', df)

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nRemoving NULL values, trimming text attributes, and forcing upper case text values")
msg("======================================================================================\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

for lyr in lyrs:
    if lyr.isFeatureLayer:
        msg("\nProcessing layer " + lyr.name + " in project dataframe. . . \n")
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
	# except Exception as e:
		# row, cur = None, None
		# msg("\n---------------------------------------------------------------------------")
		# msg("There was an error processing the data.")
		# msg("Error message:\n\n" + str(e))
		# msg("\n---------------------------------------------------------------------------")
		

msg("\n\nFini!\n\n")



	




