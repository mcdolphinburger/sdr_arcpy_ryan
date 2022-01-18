
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: ai_updatecompiledroadname.py
Created: 20120717
Modified: 20170612
About: Updates the compiled road names in the selected layer. Assumes the data is in AddressIt format.

"""





# Import modules
# ---------------------------
import sys, arcpy, string, datetime


## ==============================================================================================================
##                                                                     F U N C T I O N S / D E F I N I T I O N S
## ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(fields, fname):
	for fld in fields:
		if fld.Name == fname:
			return True
	return False
	
def CalculateRoadName(rn1, rn2, rn3, rn4, rn5):
    rn = (rn1 + " " + rn2).strip()
    rn = (rn + " " + rn3).strip()
    rn = (rn + " " + rn4).strip()
    rn = (rn + " " + rn5).strip()
    return rn


	
## ==============================================================================================================
##                                                                             I N I T I A L I Z E   S C R I P T
## ==============================================================================================================
	
	
	
# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------
msg("\n\nCalculating/Updating Compiled Road Name\n---------------------------------------------------------------\n\n")


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)               # feature layer to act on
ver = arcpy.GetParameterAsText(1)               # string indicating version of AI to process
doPRT = arcpy.GetParameter(2)                   # boolean on whether the road name fields use the Pre Type field or not

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
if ver == "AddressIt 2.3" and doPRT:
    cursorfields = ["PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME", "PRE_TYPE"]
elif ver == "AddressIt 2.3" and not doPRT:
    cursorfields = ["PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME"]
elif ver == "AddressIt 2.1 Addresses" and doPRT:
    cursorfields = ["PREFIX", "ROAD_NAME", "SUFFIX", "POSTDIR", "RDNAME", "PRE_TYPE"]
elif ver == "AddressIt 2.1 Addresses" and not doPRT:
    cursorfields = ["PREFIX", "ROAD_NAME", "SUFFIX", "POSTDIR", "RDNAME"]
elif doPRT:
    cursorfields = ["PREFIX", "NAME", "SUFFIX", "POSTDIR", "RDNAME", "PRE_TYPE"]
else:
    cursorfields = ["PREFIX", "NAME", "SUFFIX", "POSTDIR", "RDNAME"]

    
    
    

## ==============================================================================================================
##                                                                                        D O   T H E   W O  R K
## ==============================================================================================================




# Calculating layer road name values
# --------------------------------------------------------------------------------------------------------------
msg("Calculating road names in layer.")
cur = arcpy.da.UpdateCursor(lyr, cursorfields)	
for row in cur:
	r1 = row[0].strip()
	if doPRT:
		r2 = row[5].strip()
	else:
		r2 = ""
	r3 = row[1].strip()
	r4 = row[2].strip()
	r5 = row[3].strip()
	val = CalculateRoadName(r1, r2, r3, r4, r5)
	row[4] = val
	cur.updateRow(row)

	

	
	
arcpy.AddMessage("\n\nDone!\n\n")



	




