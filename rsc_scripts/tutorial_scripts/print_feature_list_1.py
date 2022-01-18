import arcpy

arcpy.env.workspace = r'C:\Data\Muskogee County, OK\ok_psap_shps'

feature_list = arcpy.ListFeatureClasses()

print feature_list