# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# AI_CompareStreetNames.py
# Created on: 2013-05-06
#
#
# Description: 
# ----------------
#  
# 
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: buildroadnamematrix.py
Created: 20201109
Modified: 20201109
About: Creates a comma-delimited list of road names from multiple sources with characters denoting if that
       road name is present in the input data sources.

"""

# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(lyr, fname):
	doesexist = False
	for fld in arcpy.ListFields(lyr):
		if fld.name == fname:
			doesexist = True
	return doesexist
	









# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
table1 = arcpy.GetParameterAsText(0)				# the first feature layer/table with road name data in its attribute table
field1 = arcpy.GetParameterAsText(1)				# the field in the first feature layer/table containing the road name data
table2 = arcpy.GetParameterAsText(2)				# the second feature layer/table with road name data in its attribute table
field2 = arcpy.GetParameterAsText(3)				# the field in the second feature layer/table containing the road name data
table3 = arcpy.GetParameterAsText(4)				# the third feature layer/table with road name data in its attribute table
field3 = arcpy.GetParameterAsText(5)				# the field in the third feature layer/table containing the road name data



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
dict_matrix = {}
dict_tb1 = {}
dict_tb2 = {}
dict_tb3 = {}




# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\nBuilding a road name matrix from the following sources:")
msg("  " + table1)
msg("  " + table2)
if table3:
	msg("  " + table3)





# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

msg("\nBuilding all road name dictionaries.")

# begin building matrix road name dictionary
# build table1 dictionary
curfields = []
curfields.append(field1)
cur = arcpy.da.SearchCursor(table1, curfields)
for row in cur:
	if not row[0] in dict_matrix.keys():
		dict_matrix[row[0]] = row[0]
	if not row[0] in dict_tb1.keys():
		dict_tb1[row[0]] = row[0]		
cur, row = None, None

# continue building matrix road name dictionary
# build table2 dictionary
curfields = []
curfields.append(field2)
cur = arcpy.da.SearchCursor(table2, curfields)
for row in cur:
	if not row[0] in dict_matrix.keys():
		dict_matrix[row[0]] = row[0]
	if not row[0] in dict_tb2.keys():
		dict_tb2[row[0]] = row[0]		
cur, row = None, None

# finish building matrix road name dictionary
# build table3 dictionary (if necessary)
if table3:
	curfields = []
	curfields.append(field3)
	cur = arcpy.da.SearchCursor(table3, curfields)
	for row in cur:
		if not row[0] in dict_matrix.keys():
			dict_matrix[row[0]] = row[0]
		if not row[0] in dict_tb3.keys():
			dict_tb3[row[0]] = row[0]		
cur, row = None, None

msg("\n\n")
msg(str(len(dict_tb1)))
msg(str(len(dict_tb2)))
msg(str(len(dict_tb3)))
msg(str(len(dict_matrix)))


for k in dict_matrix:
	line = k + ","
	if k in dict_tb1:
		line = line + "x,"
	else:
		line = line + ","
	if k in dict_tb2:
		line = line + "x,"
	else:
		line = line + ","
	if k in dict_tb3:
		line = line + "x"
	msg(line)










# # Verify that the field exists for holding the compare results for each layer.
# # If the doesn't exist, create it.
# # -------------------------------------------------------------------------------------
# if FieldExists(lyr1, "RNC"):
	# msg("Field RNC exists in layer 1? TRUE")
# else:
	# arcpy.AddField_management(lyr1, "RNC", "TEXT", "", "", "64", "RNC", "NULLABLE", "NON_REQUIRED", "")
	# msg("Field RNC exists in layer 1? FALSE, field created")	
	
# if FieldExists(lyr2, "RNC"):
	# msg("Field RNC exists in layer 2? TRUE\n")
# else:
	# arcpy.AddField_management(lyr2, "RNC", "TEXT", "", "", "64", "RNC", "NULLABLE", "NON_REQUIRED", "")
	# msg("Field RNC exists in layer 2? FALSE, field created\n")

# # Create a road name dictionary for layer 1
# # -------------------------------------------------------------------------------------	
# msg("Creating Street Name dictionary for layer 1.")
# dic1 = {}
# row, cur = None, None
# cur = arcpy.SearchCursor(lyr1)
# for row in cur:
	# sn = CalcStreetName(1, row)
	# dic1[sn] = sn

# # Create a road name dictionary for layer 2
# # -------------------------------------------------------------------------------------
# msg("Creating Street Name dictionary for layer 2.\n")
# dic2 = {}
# row, cur = None, None
# cur = arcpy.SearchCursor(lyr2)
# for row in cur:
	# sn = CalcStreetName(2, row)
	# dic2[sn] = sn

# # Compare road names in layer 1 to layer 2, write results in layer 1
# # -------------------------------------------------------------------------------------
# msg("Writing Street Name compare results to layer 1.")
# cur, row = None, None
# cur = arcpy.UpdateCursor(lyr1)
# for row in cur:
	# sn = CalcStreetName(1, row)
	# if not sn in dic2.keys():
		# row.setValue("RNC", "NO MATCH")
	# else:
		# row.setValue("RNC", "GOOD")
	# cur.updateRow(row)

# # Compare road names in layer 2 to layer 1, write results in layer 2
# # -------------------------------------------------------------------------------------	
# msg("Writing Street Name compare results to layer 2.")
# cur, row = None, None
# cur = arcpy.UpdateCursor(lyr2)
# for row in cur:
	# sn = CalcStreetName(2, row)
	# if not sn in dic1.keys():
		# row.setValue("RNC", "NO MATCH")
	# else:
		# row.setValue("RNC", "GOOD")
	# cur.updateRow(row)
# cur, row = None, None




	


msg("\n\nDone!\n\n")



	




