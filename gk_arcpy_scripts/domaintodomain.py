
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: domaintodomain.py
Created: 20180929
Modified: 20180929
About: Copies domains from one geodatabase to another.

"""



# Import arcpy module
import arcpy, arcpy.mapping, sys, string, datetime, os, fileinput
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================

def msg(msg):
	arcpy.AddMessage(msg)
	
def ValidateWorkspace(gdb):
	if gdb[-4:] == ".gdb" or gdb[-4:] == "mdb":
		msg("\nWorkspace validated, continue.\n")
	else:
		msg("\nInvalid workspace, stopping.\n")
		exit()

def CleanUpTables(gdb, t):
	arcpy.env.workspace = gdb
	t2 = arcpy.ListTables()
	for i in t:
		if i in t2:
			arcpy.Delete_management(i)



# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================

# Script arguments
# -------------------------------------------------------------
gdbS = arcpy.GetParameterAsText(0)			# Source geodatabase
gdbT = arcpy.GetParameterAsText(1)			# Target geodatabase



# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
# gdbS = "C:\data\SDR\Projects_Data\Kansas\NG911\LIVE\GIS\KSNG911N.gdb"
# gdbT = "C:\data\SDR\Projects_Data\Kansas\NG911\LIVE\CSRs\Brown_County_Live.gdb"
domS = arcpy.da.ListDomains(gdbS)			# List of all the domains in the source geodatabase
tbls = []


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg(gdbS)
msg(gdbT)



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

ValidateWorkspace(gdbS)

# Create tables of all the domains in the source geodatabase
arcpy.env.workspace = gdbS
for dom in domS:
	msg(dom.name)
	tblnam = "d_" + dom.name
	arcpy.DomainToTable_management(gdbS, dom.name, tblnam, "CODE", "DESCRIPTION")
	tbls.append(tblnam)
	arcpy.TableToDomain_management(tblnam, "CODE", "DESCRIPTION", gdbT, dom.name)
	arcpy.Delete_management(tblnam)



# Parsing strings
# --------------------------------------------------------------------------------------------------------------------------------
# Get the first N characters in a string: val[:N], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value

# CleanUpTables(gdbS, tbls)

msg("\n\nDone!\n\n")


