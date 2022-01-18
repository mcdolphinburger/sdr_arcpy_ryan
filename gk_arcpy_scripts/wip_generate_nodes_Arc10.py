# Create and classify nodes for line featureclass
# For DangleNodes can be generated under/over shoots
#
# Original script by Marek Draskovic (2005)
# Modified for Arc10 by Glenn Kammerer (2011)
#
# ===========================================================================================
# ===========================================================================================


def go_tlac(show_msg): # - printing message
    arcpy.AddMessage(show_msg) ; print show_msg

def go_error(chyba): # - error
    arcpy.AddMessage(chyba) ; print chyba
    sys.exit()

def find_char(shp, ch):
  index = 0 ; loc = 0
  for index in range(0,len(shp)): 
    if shp[index] == ch: 
        loc = index
  return loc + 1

def search_att(fc, att):
    attok = 0
    check_fc = fc
    fields = gp.listfields(check_fc)
    fields.Reset()
    field = fields.next()
    while field <> None:
        if field.name == att:
            attok = 1
            break
        field = fields.next()
    return attok





# Import system modules
import arcpy, sys, string, os, math

# Create the Geoprocessor object
# gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

#Inputs
InLyr = arcpy.GetParameterAsText(0)
shpName = arcpy.GetParameterAsText(1)
shpPath = arcpy.GetParameterAsText(2)
dg_check = arcpy.GetParameterAsText(3)



# Verify Input Line Layer has a Spatial Reference. If so, use it for creating the output Node layer
descr1 = arcpy.Describe(InLyr)
InFC = descr1.FeatureClass
spref = InFC.SpatialReference


# Create the Ouput Shapefile or FeatureClass
# Arguments: Path, Name, Geo Type, unk, Has M vals, has Z vals, Coord Sys, unk, unk, unk, unk
arcpy.CreateFeatureclass_management(shpPath, shpName, "POINT", "", "DISABLED", "DISABLED", spref, "", "0", "0", "0")
arcpy.AddField_management(shpPath + "\\" + shpName + ".shp", "NODE_CT", "LONG", "", "", "", "NODE_CT", "NULLABLE", "NON_REQUIRED", "")
# arcpy.AddMessage(shpPath + "\\" + shpName + ".shp" + "\n")
















