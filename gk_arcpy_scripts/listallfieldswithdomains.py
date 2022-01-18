
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: listallfieldswithdomains.py
Created: 20180420
Modified: xxxxxxx
About: Examines all feature layers in the active data frame and lists all fields with domains
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


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
mxd = arcpy.mapping.MapDocument("CURRENT")







# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\nSearching for fields with domains.")



## ==============================================================================================================
##                                                                                        D O   T H E   W O R K
## ==============================================================================================================


for lyr in arcpy.mapping.ListLayers(mxd):
	if lyr.isFeatureLayer:
		for fd in arcpy.ListFields(lyr):
			if fd.domain != "":
				msg(lyr.name + " | " + fd.name + " | " + fd.domain)
				














# # Begin the compare process
# # ---------------------------------------------------------------------------------------------------------------		

# # Re-calculate full street names, if necessary.
# try:

	# if bolCalcName:
		# msg("Re-calculating full street names for Address Points")
		# with arcpy.da.UpdateCursor(lyrA, cursorfieldsA) as cur:
			# for row in cur:
				# nam = CalculateFullStreetName(row, streetnamefieldsA)
				# row[len(cursorfieldsA)-1] = nam
				# cur.updateRow(row)
		# msg("Re-calculating full street names for Street Centerlines\n")
		# with arcpy.da.UpdateCursor(lyrR, cursorfieldsR) as cur:
			# for row in cur:
				# nam = CalculateFullStreetName(row, streetnamefieldsR)
				# row[len(cursorfieldsR)-1] = nam
				# cur.updateRow(row)
	
		# del row, cur

# except Exception as e:
	# msg("\nThere was an error re-calculating the full street names.")
	# msg("Error message:\n  " + str(e) + "\n")
	# row, cur = None, None

	

	
# # Build street name dictionaries for both address points and centerlines
# try:
	
	# msg("Building Address Point street name dictionary")
	# row, cur = None, None
	# streetdicA = {}
	# with arcpy.da.SearchCursor(lyrA, fullstreetfieldA) as cur:
		# for row in cur:
			# if not row[0] in streetdicA:
				# streetdicA[row[0]] = row[0]
	# #msg(str(len(streetdicA)))

	# msg("Building Street Centerline street name dictionary")
	# row, cur = None, None
	# streetdicR = {}
	# with arcpy.da.SearchCursor(lyrR, fullstreetfieldR) as cur:
		# for row in cur:
			# if not row[0] in streetdicR:
				# streetdicR[row[0]] = row[0]
	# #msg(str(len(streetdicR)))


# except Exception as e:
    # msg("\nThere was an error building the street name dictionaries.")
    # msg("\n  Error message:\n  " + str(e))
    # row, cur = None, None


# # Check for zero addresses and road name mismatches
# try:
	# msg("\nPASS 1 of 2: Checking for zero House Numbers and Street Name mismatches")
	# curlistA = []
	# curlistA.append(housenumfield)
	# curlistA.append(fullstreetfieldA)
	# curlistA.append(resultfield)
	# with arcpy.da.UpdateCursor(lyrA, curlistA) as cur:
		# for row in cur:
			# if row[0] == 0 and row[1] in streetdicR:
				# row[2] = "Fail: Zero Add"
			# elif row[0] != 0 and not row[1] in streetdicR:
				# row[2] = "Fail: Name"
			# elif row[0] == 0 and not row[1] in streetdicR:
				# row[2] = "Fail: Name/Zero Add"	
			# else:
				# row[2] = "ok"
			# cur.updateRow(row)

	# curlist = None

# except Exception as e:
    # msg("\n**********************************************************************************")
    # msg("There was an error checking for zero addresses and name mismatches.")
    # msg("Error message:\n  " + str(e))
    # msg("**********************************************************************************\n")
    # curlistA = None
	
	
# try:
	# msg("PASS 2 of 2: Checking for out of range addresses")
	# curlistR = []
	# curlistR.append(fullstreetfieldR)
	# curlistR.append(rnglowfld)
	# curlistR.append(rnghifld)
	# expr = BuildWhereClause(lyrA, resultfield, "ok")
	# cur = arcpy.da.UpdateCursor(lyrA, curlistA, expr)
	# for row in cur:
		# a = row[0]
		# n = row[1]
		# flag = False
		# curR = arcpy.da.SearchCursor(lyrR, curlistR)
		# for rowR in curR:
			# na = rowR[0]
			# lw = rowR[1]
			# hi = rowR[2]
			# if n == na and a >= lw and a <= hi:
				# res = "Pass"
				# flag = True
		# if flag == False:
			# res = "Fail: Out of Range"
		# row[2] = res
		# cur.updateRow(row)

	# cur, row, curR, rowR = None, None, None, None

# except Exception as e:
    # msg("\n**********************************************************************************")
    # msg("There was an error checking for out of range addresses.")
    # msg("Error message:\n  " + str(e))
    # msg("**********************************************************************************\n")
    # curlistR = None
    



msg("\n\nDone!\n\n")

