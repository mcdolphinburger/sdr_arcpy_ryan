
# import arcpy

# ==============================================================================================================
# 							           P   A   R   A   M   E   T   E   R   S
# ==============================================================================================================




Get fields list as a list of text values only:
fds = [fd.name.upper() for fd in arcpy.ListFields(lyr)]





NAD 83 UTM Z15N
---------------------------------------------------------------------------------
PROJCS["NAD_1983_UTM_Zone_15N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-93.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0],AUTHORITY["EPSG",26915]]



try:

except Exception as e:
	row, cur = None, None
	msg("\nThere was an error in the main loop.")
	msg("\nError message:\n\n" + str(e))

def get_field_mappings(fc_in, mapping_list):
    """
    Creates fieldmappings object
    fc_in (string) - Input feature class
    mapping_list (list) - List of tuples of input fields and output fields
    """
    import arcpy

    field_dict = dict((f.name, (f.type)) for f in  arcpy.ListFields(fc_in))
    for field, type_ in field_dict.iteritems():
        if type_ == 'OID':
            field_dict[field] = 'DOUBLE'

    field_mappings = arcpy.FieldMappings()
    for in_field, out_field in mapping_list:
        field_map = arcpy.FieldMap()
        field_map.addInputField(fc_in, in_field)
        field = field_map.outputField
        field.name = out_field
        field.type = field_dict[in_field]
        field_map.outputField = field
        field_mappings.addFieldMap(field_map)

    del field, field_map

    return field_mappings

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



LR = []
LR = [
	["GIS_SOURCE","GIS_SOURCE","TEXT","50"],
	["STSEG_ID","Road Seg Identifier","LONG",""],
	["FROM_ADD_L","Left Address From","LONG",""],
	["TO_ADD_L","Left Address To","LONG",""],
	["FROM_ADD_R","Right Address From","LONG",""],
	["TO_ADD_R","Right Address To","LONG",""],
	["PRE_DIR","Prefix Directional","TEXT","2"],
	["PRE_TYPE","Pre Type","TEXT","15"],
	["ST_NAME","Street Name","TEXT","60"],
	["ST_TYPE","Street Suffix","TEXT","4"],
	["SUF_DIR","Suffix Direction","TEXT","2"],
	["FULL_NAME","Full Street Name","TEXT","70"],
	["ALT_NAME","Alternate Street Name","TEXT","70"],
	["ONEWAY","One way","TEXT","1"],
	["MSAG_COM_L","MSAG Community Name Left","TEXT","35"],
	["MSAG_COM_R","MSAG Community Name Right","TEXT","35"],
	["ESN_L","Emergency Service Zone  Left","TEXT","6"],
	["ESN_R","Emergency Service Zone  Right","TEXT","6"],
	["CITY_L","City Left","TEXT","35"],
	["CITY_R","City Right","TEXT","35"],
	["ZIP5_L","Zip5 Left","TEXT","5"],
	["ZIP5_R","Zip5 Right","TEXT","5"],
	["ADD_ORIG","Address Origin","TEXT","35"],
	["UPD_BY","Source of Update","TEXT","20"],
	["UPD_DATE","Date Updated","DATE",""]
  ]

# arcpy field type constants: TEXT, FLOAT, DOUBLE, SHORT, LONG, DATE, BLOB, RASTER, GUID
# --------------------------------------------------------------------------------------------------------------------------------
# TEXT —Names or other textual qualities.
# FLOAT —Numeric values with fractional values within a specific range.
# DOUBLE —Numeric values with fractional values within a specific range.
# SHORT —Numeric values without fractional values within a specific range; coded values.
# LONG —Numeric values without fractional values within a specific range.
# DATE —Date and/or Time.
# BLOB —Images or other multimedia.
# RASTER —Raster images.
# GUID —GUID values

# Changing the case of strings
# --------------------------------------------------------------------------------------------------------------------------------
# if fld.name == fname or fld.name == fname.lower() or fld.name == fname.title():

# Parsing strings
# --------------------------------------------------------------------------------------------------------------------------------
# Get the first N characters in a string: val[:N], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value

# Join Field parameters
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.JoinField_management(in_data, in_field, join_table, join_field, {fields})


# Make Feature Layer
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.MakeFeatureLayer_management (in_features, out_layer, {where_clause}, {workspace}, {field_info})


# Add attribute join
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.AddJoin_management (in_layer_or_view, in_field, join_table, join_field, {join_type})


# Feature Class to Geodatabase
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.FeatureClassToGeodatabase_conversion (Input_Features, Output_Geodatabase)


# Copy features
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.CopyFeatures_management (in_features, out_feature_class, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})


# Copy datasets
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.Copy_management (in_data, out_data, {data_type})


# Rename datasets
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.Rename_management (in_data, out_data, {data_type})


# Compact Geodatabases
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.Compact_management (in_workspace)


# Create a Feature Dataset
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.CreateFeatureDataset_management(out_dataset_path, out_name, {spatial_reference})



