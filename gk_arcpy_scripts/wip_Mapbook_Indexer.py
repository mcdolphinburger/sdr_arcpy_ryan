#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#																											#
#	Mapbook_Indexer.py																						#
#	Created on: 2012-01-24																					#
#																											#
#																											#
#	Description: 																							#
#	----------------																						#
#																											#
#																											#
#																											#
#																											#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import arcpy module
import arcpy


arcpy.AddMessage("\n" + "\n" + "Mapbook Indexer Tool")
arcpy.AddMessage("====================" + "\n" + "\n")



# Script arguments
# ==========================================================================================================
FL1 = arcpy.GetParameterAsText(0)						# Road Centerline feature layer
fieldRDNAME = arcpy.GetParameterAsText(1)				# Road Centerline compiled road name field
FL2 = arcpy.GetParameterAsText(2)						# Mapbook Grid feature layer
fieldPAGE = arcpy.GetParameterAsText(3)					# Mapbook Grid page value field
FL3 = arcpy.GetParameterAsText(4)						# Secondary Boundary feature layer (optional)



# Additional variable assignment
# ==========================================================================================================
desc1 = arcpy.Describe(FL1)
desc2 = arcpy.Describe(FL2)
fc1 = desc1.FeatureClass
fc2 = desc2.Featureclass
fields1 = fc1.Fields
fields2 = fc2.Fields

arcpy.AddMessage("\n" + "\n" + "here!" + "\n" + "\n")

if len(FL3) > 0:
 	desc3 = arcpy.Describe(FL3)
	fc3 = desc3.FeatureClass
	fields3 = fc3.Fields

	
arcpy.AddMessage("\n" + "\n" + "here!" + "\n" + "\n")	
	
	
scur = arcpy.SearchCursor(FL2)
for feat in scur:
	mapbookpage = feat.getValue("PageNumber")
	arcpy.AddMessage("Page: " + str(mapbookpage))
	arcpy.SelectLayerByAttribute_management(FL2, "NEW_SELECTION", "[PageNumber] = " + str(mapbookpage) + "")
	# Select roads intersecting current mapbook grid
	arcpy.SelectLayerByLocation_management(FL1, "INTERSECT", FL2, "", "NEW_SELECTION")
	




	
	
		
		
arcpy.AddMessage("\n" + "\n" + "\n")



