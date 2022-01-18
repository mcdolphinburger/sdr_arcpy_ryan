"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: codeaddresspointparity.py
Created: 20200708
Modified: 20200708
About: Code the Parity field of an address point layer with parity values
		Z = House Number is Zero
		E = House Number is Even
		O = House Number is Odd

"""

# Import modules
# ---------------------------
import arcpy, datetime, os, string, arcpy.mapping, _My_Python_Functions
from _My_Python_Functions import IsNumericField
from fractions import Fraction


# ==============================================================================================================
#                                                                             F   U   N   C   T   I   O   N   S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)

def GetFieldType(lyr, nam):
	for fd in arcpy.ListFields(lyr):
		if fd.name == nam:
			return fd.type
			
def GetWorkspaceType(d):
	if (d.dataElement.dataType) == "ShapeFile":
		return "shape"
	elif (d.dataElement.dataType) == "FeatureClass":
		p = d.dataElement.catalogPath
		if ".mdb" in p:
			return "pers"
		else:
			return "file"
	else:
		return "unk"

def GetSelectionCount(lyr):
	sourcecount = int(arcpy.GetCount_management(fc1).getOutput(0))
    

def IsANumber(n):
	try:
		float(n)
		return True
	except ValueError:
		try:
			Fraction(n)
			return True
		except ValueError:
			return False
            
		

# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	

	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrAP = arcpy.GetParameterAsText(0)					# The Address Point layer
fHN = arcpy.GetParameterAsText(1)					# The field containing House Number values
fP = arcpy.GetParameterAsText(2)					# The field for Parity values



# Introduction message
# -------------------------------------------------------------------------------------------------------------
msg("\nCoding the selected layer with parity values.\n")




# ==============================================================================================================
#                                                                             		      D O   T H E   W O R K
# ==============================================================================================================


arcpy.SelectLayerByAttribute_management(lyrAP, "CLEAR_SELECTION","")

cur = arcpy.da.UpdateCursor(lyrAP, [fHN, fP])
for row in cur:
	HN = row[0]
	if HN == 0:
		row[1] = "Z"
	elif HN % 2 == 0:
		row[1] = "E"
	else:
		row[1] = "O"
	cur.updateRow(row)




msg("\n\nDone!\n\n")



	




