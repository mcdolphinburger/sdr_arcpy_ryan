
# import arcpy

# ==============================================================================================================
# 							           F   U   N   C   T   I   O   N   S
# ==============================================================================================================

#  Receives: Feature Class or Feature Layer
#            Tuple of field pairs for the field map
#   Returns: An ESRI Field Mappings object
## ------------------------------------------------------------------------------
def GetFieldMappings(fc_in, fps):
	field_mappings = arcpy.FieldMappings()
	#field_mappings.addTable(fc_in)
	for p in fps:
		field_map = arcpy.FieldMap()					# initialize new fieldmap object
		field_map.addInputField(fc_in, p[5]) 			# get the input (source) field for the new fieldmap object       
		field = field_map.outputField        			# create a field object for the corresponding ouput (target) field
		field.name = p[0]								# set the output field's name
		field_map.outputField = field					# set the fieldmap's outputField
		field_mappings.addFieldMap(field_map)			# add the new fieldmap object to the fieldmappings object
		del field, field_map							# clean up objects created in this pass through the loop so they can be used again
	return field_mappings
	
	

def GetMIN(n1, n2, n3, n4):
	k = 1000000
	if n1 < k:
		k = n1
	if n2 < k:
		k = n2
	if n3 < k:
		k = n3
	if n4 < k:
		k = n4
	return k
	
def GetMAX(n1, n2, n3, n4):
	k = -1000000
	if n1 > k:
		k = n1
	if n2 > k:
		k = n2
	if n3 > k:
		k = n3
	if n4 > k:
		k = n4
	return k
	

	 
	 
# Tests a layer to see if it has a selection. Returns TRUE if there is an existing selection, and
# returns FALSE if there is no selection.
# -------------------------------------------------------------------------------------------------
def SelectionExists(lyr):
	d = arcpy.Describe(lyr)
	if not d.FIDSet  == '':
		return True
	else:
		return False
		
	# selectionCount = len(gp.describe(lyr).fidset.split(";"))






# Extracts and returns a number from the left side of the passed string. If there is no number on
# the left side of the passed string, it returns -1.
# -------------------------------------------------------------------------------------------------
def ExtractNumFromLeft(strval):
	num = ""
	for i in strval:
		if i.isdigit():
			num = num + i
		else:
			break
	if num == "":
		num = int("-1")
	else:
		num = int(num)
	return num



# map layer name or feature class, name, type, precision, scale, length, alias)
def CreateMyField(lyr, n, t, p, s, l, a):
	arcpy.AddField_management(lyr, n, t, p, s, l, a, "NULLABLE", "NON_REQUIRED", "")

def CreateMyField2(lyr, x):
	msg("    " + x[0])
	arcpy.AddField_management(lyr, x[0], x[1], x[3], x[4], x[2], x[5], "NULLABLE", "NON_REQUIRED", "")

def GetSelectionCount(lyr):
	return int(arcpy.GetCount_management(lyr).getOutput(0))

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
	
def FieldExists(fields, fname):
	doesexist = False
	for fld in fields:
		if fld.Name == fname:
			doesexist = True
	return doesexist
	
def FieldExists(lyr, fname):
	doesexist = False
	for fld in arcpy.ListFields(lyr):
		if fld.name == fname:
			doesexist = True
	return doesexist

def CreateTextField(lyr, fname, len):
	arcpy.AddField_management(lyr, fname, "TEXT", "", "", len, fname, "NULLABLE", "NON_REQUIRED", "")
	
def CreateLongField(lyr, fname):
	arcpy.AddField_management(lyr, fname, "LONG", "", "", "", fname, "NULLABLE", "NON_REQUIRED", "")
	
def CreateShortField(lyr, fname):
	arcpy.AddField_management(lyr, fname, "SHORT", "", "", "", fname, "NULLABLE", "NON_REQUIRED", "")
	
def CreateDoubleField(lyr, fname):
	arcpy.AddField_management(lyr, fname, "DOUBLE", "", "", "", fname, "NULLABLE", "NON_REQUIRED", "")
	
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
	
	
#	Receives: describe object
#	 Returns: string indicating the kind of workspace of the input layer
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
	
	

#	Receives: featureclass object, field maps object
#	 Returns: Field Mappings object
#	---------------------------------------------------------------------------------
def GetFieldMappings(fc_in, fmaps):
    field_mappings = arcpy.FieldMappings()
    field_mappings.addTable(fc_in)
    for input, output in fmaps.iteritems():
        field_map = arcpy.FieldMap()
        field_map.addInputField(fc_in, input)        
        field = field_map.outputField        
        field.name = output
        field_map.outputField = field
        field_mappings.addFieldMap(field_map)
        del field, field_map

    return field_mappings
	
def GetOIDFieldName(lyr):
	return arcpy.Describe(lyr).OIDFieldName
	

	
	
	
	
	
	
	
	
	
	
	