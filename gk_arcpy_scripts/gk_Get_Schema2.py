

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: gk_Get_Schema2.py
Created: 20120126
Modified: 20200921
About: Lists all the field properties for the chosen feature layer.
"""


# Import modules
# ---------------------------
import arcpy, sys, string, datetime


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def GetPythonFieldType(f):
	if f.type == "String":
		return "TEXT"
	elif f.type == "Double":
		return "DOUBLE"
	elif f.type == "Single":
		return "FLOAT"
	elif f.type == "Integer":
		return "LONG"
	elif f.type == "SmallInteger":
		return "SHORT"
	elif f.type == "Date":
		return "DATE"
	elif f.type == "Raster":
		return "RASTER"
	elif f.type == "Guid":
		return "GUID"
	elif f.type == "Blob":
		return "BLOB"
	elif f.type == "OID":
		return "OID"
	elif f.type == "Geometry":
		return "GEOMETRY"
	else:
		return "<unk>"
	


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
IL = arcpy.GetParameterAsText(0)


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(IL)



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nField definitions for: " + IL + "\n============================================================\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

msg("FIELD_NAME,FIELD_ALIAS,FIELD_TYPE,FIELD_LENGTH,FIELD_PRECISION,FIELD_SCALE,DOMAIN,DEFAULT_VALUE")

try:

	for field in fields:
		fname = field.name.upper()
		falias = field.aliasName.upper()
		ftype = GetPythonFieldType(field)
		#ftype = field.type
		flen = field.length
		if ftype != "TEXT":
			flen = ""
		fprec = field.precision
		if fprec == 0:
			fprec = ""
		fscale = field.scale
		if fscale == 0:
			fscale = ""
		fdom = field.domain
		if fdom == "":
			fdom = "None"
		fdefv = field.defaultValue
		
		
		msg(fname + "," + falias + "," + ftype + "," + str(flen) + "," + str(fprec) + "," + str(fscale) + "," + fdom + "," + str(fdefv))

	msg("\n\nDone!\n\n")


except Exception as e:
	msg("\n** Error **\n\n" + str(e))
	




