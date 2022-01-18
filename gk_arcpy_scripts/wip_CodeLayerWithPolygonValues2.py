# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# CodeLayerWithPolygonValues1.py
# Created on: 2012-02-20
#
#
# Description: 
# ----------------
#  
# 
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import modules
# ---------------------------
import arcpy, datetime, os


# ==============================================================================================================
#                                                                             F   U   N   C   T   I   O   N   S
# ==============================================================================================================


def FieldExists(fields, fname):
	doesexist = "FALSE"
	for fld in fields:
		if fld.Name == fname:
			doesexist = "TRUE"
	return doesexist

def CreateTextField(lyr, fname, len):
	arcpy.AddField_management(lyr, fname, "TEXT", "", "", len, fname, "NULLABLE", "NON_REQUIRED", "")
	
def CalculateRoadName(fet, v):
# 	v = version constant. Possible values are:
#			"2.11" = AddressIt version 2.1 Addresses
#			"2.12" = AddressIt version 2.1 Roads
#			"2.2"  = AddressIt version 2.2

	if v == "2.11":
		PRE = "PREFIX"
		NAM = "ROAD_NAME"
		SUF = "SUFFIX"
		PDR = "POSTDIR"
	elif v == "2.12":
		PRE = "PREFIX"
		NAM = "NAME"
		SUF = "SUFFIX"
		PDR = "POSTDIR"
	elif v == "2.2":
		PRE = "PRE_DIR"
		NAM = "STREET_NAME"
		SUF = "STREET_TYPE"
		PDR = "POST_DIR"
		
	rn1 = fet.getValue(PRE).strip()
	rn2 = fet.getValue(NAM).strip()
	rn3 = fet.getValue(SUF).strip()	
	rn4 = fet.getValue(PDR).strip()
	rn = (rn1 + " " + rn2).strip()
	rn = (rn + " " + rn3).strip()
	rn = (rn + " " + rn4).strip()
	return rn
	
def msg(msg):
	arcpy.AddMessage(msg)

def parity(num):
	if num == 0:
		p = "X"
	elif num/2 == int(num/2):
		p = "E"
	else:
		p = "O"
	return p

def test_address(a, mn, mx, ap, rp):
	if len(rp) == 4:
		v1 = rp[0:2]
		v2 = rp[2:len(rp)]
	
	if len(rp) == 4 and (v1 == "EE" or v1 == "OO") and (v2 == "EE" or v2 == "OO") and a >= mn and a <= mx:
		val = "GOOD"
	elif len(rp) == 2 and ap == "E" and rp == "EE" and a >= mn and a <= mx:
		val = "GOOD-E"
	elif len(rp) == 2 and ap == "O" and rp == "OO" and a >= mn and a <= mx:
		val = "GOOD-O"
	else:
		val = "FAIL"
	
	return val
	
def CalculatePCONST(x1, x2, y1, y2):
	if x1 == 0:
		cLF = "X"
	elif x1/2 == int(x1/2):
		cLF = "E"
	else:
		cLF = "O"
	if x2 == 0:
		cLT = "X"
	elif x2/2 == int(x2/2):
		cLT = "E"
	else:
		cLT = "O"
	if y1 == 0:
		cRF = "X"
	elif y1/2 == int(y1/2):
		cRF = "E"
	else:
		cRF = "O"
	if y2 == 0:
		cRT = "X"
	elif y2/2 == int(y2/2):
		cRT = "E"
	else:
		cRT = "O"
		
	return cLF + cLT + cRF + cRT
	
#			Receives: describe object
#	 		 Returns: string indicating the kind of workspace of the input layer
#	---------------------------------------------------------------------------------
def GetWorkspaceType(ds):
	if (ds.dataElement.dataType) == "ShapeFile":
		work = "shape"
	elif (ds.dataElement.dataType) == "FeatureClass":
		p = ds.dataElement.catalogPath
		if ".mdb" in p:
			work = "pers"
		else:
			work = "file"
	else:
		work = "unk"
	return work


	
	
	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	
	
	

# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyrT = arcpy.GetParameterAsText(0)								# Target Feature Layer (layer getting coded)
fT = arcpy.GetParameterAsText(1)								# Target field to receive values
lyrS = arcpy.GetParameterAsText(2)								# Source Feature Layer (selecting layer)
fS = arcpy.GetParameterAsText(3)								# Source field to derive values from



# Initialize some variables.
# --------------------------------------------------------------------------------------------------------------
descT = arcpy.Describe(lyrT)
descS = arcpy.Describe(lyrS)
fcT = descT.FeatureClass
fcS = descS.Featureclass
fieldsT = fcT.Fields
fieldsS = fcS.Fields
countT = int(arcpy.GetCount_management(lyrT).getOutput(0))
countS = int(arcpy.GetCount_management(lyrS).getOutput(0))



# Introduction message
# -------------------------------------------------------------------------------------------------------------
msg("\n\n")
msg("Coding field '" + fT + "' in '" + lyrT + "' with values from field '" + fS + "' in '" + lyrS + "'")
msg("==================================================================================================\n\n")
msg("Target Layer feature count: " + str(countT) + "\nSource Layer feature count: " + str(countS) + "\n\n")





