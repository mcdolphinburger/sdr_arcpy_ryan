# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# nullbgone2.py
# Created on: 2013-04-13
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
import arcpy, sys, string, datetime


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



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nRemoving NULL values, trimming text attribute values, and forcing upper case text values")
msg("=========================================================================================\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O R K
# ==============================================================================================================

for fd in arcpy.ListFields(lyr):
	if fd.editable:
		if fd.type == "String":
			msg(" Processing field " + str(fd.name).upper() + " (" + fd.type + ")")
			cur = arcpy.UpdateCursor(lyr)
			for row in cur:
				if row.getValue(fd.name) == None:
					row.setValue(fd.name, "")
					cur.updateRow(row)
				else:
					v = row.getValue(fd.name)
					v = v.strip()
					v = v.upper()
					row.setValue(fd.name, v)
					cur.updateRow(row)
			cur, row = None, None
		elif fd.type == "Double" or fd.type == "Single" or fd.type == "Integer" or fd.type == "SmallInteger":
			msg(" Processing field " + str(fd.name).upper() + " (" + fd.type + ")")
			cur = arcpy.UpdateCursor(lyr)
			for row in cur:
				if row.getValue(fd.name) == None:
					row.setValue(fd.name, 0)
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
	msg("  Field " + str(fd.name).upper() + " is not editable")


msg("\n\nDone!\n\n")



	




