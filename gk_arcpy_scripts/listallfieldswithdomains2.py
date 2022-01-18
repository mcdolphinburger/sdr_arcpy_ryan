
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: listallfieldswithdomains.py
Created: 20180420
Modified: xxxxxxx
About: Examines all feature classes in the specified workspace and lists all fields with domains
       assigned to them, along with the domain name.

"""




# Import modules
# ---------------------------
import arcpy, sys, string, datetime, os, fileinput
from arcpy import env
from arcpy import mapping


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)




	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
ws = arcpy.GetParameterAsText(0)						# the workspace to examine


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
arcpy.env.workspace = ws
datasets = arcpy.ListDatasets("*", "Feature")
fcs = arcpy.ListFeatureClasses()








# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\nSearching " + ws + " for fields with domains.")



## ==============================================================================================================
##                                                                                        D O   T H E   W O R K
## ==============================================================================================================

if fcs != "":
	for fc in arcpy.ListFeatureClasses():
		for fd in arcpy.ListFields(fc):
			#if fd.name == "STRUCTURE_COMP" or fd.name == "STRUCTURE_TYPE":
			if fd.domain != "":
				msg(fc + ": " + fd.name + " -> " + fd.domain)
			
if datasets != "":
	for ds in datasets:
		for fc in arcpy.ListFeatureClasses("", "", ds):
			for fd in arcpy.ListFields(fc):
				#if fd.name == "STRUCTURE_COMP" or fd.name == "STRUCTURE_TYPE":
				if fd.domain != "":
					msg(fc + ": " + fd.name + " -> " + fd.domain)

						
						
						
						
						
						
						