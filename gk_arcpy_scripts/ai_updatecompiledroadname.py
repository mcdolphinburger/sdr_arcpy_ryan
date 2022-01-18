
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: ai_updatecompiledroadname.py
Created: 20120717
Modified: 20170612
About: Updates the compiled road names in the selkected layer. Assumes the data is in AddressIt format.

"""





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
	
def CalculateRoadName(rn1, rn2, rn3, rn4):
	rn = (rn1 + " " + rn2).strip()
	rn = (rn + " " + rn3).strip()
	rn = (rn + " " + rn4).strip()
	return rn


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------
msg("\n\nCalculating/Updating Compiled Road Name\n---------------------------------------------------------------\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
FL = arcpy.GetParameterAsText(0)                # feature layer to act on
VER = arcpy.GetParameterAsText(1)               # string indicating version of AI to process
doTrim = arcpy.GetParameterAsText(2)            # boolean on whether to trim the fields prior to processing

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
lyrfds = arcpy.ListFields(FL)
if VER == "AddressIt 2.3":
    PRE = "PRE_DIR"
    PRT = "PRE_TYPE"
    NAM = "STREET_NAME"
    SUF = "STREET_TYPE"
    PDR = "POST_DIR"
    CNAM = "COMP_STR_NAME"
else:
    PRE = "PREFIX"
    PRT = "PRE_TYPE"
    SUF = "SUFFIX"
    PDR = "POSTDIR"
    CNAM = "RDNAME"
    if VER == "AddressIt 2.1 Addresses":
        NAM = "ROAD_NAME"
    else:
        NAM = "NAME"
		
curfields = [PRE, NAM, SUF, PDR, CNAM]






# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

# Trimming all road name fields in the layer
# --------------------------------------------------------------------------------------------------------------
if doTrim == "YES":
	msg("Trimming layer road name fields...")
	arcpy.CalculateField_management(FL, PRE, "!" + PRE + "!.strip()", "PYTHON_9.3", "")
	arcpy.CalculateField_management(FL, NAM, "!" + NAM + "!.strip()", "PYTHON_9.3", "")
	arcpy.CalculateField_management(FL, SUF, "!" + SUF + "!.strip()", "PYTHON_9.3", "")
	arcpy.CalculateField_management(FL, PDR, "!" + PDR + "!.strip()", "PYTHON_9.3", "")

# Calculating layer road name values
# --------------------------------------------------------------------------------------------------------------
msg("Calculating road names in layer...")
cur = arcpy.da.UpdateCursor(FL, curfields)	
for row in cur:
    r1 = row[0].strip()
    r2 = row[1].strip()
    r3 = row[2].strip()
    r4 = row[3].strip()
    val = CalculateRoadName(r1, r2, r3, r4)
    row[4] = val
    cur.updateRow(row)

	

	
	
arcpy.AddMessage("\n\nDone!\n\n")



	