# ==============================================================================================================
#                                                                             		      D O   T H E   W O R K
# ==============================================================================================================


	

# Identify features completely outside the polygons and code accordingly
# --------------------------------------------------------------------------------------------------------------
msg("Coding features completely outside all polygons . . .")
arcpy.SelectLayerByLocation_management(lyrT, "INTERSECT", lyrS, "", "NEW_SELECTION")
arcpy.SelectLayerByLocation_management(lyrT, "INTERSECT", lyrS, "", "SWITCH_SELECTION")
arcpy.CalculateField_management(lyrT, fT, "-1", "VB", "")
arcpy.SelectLayerByAttribute_management(lyrT, "CLEAR_SELECTION","")


# Identify features completely inside the polygons and code accordingly
# --------------------------------------------------------------------------------------------------------------
msg("Coding features completely inside all polygons . . .")
curS1 = arcpy.SearchCursor(lyrS)
for rowS1 in curS1:
	val = rowS1.getValue(fS)
	msg("[" + fS + "] = " + str(val))
	arcpy.SelectLayerByAttribute_management(lyrS, "NEW_SELECTION", "[" + fS + "] = " + str(val))
	arcpy.SelectLayerByLocation_management(lyrT, "COMPLETELY_WITHIN", lyrS, "", "NEW_SELECTION")
	arcpy.CalculateField_management(lyrT, fT, val, "VB", "")
	arcpy.SelectLayerByAttribute_management(lyrT, "CLEAR_SELECTION","")
	arcpy.SelectLayerByAttribute_management(lyrS, "CLEAR_SELECTION","")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
# # Pass 3: Check for valid road names.
# # --------------------------------------------------------------------------------------------------------------
# arcpy.AddMessage("Pass 3: Checking for valid road names...")
# acur3 = arcpy.UpdateCursor(FL1)

# for afeat3 in acur3:
	# val = afeat3.getValue("RACT")
	# if val == "":
		# # Get address feature road name
		# val1 = build_rdname1(afeat3)
		# flag = "false"
		# for n, p in dictRRN.iteritems():
			# if val1 == n:
				# flag = "true"
				# val = "RDNAME OK"
				# break
		# if flag == "false":
			# val = "RNF"
	# # arcpy.AddMessage(val)
	# afeat3.RACT = val	
	# acur3.updateRow(afeat3)




# # Pass 4: Check for valid addresses.
# # --------------------------------------------------------------------------------------------------------------
# arcpy.AddMessage("Pass 4: Checking for valid addresses...")

# acur4 = arcpy.UpdateCursor(FL1)
# for afeat4 in acur4:
	# if afeat4.getValue("RACT") == "RDNAME OK":
		# arn = build_rdname1(afeat4)
		# anum = float(afeat4.getValue(ADD))
		# apar = parity(anum)
		# vPRE = afeat4.getValue(PRE).strip()
		# vANAM = afeat4.getValue(ANAM).strip()
		# vSUF = afeat4.getValue(SUF).strip()
		# vPDR = afeat4.getValue(PDR).strip()
		# wclause = "[" + PRE + "] = '" + vPRE + "' AND [" + RNAM + "] = '" + vANAM + "' AND [" + SUF + "] = '" + vSUF + "' AND [" + PDR + "] = '" + vPDR + "'"
		# msg(wclause)
		
		# # arcpy.SelectLayerByAttribute_management(FL2, "NEW_SELECTION", PRE + " = " + )
		
		# # "[PRE_DIR] = 'E' AND [STREET_NAME] = '11TH' AND [STREET_TYPE] = 'AVE' AND [POST_DIR] = ' '"
		
		# # rcur4 = arcpy.SearchCursor(FL2)
		# # for rfeat4 in rcur4:
			# # pconst = rfeat4.getValue("PCONST")
			# # pl = pconst[0:2]
			# # pr = pconst[2:len(pconst)]
			# # rrn = build_rdname2(rfeat4)
			# # vLF = rfeat4.getValue(LF)
			# # vLT = rfeat4.getValue(LT)
			# # vRF = rfeat4.getValue(RF)
			# # vRT = rfeat4.getValue(RT)
			# # if arn == rrn and pl == "XX" and pr != "XX":
				# # mn = vRF
				# # mx = vRT
				# # val = test_address(anum, mn, mx, apar, pr)
			# # elif arn == rrn and pl != "XX" and pr == "XX":
				# # mn = vLF
				# # mx = vLT
				# # val = test_address(anum, mn, mx, apar, pl)
			# # elif arn == rrn and pl == "XX" and pr == "XX":
				# # val = "FAIL"
			# # else:
				# # mn = min(vLF, vLT, vRF, vRT)
				# # mx = max(vLF, vLT, vRF, vRT)
				# # val = test_address(anum, mn, mx, apar, pconst)

			# # if val == "GOOD" or val == "GOOD-E" or val == "GOOD-O":
				# # msg(val)
				# # afeat4.RACT = val
				# # acur4.updateRow(afeat4)
				# # break
			



msg("Done!")

arcpy.AddMessage("\n\n\n")



	




