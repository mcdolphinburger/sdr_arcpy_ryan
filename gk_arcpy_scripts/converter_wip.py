"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: Cconverterwip.py
Created: 20170602
Modified: xxxxxxxx
About: Parctice script for converting input data to an output dataset with different names, using Insert cursors.
"""

# Import modules
# ---------------------------
import sys, arcpy, arcpy.mapping, string, datetime, os


# Script Functions
# --------------------------------------------------------------------------------------------------------------
def msg(msg):
	arcpy.AddMessage(msg)
		
def FieldExists(fields, fname):
	for fld in fields:
		if fld.name == fname:
			return True
	return False
	
def IsDeletableField(fd):
	if (fd.required or fd.name == "JOINID" or fd.name == "DATASOURCE"):
		return False
	return True


# Script Arguments
# --------------------------------------------------------------------------------------------------------------
inLyr = arcpy.GetParameterAsText(0)
outLyr = arcpy.GetParameterAsText(1)


# Initialize Variables
# --------------------------------------------------------------------------------------------------------------
spref = arcpy.Describe(inLyr).spatialReference
pth = arcpy.Describe(inLyr).catalogPath

theschemaR = []
theschemaR = [
    ["JOINID", "LONG", "", "9", "", "JOINID"],
    ["DATASOURCE", "TEXT", "50", "", "", "DATASOURCE"],
    ["PREFIX", "TEXT", "2", "", "", "PRE_DIR"],
    ["NAME", "TEXT", "40", "", "", "STREET_NAME"],
    ["SUFFIX", "TEXT", "4", "", "", "STREET_TYPE"],
    ["POSTDIR", "TEXT", "2", "", "", "POST_DIR"],
    ["RDNAME", "TEXT", "51", "", "", "COMP_STR_NAME"],
    ["CLASSIFI", "TEXT", "50", "", "", "CLASSIFICATION"],
    ["ALIAS", "TEXT", "51", "", "", "ALIAS1"],
    ["ALIAS2", "TEXT", "51", "", "", "ALIAS2"],
    ["LEFT_FROM", "LONG", "", "6", "", "LEFT_FROM"],
    ["LEFT_TO", "LONG", "", "6", "", "LEFT_TO"],
    ["RIGHT_FROM", "LONG", "", "6", "", "RIGHT_FROM"],
    ["RIGHT_TO", "LONG", "", "6", "", "RIGHT_TO"],
    ["MSAG_COM_E", "TEXT", "32", "", "", "E911_COMM_E"],
    ["MSAG_COM_O", "TEXT", "32", "", "", "E911_COMM_O"],
    ["ZIP_COM_E", "TEXT", "32", "", "", "ZIP_COMM_E"],
    ["ZIP_COM_O", "TEXT", "32", "", "", "ZIP_COMM_O"],
    ["LANES", "SHORT", "", "4", "", "LANES"],
    ["SPEED", "SHORT", "", "4", "", "<none>"],
    ["WIDTH", "SHORT", "", "4", "", "<none>"],
    ["SURFACE", "TEXT", "32", "", "", "SURFACE"],
    ["SHOULDER", "TEXT", "5", "", "", "SHOULDER"],
    ["ONEWAY", "TEXT", "2", "", "", "ONE_WAY"],
    ["NOTE1", "TEXT", "150", "", "", "NOTE1"],
    ["NOTE2", "TEXT", "150", "", "", "NOTE2"],
    ["INDEX", "LONG", "", "9", "", "<none>"]
    ]	

theschemaA = []
theschemaA = [
    ["JOINID", "LONG", "", "9", "", "JOINID"],
    ["DATASOURCE", "TEXT", "50", "", "", "DATASOURCE"],
    ["NEW_ADD", "LONG", "", "8", "", "STRUCTURE_NUM"],
    ["ALPHA", "TEXT", "16", "", "", "UNIT_DESIG"],
    ["PREFIX", "TEXT", "2", "", "", "PRE_DIR"],
    ["ROAD_NAME", "TEXT", "40", "", "", "STREET_NAME"],
    ["SUFFIX", "TEXT", "4", "", "", "STREET_TYPE"],
    ["POSTDIR", "TEXT", "2", "", "", "POST_DIR"],
    ["RDNAME", "TEXT", "51", "", "", "COMP_STR_NAME"],
    ["FULL_ADDR", "TEXT", "100", "", "", "FULL_ADDRESS"],
    ["CITY", "TEXT", "32", "", "", "CITY"],
    ["STATE", "TEXT", "2", "", "", "STATE"],
    ["ZIP", "TEXT", "12", "", "", "ZIP"],
    ["ALIAS", "TEXT", "51", "", "", "ALIAS1"],
    ["ALIAS2", "TEXT", "51", "", "", "ALIAS2"],
    ["LAST_NAME", "TEXT", "50", "", "", "LAST_NAME1"],
    ["FIRST_NAME", "TEXT", "50", "", "", "FIRST_NAME1"],
    ["LNAME2", "TEXT", "50", "", "", "LAST_NAME2"],
    ["FNAME2", "TEXT", "50", "", "", "FIRST_NAME2"],
    ["PHONE", "TEXT", "14", "", "", "LL_PHONE1"],
    ["PHONE2", "TEXT", "14", "", "", "LL_PHONE2"],
    ["CPHONE1", "TEXT", "14", "", "", "CELL_PHONE1"],
    ["CPHONE2", "TEXT", "14", "", "", "CELL_PHONE2"],
    ["MAIL_ADD", "TEXT", "50", "", "", "MAIL_ADD"],
    ["MAIL_CITY", "TEXT", "32", "", "", "MAIL_CITY"],
    ["MAIL_STATE", "TEXT", "2", "", "", "MAIL_STATE"],
    ["STRUC_COMP", "TEXT", "20", "", "", "STRUCTURE_COMP"],
    ["STRUC_TYPE", "TEXT", "20", "", "", "STRUCTURE_TYPE"],
    ["NOTE1", "TEXT", "150", "", "", "NOTE1"],
    ["NOTE2", "TEXT", "150", "", "", "NOTE2"],
    ["HOTLINK", "TEXT", "100", "", "", "HOTLINK"],
    ["LONGITUDE", "DOUBLE", "", "19", "8", "LONGITUDE"],
    ["LATITUDE", "DOUBLE", "", "19", "8", "LATITUDE"],
    ["INDEX", "LONG", "", "9", "", "<none>"]
    ]







# Introduction Message
# --------------------------------------------------------------------------------------------------------------
msg("\n\n")


# Execute Script
# --------------------------------------------------------------------------------------------------------------

if "USER_NAME" in arcpy.ListFields(inLyr):
    msg("poop!")










# # ==============================================================================================================
# #                                                                     F U N C T I O N S / D E F I N I T I O N S
# # ==============================================================================================================


	
	
# # Receives a row of attributes from a list and a field name. Iterates through the list of fields names
# # to find the field index, then returns the attribute from the row attributes at that index.	
# def GetFieldValue(fmL, bL, rw, fn):
	# res = "x"
	# q = bL[rw]
	# for j in fmL:
		# if j[0] == fn:
			# outfname = j[5]
			# if outfname == "<none>" and j[1] == "TEXT":
				# res = ""
			# elif outfname == "<none>":
				# res = 0
			
	# k = -1
	# for f in bL[0]:
		# k = k + 1
		# if f == outfname:
			# res = q[k]
			# break
	# return res
	
# #  The main function of the converter.
# #  -------------------------------------------------------------------------------------------------
# ##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ##
# ##     ds = incoming data source.
# ##     lt = incoming layer type (adds, roads).
# ##    lyr = incoming layer.
# ## shpnam = the name of the output shapefile (no path, no file extension, just the name).
# ##    out = the folder to save the output shapefile in. A path.
# ##    bol = boolean on whether to do the street name compression or not.
# ##  spref = the spatial reference of the incoming layer.
# ##
# ##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# def ConvertDataSource(ds, lt, lyr, shpnam, out, bol, spref):

	# # Initialize main variables.
	# # --------------------------------------------------------------------------------------------------------------
	# d = arcpy.Describe(lyr)
	# fc = d.FeatureClass								# the Feature Class of the Incoming/Source data
	# lyrpath = d.catalogPath							# the file system path to the Incoming/Source data
	# fds = arcpy.ListFields(lyr)						# the fields object of the Incoming/Source data
	# pL, nL = os.path.split(lyrpath)					# the file system path to the Incoming/Source data geodatabase, and the Feature Class name
	# outshape = out + "\\" + shpnam + ".shp"			# the full path to the output shapefile
	# for fd in fds:
		# if fd.type == "OID":
			# fOID = fd.name							# the name of the Object ID field in the Incoming/Source data
	

	# msg("\n")
	# msg("   Agency Data Source: " + ds)
	# msg("            Data Type: " + lt)
	# msg("     Source Data Name: " + nL)
	# msg("Output Shapefile Name: " + shpnam + ".shp")
	# msg("        Output Folder: " + out)
	# msg("  Compress Road Names: " + str(bol))
	# msg("\n")	
	


	# # ==============================================================================================================
	# #                                                                                     D O   T H E   W O R K
	# # ==============================================================================================================

	# # 01: Prep incoming source data
	# # 02: Export the attribute table to Python tuple list object
	# # 03: Export the feature classes to shapefile and add to map
	# # 04: Delete all fields from new shapefile
	# # 05: Add Go2It fields to shapefile
	# # 06: Populate shapefile fields
	# # 07: (Optional) Run road name compression


	# # 01: Prep incoming data
	# # --------------------------------------------------------------------------------------------------------------
	# msg("Step 01: Prep Incoming data\n------------------------------------------------------------------------------")
	
	# try:
	
		# # Prep JOINID
		# if not FieldExists(fds, "JOINID"):
			# msg(lt + " JOINID field existed? FALSE\n    Calculating " + lt + " JOINID values.")
			# arcpy.AddField_management(lyr, "JOINID", "LONG", "", "", "", "JOINID", "NULLABLE", "NON_REQUIRED", "")
			# arcpy.CalculateField_management(lyr, "JOINID", "!" + fOID + "!", "PYTHON", "")
		# else:
			# msg(lt + " JOINID field existed? TRUE\n    Updating " + lt + " JOINID field.")
			# arcpy.CalculateField_management(lyr, "JOINID", "!" + fOID + "!", "PYTHON", "")
		
		# # Prep DATASOURCE
		# if not FieldExists(fds, "DATASOURCE"):
			# msg(lt + " DATASOURCE field existed? FALSE\n    Calculating " + lt + " DATASOURCE field.")
			# arcpy.AddField_management(lyr, "DATASOURCE", "TEXT", "50", "", "", "DATASOURCE", "NULLABLE", "NON_REQUIRED", "")
			# arcpy.CalculateField_management(lyr, "DATASOURCE", "\"" + ds + "\"", "PYTHON", "")
		# else:
			# msg(lt + " DATASOURCE field existed? TRUE\n    Updating " + lt + " DATASOURCE field.")
			# arcpy.CalculateField_management(lyr, "DATASOURCE", "\"" + ds + "\"", "PYTHON", "")
		
		# # Prep MAILADD
		# if lt == "Address Point" and ds <> "Craig":
			# if not FieldExists(fds, "MAIL_ADD"):
				# msg(lt + " MAIL_ADD field existed? FALSE\n    Creating " + lt + " MAIL_ADD field.")
				# arcpy.AddField_management(lyr, "MAIL_ADD", "TEXT", "50", "", "", "MAIL_ADD", "NULLABLE", "NON_REQUIRED", "")
				# arcpy.CalculateField_management(lyr, "MAIL_ADD", "(!MAIL_ADD1! + \" \" + !MAIL_ADD2!).strip()", "PYTHON", "")
			# else:
				# msg(lt + " MAIL_ADD field existed? TRUE\n    Updating " + lt + " MAIL_ADD field.")
				# arcpy.CalculateField_management(lyr, "MAIL_ADD", "(!MAIL_ADD1! + \" \" + !MAIL_ADD2!).strip()", "PYTHON", "")
		
	# except Exception as e:
		# msg("\nThere was an error preparing the incoming/source data.")
		# msg("\n  Error message:\n  " + str(e))

		
	# # 02: Exporting input attributes to a list object
	# # --------------------------------------------------------------------------------------------------------------
	# msg("\nStep 02: Exporting attributes to an array.\n------------------------------------------------------------------------------")

	# try:
	
		# msg("Creating array of attributes from " + nL + ".")
		# fds = arcpy.ListFields(lyr)
		# butesList = {}
		# r = []
		# for f in fds:
			# if not f.required:
				# r.append(f.name.upper())
		# butesList[0] = r
		# #msg(butesList[0])
		# del r
		# cur = arcpy.da.SearchCursor(lyr, "*")
		# i = 0
		# for row in cur:
			# i = i + 1
			# r = []
			# for f in fds:
				# if not f.required:
					# v = row.getValue(f.name)
					# r.append(v)
			# butesList[i] = r
			# #msg(butesList[i])
			# del r
			
	# except Exception as e:
		# msg("\nThere was an error dumping the incoming/source attributes to a list.")
		# msg("\n  Error message:\n  " + str(e))

	# # 03: Exporting input feature classes to shapefile
	# # --------------------------------------------------------------------------------------------------------------
	# msg("\nStep 03: Exporting " + lt + " to shapefile.\n------------------------------------------------------------------------------")

	# try:
	
		# # exporting to shapefile
		# msg("Exporting " + nL + " layer to shapefile.")
		# arcpy.FeatureClassToFeatureClass_conversion (lyr, out, shpnam + ".shp")

		# # adding the new shapefiles to the map
		# msg("Adding new shapefile to map.")
		# mxd = arcpy.mapping.MapDocument("CURRENT")
		# df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
		# newlayerS = arcpy.mapping.Layer(outshape)
		# arcpy.mapping.AddLayer(df, newlayerS, "BOTTOM")
		# arcpy.RefreshActiveView()
		# arcpy.RefreshTOC()
		# del mxd, df
		
	# except Exception as e:
		# msg("\nThere was an error exporting the incoming/source data to a shapefile.")
		# msg("\n  Error message:\n  " + str(e))

	# # 04: Delete all fields from shapefile except for JOINID, DATASOURCE, Shape and FID
	# # --------------------------------------------------------------------------------------------------------------
	# msg("\nStep 04: Deleting all fields from " + shpnam + ".shp except for JOINID and DATASOURCE.\n------------------------------------------------------------------------------")
	
	# try:
	
		# msg("Deleting fields from " + shpnam + ".shp.")
		# sfds = arcpy.ListFields(outshape)
		# dropfields = []
		# for fd in sfds:
			# if IsDeletableField(fd):
				# dropfields.append(fd.name)
		# arcpy.DeleteField_management(outshape, dropfields)
		
	# except Exception as e:
		# msg("\nThere was an error deleting fields from the new output shapefile.")
		# msg("  Error message:\n  " + str(e))


	# # 05: Add go2it fields to shapefile
	# # --------------------------------------------------------------------------------------------------------------
	# msg("\nStep 05: Adding Go2It fields.\n------------------------------------------------------------------------------")
	
	# try:

		# msg("Adding Go2It fields to " + shpnam+ ".shp.")
		# fieldmapList = []
		# fieldmapList = GetTheSchema(ds, lt)
		# for i in fieldmapList:
			# if i[1] == "DATE":
				# arcpy.AddField_management(outshape, i[0], "DATE", "", "", "", "\"" + i[0] + "\"", "NULLABLE", "NON_REQUIRED", "")
			# elif i[1] == "TEXT":
				# arcpy.AddField_management(outshape, i[0], "TEXT", "", "", i[2], "\"" + i[0] + "\"", "NULLABLE", "NON_REQUIRED", "")
			# elif i[1] == "SHORT":
				# arcpy.AddField_management(outshape, i[0], "SHORT", i[3], i[4], "", "\"" + i[0] + "\"", "NULLABLE", "NON_REQUIRED", "")
			# elif i[1] == "LONG":
				# arcpy.AddField_management(outshape, i[0], "LONG", i[3], i[4], "", "\"" + i[0] + "\"", "NULLABLE", "NON_REQUIRED", "")
			# elif i[1] == "DOUBLE":
				# arcpy.AddField_management(outshape, i[0], "DOUBLE", i[3], i[4], "", "\"" + i[0] + "\"", "NULLABLE", "NON_REQUIRED", "")

	# except Exception as e:
		# msg("\nThere was an error adding the Go2It fields to the new shapefile.")
		# msg("  Error message:\n  " + str(e))
			
	
	# # 06: Populate attribute data from lists
	# # --------------------------------------------------------------------------------------------------------------
	# msg("\nStep 06: Populating attribute data.\n------------------------------------------------------------------------------")
	
	# if lt == "Street Centerline":
	
		# try:

			# # Populate Centerline attributes
			# # *************************************************************************************
			# msg("Populating Centerline attributes to " + shpnam + ".shp.")
			# cur = arcpy.UpdateCursor(newlayerS)
			# i=0
			# for row in cur:
				# i = i + 1
				# pre = GetFieldValue(fieldmapList, butesList, i, "PREFIX")
				# nam = GetFieldValue(fieldmapList, butesList, i, "NAME")
				# suf = GetFieldValue(fieldmapList, butesList, i, "SUFFIX")
				# pdr = GetFieldValue(fieldmapList, butesList, i, "POSTDIR")
				# fnam = GetFieldValue(fieldmapList, butesList, i, "RDNAME")
				# if len(fnam) > 51:
					# msg("   Row " + str(i) + " of RDNAME: value is too big and will be truncated")
					# fnam = fnam[:51]
				# classi = GetFieldValue(fieldmapList, butesList, i, "CLASSIFI")
				# alias1 = GetFieldValue(fieldmapList, butesList, i, "ALIAS")
				# if len(alias1) > 51:
					# msg("   Row " + str(i) + " of ALIAS: value is too big and will be truncated")
					# alias1 = alias1[:51]
				# alias2 = GetFieldValue(fieldmapList, butesList, i, "ALIAS2")
				# if len(alias2) > 51:
					# msg("   Row " + str(i) + " of ALIAS2: value is too big and will be truncated")
					# alias2 = alias2[:51]
				# lf = GetFieldValue(fieldmapList, butesList, i, "LEFT_FROM")
				# lto = GetFieldValue(fieldmapList, butesList, i, "LEFT_TO")
				# rf = GetFieldValue(fieldmapList, butesList, i, "RIGHT_FROM")
				# rt = GetFieldValue(fieldmapList, butesList, i, "RIGHT_TO")
				# ecom = GetFieldValue(fieldmapList, butesList, i, "MSAG_COM_E")
				# ocom = GetFieldValue(fieldmapList, butesList, i, "MSAG_COM_O")
				# zecom = GetFieldValue(fieldmapList, butesList, i, "ZIP_COM_E")
				# zocom = GetFieldValue(fieldmapList, butesList, i, "ZIP_COM_O")
				# lanes = GetFieldValue(fieldmapList, butesList, i, "LANES")
				# speed = GetFieldValue(fieldmapList, butesList, i, "SPEED")
				# width = GetFieldValue(fieldmapList, butesList, i, "WIDTH")
				# surf = GetFieldValue(fieldmapList, butesList, i, "SURFACE")
				# should = GetFieldValue(fieldmapList, butesList, i, "SHOULDER")
				# oneway = GetFieldValue(fieldmapList, butesList, i, "ONEWAY")
				# note1 = GetFieldValue(fieldmapList, butesList, i, "NOTE1")
				# if len(note1) > 150:
					# msg("   Row " + str(i) + " of NOTE1: value is too big and will be truncated")
					# note1 = note1[:150]
				# note2 = GetFieldValue(fieldmapList, butesList, i, "NOTE2")
				# if len(note2) > 150:
					# msg("   Row " + str(i) + " of NOTE2: value is too big and will be truncated")
					# note2 = note2[:150]
				
				# row.setValue("PREFIX", pre)
				# row.setValue("NAME", nam)
				# row.setValue("SUFFIX", suf)
				# row.setValue("POSTDIR", pdr)
				# row.setValue("RDNAME", fnam)
				# row.setValue("CLASSIFI", classi)
				# row.setValue("ALIAS", alias1)
				# row.setValue("ALIAS2", alias2)
				# row.setValue("LEFT_FROM", lf)
				# row.setValue("LEFT_TO", lto)
				# row.setValue("RIGHT_FROM", rf)
				# row.setValue("RIGHT_TO", rt)
				# row.setValue("MSAG_COM_E", ecom)
				# row.setValue("MSAG_COM_O", ocom)
				# row.setValue("ZIP_COM_E", zecom)
				# row.setValue("ZIP_COM_O", zocom)
				# row.setValue("LANES", lanes)
				# row.setValue("SPEED", speed)
				# row.setValue("WIDTH", width)
				# row.setValue("SURFACE", surf)
				# row.setValue("SHOULDER", should)
				# row.setValue("ONEWAY", oneway)
				# row.setValue("NOTE1", note1)
				# row.setValue("NOTE2", note2)

				# cur.updateRow(row)
				
			# del row, cur
		
		# except Exception as e:
			# msg("\n  There was an error writing attributes to the output centerline shapefile.")
			# msg("    Error message:\n" + str(e))

	# else:
	
		# try:

			# # Populate Address attributes
			# # *************************************************************************************
			# msg("Populating Address attributes to " + shpnam + ".shp.")
			# cur = arcpy.UpdateCursor(newlayerS)
			# i=0
			# for row in cur:
				# i = i + 1
				# housenum = GetFieldValue(fieldmapList, butesList, i, "NEW_ADD")
				# unitdesig = GetFieldValue(fieldmapList, butesList, i, "ALPHA")
				# pre = GetFieldValue(fieldmapList, butesList, i, "PREFIX")
				# nam = GetFieldValue(fieldmapList, butesList, i, "ROAD_NAME")
				# suf = GetFieldValue(fieldmapList, butesList, i, "SUFFIX")
				# pdr = GetFieldValue(fieldmapList, butesList, i, "POSTDIR")
				# fnam = GetFieldValue(fieldmapList, butesList, i, "RDNAME")
				# if len(fnam) > 51:
					# msg("   Row " + str(i) + " of RDNAME: value is too big and will be truncated")
					# fnam = fnam[:51]
				# fulladd = GetFieldValue(fieldmapList, butesList, i, "FULL_ADDR")
				# alias1 = GetFieldValue(fieldmapList, butesList, i, "ALIAS")
				# if len(alias1) > 51:
					# msg("   Row " + str(i) + " of ALIAS: value is too big and will be truncated")
					# alias1 = alias1[:51]
				# alias2 = GetFieldValue(fieldmapList, butesList, i, "ALIAS2")
				# if len(alias2) > 51:
					# msg("   Row " + str(i) + " of ALIAS2: value is too big and will be truncated")
					# alias2 = alias2[:51]
				# namelast = GetFieldValue(fieldmapList, butesList, i, "LAST_NAME")
				# namefirst = GetFieldValue(fieldmapList, butesList, i, "FIRST_NAME")
				# namelast2 = GetFieldValue(fieldmapList, butesList, i, "LNAME2")
				# namefirst2 = GetFieldValue(fieldmapList, butesList, i, "FNAME2")
				# phone1 = GetFieldValue(fieldmapList, butesList, i, "PHONE")
				# phone2 = GetFieldValue(fieldmapList, butesList, i, "PHONE2")
				# cphon1 = GetFieldValue(fieldmapList, butesList, i, "CPHONE1")
				# cphon2 = GetFieldValue(fieldmapList, butesList, i, "CPHONE2")
				# mail1 = GetFieldValue(fieldmapList, butesList, i, "MAIL_ADD")
				# mail2 = GetFieldValue(fieldmapList, butesList, i, "MAIL_CITY")
				# mail3 = GetFieldValue(fieldmapList, butesList, i, "MAIL_STATE")
				# strucomp = GetFieldValue(fieldmapList, butesList, i, "STRUC_COMP")
				# if len(strucomp) > 20:
					# msg("   Row " + str(i) + " of STRUC_COMP: value is too big and will be truncated")
					# strucomp = strucomp[:20]
				# strutype = GetFieldValue(fieldmapList, butesList, i, "STRUC_TYPE")
				# if len(strutype) > 20:
					# msg("   Row " + str(i) + " of STRUC_TYPE: value is too big and will be truncated")
					# strutype = strutype[:20]
				# note1 = GetFieldValue(fieldmapList, butesList, i, "NOTE1")
				# if len(note1) > 150:
					# msg("   Row " + str(i) + " of NOTE1: value is too big and will be truncated")
					# note1 = note1[:150]
				# note2 = GetFieldValue(fieldmapList, butesList, i, "NOTE2")
				# if len(note2) > 150:
					# msg("   Row " + str(i) + " of NOTE2: value is too big and will be truncated")
					# note2 = note2[:150]
				# hlink = GetFieldValue(fieldmapList, butesList, i, "HOTLINK")
				# if len(hlink) > 100:
					# msg("   Row " + str(i) + " of HOTLINK: value is too big and will be truncated")
					# hlink = hlink[:100]
				# longi = GetFieldValue(fieldmapList, butesList, i, "LONGITUDE")
				# lati = GetFieldValue(fieldmapList, butesList, i, "LATITUDE")
				
				
				# row.setValue("NEW_ADD", housenum)
				# row.setValue("ALPHA", unitdesig)
				# row.setValue("PREFIX", pre)
				# row.setValue("ROAD_NAME", nam)
				# row.setValue("SUFFIX", suf)
				# row.setValue("POSTDIR", pdr)
				# row.setValue("RDNAME", fnam)
				# row.setValue("FULL_ADDR", fulladd)
				# row.setValue("ALIAS", alias1)
				# row.setValue("ALIAS2", alias2)
				# row.setValue("LAST_NAME", namelast)
				# row.setValue("FIRST_NAME", namefirst)
				# row.setValue("LNAME2", namelast2)
				# row.setValue("FNAME2", namefirst2)
				# row.setValue("PHONE", phone1)
				# row.setValue("PHONE2", phone2)
				# row.setValue("CPHONE1", cphon1)
				# row.setValue("CPHONE2", cphon2)
				# row.setValue("MAIL_ADD", mail1)
				# row.setValue("MAIL_CITY", mail2)
				# row.setValue("MAIL_STATE", mail3)
				# row.setValue("STRUC_COMP", strucomp)
				# row.setValue("STRUC_TYPE", strutype)
				# row.setValue("NOTE1", note1)
				# row.setValue("NOTE2", note2)
				# row.setValue("HOTLINK", hlink)
				# row.setValue("LONGITUDE", longi)
				# row.setValue("LATITUDE", lati)
				
				# cur.updateRow(row)
				
			# del row, cur

		# except Exception as e:
			# msg("\n  There was an error writing attributes to the output address point shapefile.")
			# msg("    Error message:\n" + str(e))

	# # 07: Reformat Numeric Road Names
	# # --------------------------------------------------------------------------------------------------------------
	# msg("\nStep 07: Running the Road Name Formatter.\n------------------------------------------------------------------------------")

	# if bol:

		# # Process the street centerline layer
		# # ==============================================================================================================
		# fdsr = arcpy.ListFields(newlayerS)
		# pre = "PREFIX"
		# nam = "NAME"
		# nam2 = "ROAD_NAME"
		# suf = "SUFFIX"
		# pdr = "POSTDIR"
		# fnam = "RDNAME"
		# fadd = "FULL_ADDR"
		
		# # Add Temp Name field and calculate a default value of zero.
		# # --------------------------------------------------------------------------------------------------------------
		# try:
			
			# msg("  Setting up Temp Name field.")
			# if not FieldExists(fdsr, "TEMP_NAME"):
				# arcpy.AddField_management(newlayerS, "TEMP_NAME", "LONG", "9", "", "", "", "NULLABLE", "NON_REQUIRED", "")
				# arcpy.CalculateField_management(newlayerS, "TEMP_NAME", "0", "VB", "")
			# else:
				# arcpy.CalculateField_management(newlayerS, "TEMP_NAME", "0", "VB", "")
				
		# except Exception as e:
			# msg("\n  There was an error in setting up the Temp Name field.")
			# msg("    Error message:\n" + str(e))
			
			
		# # Trimming Pre Directional and Street Name fields
		# # --------------------------------------------------------------------------------------------------------------
		# try:
			# msg("  Trimming street name fields.")
			# cur = arcpy.UpdateCursor(newlayerS)
			# for row in cur:
				# row.setValue("PREFIX", row.getValue("PREFIX").strip())
				# if lt == "Street Centerline":
					# row.setValue("NAME", row.getValue("NAME").strip())
				# else:
					# row.setValue("ROAD_NAME", row.getValue("ROAD_NAME").strip())
				# row.setValue("SUFFIX", row.getValue("SUFFIX").strip())
				# row.setValue("POSTDIR", row.getValue("POSTDIR").strip())
				# cur.updateRow(row)
			
			# # free up memory and file lock
			# row, cur = None, None

		# except Exception as e:
			# row, cur = None, None
			# msg("\n  There was an error in trimming the street name fields.")
			# msg("    Error message:\n" + str(e))
			
		# # Get Cursor of all records and loop through all records and check street name field values
		# # for numeric or not. If numeric, write value to temp name field
		# # --------------------------------------------------------------------------------------------------------------
		# try:
			# msg("  Identifying numeric values in Street Name field and writing to Temp Name field.")
			# cur = arcpy.UpdateCursor(newlayerS)
			# for row in cur:
				# if lt == "Street Centerline":
					# val = row.getValue("NAME")
				# else:
					# val = row.getValue("ROAD_NAME")
				# if val.isdigit():
					# #write val to TEMP_NAME field
					# row.TEMP_NAME = val
					# cur.updateRow(row)
			
			# # free up memory and file lock
			# row, cur = None, None
			
		# except Exception as e:
			# row, cur = None, None
			# msg("\nThere was an error writing numeric values to the Temp Name field.")
			# msg("\nError message:\n" + str(e))

		# # Select non-zero values from Temp Name field and calc new Street Name values
		# # --------------------------------------------------------------------------------------------------------------
		# try:
			# msg("  Calculating new Street Name values on selected features.")
			# arcpy.SelectLayerByAttribute_management(newlayerS, "NEW_SELECTION", "\"TEMP_NAME\" <> 0")
			# if lt == "Street Centerline":
				# arcpy.CalculateField_management(newlayerS, "NAME", "!PREFIX! + !NAME!", "PYTHON", "")
			# else:
				# arcpy.CalculateField_management(newlayerS, "ROAD_NAME", "!PREFIX! + !ROAD_NAME!", "PYTHON", "")

		# except Exception as e:
			# msg("\nThere was an error calculating the new street name values.")
			# msg("\nError message:\n" + str(e))
			
		# # Clear out Pre Directional values from the Pre Directional field on selected features
		# # --------------------------------------------------------------------------------------------------------------
		# try:
			# msg("  Clearing Pre Directional values on selected features.")
			# arcpy.CalculateField_management(newlayerS, "PREFIX", "\"\"", "PYTHON", "")

		# except Exception as e:
			# msg("\nThere was an error clearing the selected pre directional field.")
			# msg("\nError message:\n" + str(e))
	
		# # Delete the Temp Name field
		# # --------------------------------------------------------------------------------------------------------------
		# try:
			# msg("  Deleting Temp Name field.\n")
			# arcpy.DeleteField_management(newlayerS, "TEMP_NAME")
			
		# except Exception as e:
			# row, cur = None, None
			# msg("\nThere was an error deleting the Temp Name field.")
			# msg("\nError message:\n" + str(e))
			
		# # Clear any selection in the centerline data
		# # --------------------------------------------------------------------------------------------------------------
		# arcpy.SelectLayerByAttribute_management(newlayerS, "CLEAR_SELECTION", "")		
			
	# else:
		# msg("User opted out of reformatting the road names.")
	
	
	# # 08: Recalculate RDNAME values and FULL_ADDR values
	# # --------------------------------------------------------------------------------------------------------------
	# msg("\nStep 08: Recalculate RDNAME values and FULL_ADDR values.\n------------------------------------------------------------------------------")
	
	# try:
		# exp1 = "(((!PREFIX! + \" \" + !NAME!).strip() + \" \" + !SUFFIX!).strip() + \" \" + !POSTDIR!).strip()"
		# exp2 = "(((!PREFIX! + \" \" + !ROAD_NAME!).strip() + \" \" + !SUFFIX!).strip() + \" \" + !POSTDIR!).strip()"
		# exp3 = "str(!NEW_ADD!) + \" \" + !RDNAME!"
		
		# if lt == "Street Centerline":
			# msg("  Recalculating centerlines RDNAME values.")
			# arcpy.CalculateField_management(newlayerS, "RDNAME", exp1, "PYTHON", "")
		# else:
			# msg("  Recalculating address point RDNAME values.")
			# arcpy.CalculateField_management(newlayerS, "RDNAME", exp2, "PYTHON", "")
			# msg("  Recalculating address point FULL_ADDR values.")
			# arcpy.CalculateField_management(newlayerS, "FULL_ADDR", exp3, "PYTHON", "")
	
	# except Exception as e:
		# msg("\nThere was an error recalculating the RDNAME or FULL_ADDR field.")
		# msg("  Error message:\n    " + str(e))
	
	# # 09: Recalculate Longitude and Latitude
	# # --------------------------------------------------------------------------------------------------------------
	
	# try:
	
		# if lt == "Address Point":
			# descshp = arcpy.Describe(newlayerS)
			# #spr = "GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],AUTHORITY["EPSG",4326]]"
			# spr = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"
			# shpfld = descshp.ShapeFieldName
			# msg("\nStep 09: Recalculating Longitude and Latitude.\n------------------------------------------------------------------------------")	
			# msg("Calculating Longitude and Latitude.")
			# cur = arcpy.UpdateCursor(newlayerS, "", spr)
			# for row in cur:
				# feat = row.getValue(shpfld)
				# geom = feat.getPart(0)
				# X = geom.X
				# Y = geom.Y
				# row.LONGITUDE = X
				# row.LATITUDE = Y
				# cur.updateRow(row)
			# row, cur = None, None


	# except Exception as e:
		# msg("\nThere was an error calculating the longitude and latitude.")
		# msg("  Error message:\n    " + str(e))
	
	

arcpy.AddMessage("\n\nDone!\n\n")



	