# Create Personal Geodatabase
# --------------------------------------------------------------------------------------------------------------------------------
# CreatePersonalGDB_management (out_folder_path, out_name, {out_version})
# arcpy.CreatePersonalGDB_management(out_folder_path, out_name, {out_version})


# Create File Geodatabase
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.CreateFileGDB_management (out_folder_path, out_name, {out_version})


# Delete Data
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.Delete_management (in_data, {data_type})


# Delete Field
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.DeleteField_management (in_table, drop_field)


# Append Features parameters
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.Append_management (inputs, target, {schema_type}, {field_mapping}, {subtype})


# Copy Features parameters
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.CopyFeatures_management (in_features, out_feature_class, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})


# FeatureClass to FeatureClass parameters
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.FeatureClassToFeatureClass_conversion (in_features, out_path, out_name, {where_clause}, {field_mapping}, {config_keyword})


# Create FeatureClass parameters
# --------------------------------------------------------------------------------------------------------------------------------
# Arguments: Path, Name, Geo Type, Template Feat Class, Has M vals, has Z vals, Coord Sys, Config Keyword, 
#                      Output Sp Grid1, Output Sp Grid2, Output Sp Grid3
# arcpy.CreateFeatureclass_management(shpPath, shpName, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")


# Add Field parameters
# --------------------------------------------------------------------------------------------------------------------------------
# Arguments: input table, field name, field type, precision, scale, length, field alias, is nullable, is required, domain
# arcpy.AddField_management(FL1, "RACT", "TEXT", "", "", "32", "RACT", "NULLABLE", "NON_REQUIRED", "")
# arcpy.AddField_management(FL1, "LOW", "LONG", "", "", "", "LOW", "NULLABLE", "NON_REQUIRED", "")
# arcpy.AddField_management(FL1, "LOW", "SHORT", "", "", "", "LOW", "NULLABLE", "NON_REQUIRED", "")


# Calculate Field parameters
# --------------------------------------------------------------------------------------------------------------------------------
# Arguments: input table, field name, expression, expression type, code block
# arcpy.CalculateField_management(Input_Table, Field_Name, Expression, Expression_Type, Code_Block)
# arcpy.CalculateField_management(Addresses__2_, "E911_COMM", "\"xxxx\"", "VB", "")


# Select Layer By Attribute
# --------------------------------------------------------------------------------------------------------------------------------
# Arguments: Layer Name or Table View, Selection Type, Expression
# arcpy.SelectLayerByAttribute_management(Layer, "NEW_SELECTION", "[COMP_STR_NAME] = '10TH ST'")


# Select Layer By Location
# --------------------------------------------------------------------------------------------------------------------------------
# Arguments: Input Feature Layer, Relationship, Selecting features, Search Distance, Selection type
# arcpy.SelectLayerByLocation_management(Target Layer, "INTERSECT", Selecting Layer, "", "NEW_SELECTION")

# Get Feature Count
# --------------------------------------------------------------------------------------------------------------------------------
# sourcecount = int(arcpy.GetCount_management(fc1).getOutput(0))
# sourcecount = len(desc.fidset.split(";"))	  <--- where desc is a describe object

# Create Table Syntax
# --------------------------------------------------------------------------------------------------------------------------------
# arcpy.CreateTable_management (out_path, out_name, {template}, {config_keyword})

# Extract Element Function
# --------------------------------------------------------------------------------------------------------------------------------
# Returns the nth element of a text string, where the elements are separated by a specified separator character
def ExtractElement(txt, n, sep):
	txt1 = txt.strip()
	
	# add seperator to end of string
	if txt[-1:] != sep:
		txt1 = txt1 + sep
		
	# Initialize
	elcnt = 0
	tempel = ""
	
	# Extract
	for c in txt1:
		if c == sep:
			elcnt = elcnt + 1
			if elcnt == n:
				# got the element we need, so get out
				theelement = tempel
				return theelement
			else:
				tempel = ""
		else:
			tempel = tempel + c


# Public Function ExtractElement(txt, n, Separator) As String

# '  Txt = text string passed
# '  n = integer passed
# '  Separator = a single character used as a separator

# Returns the nth element of a text string, where the elements are separated by a specified separator character

    # Dim Txt1 As String, temperament As String
    # Dim ElementCount As Integer, i As Integer
    # Dim TempElement As String
    
    # Txt1 = txt
# '   If space separator, remove excess spaces
    # If Separator = Chr(32) Then Txt1 = Application.Trim(Txt1)
    
# '   Add a separator to the end of the string
    # If Right(Txt1, Len(Txt1)) <> Separator Then _
        # Txt1 = Txt1 & Separator
    
# '   Initialize
    # ElementCount = 0
    # TempElement = ""
    
# '   Extract each element
    # For i = 1 To Len(Txt1)
        # If Mid(Txt1, i, 1) = Separator Then
            # ElementCount = ElementCount + 1
            # If ElementCount = n Then
# '               Found it, so exit
                # ExtractElement = TempElement
                # Exit Function
            # Else
                # TempElement = ""
            # End If
        # Else
            # TempElement = TempElement & Mid(Txt1, i, 1)
        # End If
    # Next i
    
    # ExtractElement = ""
    
# End Function













