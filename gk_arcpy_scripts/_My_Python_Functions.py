
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: _My_Python_Functions.py
Created: 20161219
Modified: 
About: Module for my commonly used functions that can be shared among my scripts.

"""


# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, os, string, datetime, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

# Receives a string indicating the AddressIt version and a row object from a cursor
# and calculates the compiled street name.
# Specific to AddressIt 2.1 and AddressIt 2.2.
def CalcAI23Rdname(v, rw):
	if v == "AddressIt 2.2":
		PRE = rw.getValue("PRE_DIR").strip()
		NAM = rw.getValue("STREET_NAME").strip()
		SUF = rw.getValue("STREET_TYPE").strip()
		PDR = rw.getValue("POST_DIR").strip()
	else:
		PRE = rw.getValue("PREFIX").strip()
		SUF = rw.getValue("SUFFIX").strip()
		if not rw.getValue("POST_DIR"):
			PDR = ""
		else:
			PDR = rw.getValue("POST_DIR").strip()
		if v == "AddressIt 2.1 Addresses":
			NAM = rw.getValue("ROAD_NAME").strip()
		else:
			NAM = rw.getValue("NAME").strip()
	rn = (PRE + " " + NAM).strip()
	rn = (rn + " " + SUF).strip()
	rn = (rn + " " + PDR).strip()
	return rn
	
def CreateField1(lyr, nam, typ, len):
	arcpy.AddField_management(lyr, nam, typ, "", "", ln, nam, "NULLABLE", "NON_REQUIRED", "")
	
	
def IsNumericField(fld):
	if fld == "FLOAT":
		return True
	elif fld == "DOUBLE":
		return True
	elif fld == "SHORT":
		return True
	elif fld == "LONG":
		return True
	elif fld == "Integer":
		return True
	elif fld == "SmallInteger":
		return True
	elif fld == "Single":
		return True
	elif fld == "Double":
		return True
	else:
		return False
        
        
def LayerHasSelection(lyr):
    ct = len(arcpy.Describe(lyr).fidSet.split(";"))
    if ct > 0:
        return True
    else:
        return False
	






