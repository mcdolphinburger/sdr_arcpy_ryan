

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: ai_updatecompiledroadnameandfulladdress.py
Created: 20120605
Modified: 20170612
About: Re-calculates the AddressIt compiled road name and updates the full address value.

"""

# Import modules
# ---------------------------
import sys, arcpy, string, datetime, arcpy.mapping


## ==============================================================================================================
##                                                                     F U N C T I O N S / D E F I N I T I O N S
## ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)

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
m = "\n\nCalculating and Updating Compiled Road Name and Full Address values"
m = m + "\n------------------------------------------------------------------------\n"
msg(m)


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrR = arcpy.GetParameterAsText(0)
lyrA = arcpy.GetParameterAsText(1)
doPRT = arcpy.GetParameter(2)

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------

if doPRT:
    cursorfieldsR = ["PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME", "PRE_TYPE"]
    cursorfieldsA = ["STRUCTURE_NUM", "PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME", "FULL_ADDRESS", "PRE_TYPE"]
else:
    cursorfieldsR = ["PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME"]
    cursorfieldsA = ["STRUCTURE_NUM", "PRE_DIR", "STREET_NAME", "STREET_TYPE", "POST_DIR", "COMP_STR_NAME", "FULL_ADDRESS"]


## ==============================================================================================================
##                                                                                        D O   T H E   W O  R K
## ==============================================================================================================



# Calculating road centerline road name values
# --------------------------------------------------------------------------------------------------------------
msg("Calculating road names in road centerline data.")
row, cur = None, None
cur = arcpy.da.UpdateCursor(lyrR, cursorfieldsR)	
for row in cur:
    r1 = row[0].strip()
    if doPRT:
        r2 = row[5].strip()
    else:
        r2 = ""
    r3 = row[1].strip()
    r4 = row[2].strip()
    r5 = row[3].strip()
    rn = CalculateRoadName(r1, r2, r3, r4, r5)
    row[4] = rn
    cur.updateRow(row)


# Calculating address point road names anf dull addresses
# --------------------------------------------------------------------------------------------------------------
msg("Calculating road names and full addresses in address point data.")
row, cur = None, None
cur = arcpy.da.UpdateCursor(lyrA, cursorfieldsA)	
for row in cur:
    a = row[0]
    r1 = row[1].strip()
    if doPRT:
        r2 = row[7].strip()
    else:
        r2 = ""
    r3 = row[2].strip()
    r4 = row[3].strip()
    r5 = row[4].strip()
    rn = CalculateRoadName(r1, r2, r3, r4, r5)
    fa = (str(a) + " " + rn).strip()
    row[5] = rn
    row[6] = fa
    cur.updateRow(row)
    
    

arcpy.AddMessage("\n\nDone!\n\n")



	




