
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: labelscripts.py
Created: 20170825
Modified: 20170825
About: Script that assigns or changes label expressions.

"""




# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


## ==============================================================================================================
##                                                                     F U N C T I O N S / D E F I N I T I O N S
## ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
	return False
    
def GetLabelLayer(m, d, fc):
    for xx in arcpy.mapping.ListLayers(m, "", d):
        if not xx.isGroupLayer and not "Basemap" in xx.longName:
            ff = arcpy.Describe(xx).featureClass.path + "\\" + xx.name
            if ff == fc:
                return xx
    return None
    
def setMcCurtainAddLabel(lyr, v):
    if v == "McCurtain - Adds Minimal":
        exp = "[STRUCTURE_NUM]"
    elif v == "McCurtain - Adds Full Address":
        exp = "[STRUCTURE_NUM] & vbcrlf & [COMP_STR_NAME]"
    else:
        exp = "[STRUCTURE_NUM] & \" \"& [COMP_STR_NAME] & \" \" & [UNIT_DESIG]  & VBCRLF & [MAIL_ADD1]  & \" \" & [MAIL_ADD2] & \", \" & [MAIL_CITY] & \" \" & [MAIL_ZIP] & VBCRLF &  [LAST_NAME1] & \", \" & [FIRST_NAME1] & VBCRLF & [LAST_NAME2] & \", \" & [FIRST_NAME2] & vbcrlf &[LL_PHONE1] & \":\" & [LL_PHONE2]  & [CELL_PHONE1] & \":\" & [CELL_PHONE2] & vbcrlf & [DATE_CREATED] & \" | \" & [DATE_MODIFIED] & vbcrlf & [NOTE1] & vbcrlf & [NOTE2]"
    lyr.labelClasses[0].expression = exp




        
## ==============================================================================================================
##                                                                           I N I T I A L I Z E   S C R I P T
## ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
thelabel = arcpy.GetParameterAsText(0)			# the layer and type of label to assign
xxx = arcpy.GetParameterAsText(1)			    # dummy parameter; feature class; not used for anything


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fcPolkAdd = "C:\data\SDR\Projects_Data\Missouri\MO_Polk_County\LIVE\GIS\Polk_County_911.gdb\Addressing\Polk_Addresses"
fcPolkRoad = "C:\data\SDR\Projects_Data\Missouri\MO_Polk_County\LIVE\GIS\Polk_County_911.gdb\Addressing\Polk_Centerlines"
fcNewtAdd = "C:\data\SDR\Projects_Data\Missouri\MO_Newton_County\LIVE\GIS\Newton_Live.gdb\CAD_Layers\Addresses"
fcNewtRoad = "C:\data\SDR\Projects_Data\Missouri\MO_Newton_County\LIVE\GIS\Newton_Live.gdb\CAD_Layers\MONEWTss"
fcMcCAdd = "C:\data\SDR\Projects_Data\Oklahoma\OK_McCurtain_County\LIVE\GIS\McCurtain_LIVE.gdb\AddressIt\Addresses"
fcMcCRoad = "C:\data\SDR\Projects_Data\Oklahoma\OK_McCurtain_County\LIVE\GIS\McCurtain_LIVE.gdb\AddressIt\Centerlines"

mxd = arcpy.mapping.MapDocument("CURRENT")
df = mxd.activeDataFrame

        

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	





## ==============================================================================================================
##                                                                                        D O   T H E   W O R K
## ==============================================================================================================

if "Polk - Adds" in thelabel:
    fc = fcPolkAdd
    if thelabel == "Polk - Adds Minimal":
        msg("xxx")
elif "Newton - Adds" in thelabel:
    fc = fcNewtAdd
elif "McCurtain - Adds" in thelabel:
    lblyr = GetLabelLayer(mxd, df, fcMcCAdd)
    if not lblyr is None:
        setMcCurtainAddLabel(lblyr, thelabel)

try:
    q = 1
    # wc = BuildWhereClause(lyrA, resultfield, "--")
    # arcpy.SelectLayerByAttribute_management(lyrA, "NEW_SELECTION", wc)
    # arcpy.CalculateField_management(lyrA, resultfield, "\"Fail: Out of Range\"", "VB", "")
    # arcpy.SelectLayerByAttribute_management(lyrA, "CLEAR_SELECTION")

except Exception as e:
    msg("\n**********************************************************************************")
    msg("There was an error checking for out of range addresses.")
    msg("Error message:\n  " + str(e))
    msg("**********************************************************************************\n")


    

msg("\n\nDone!\n\n")

