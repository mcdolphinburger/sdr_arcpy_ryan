import arcpy

points = r'C:\Data\Dunklin County, MO\shapes\dunklin_adds.shp'
esns = r'C:\Data\Dunklin County, MO\shapes\dunklin_esn.shp'
outpath = r'C:\Data\Dunklin County, MO\shapes'

arcpy.MakeFeatureLayer_management(points, 'adds_shape')
arcpy.MakeFeatureLayer_management(esns, 'esn_shape', """ "ESN" = '861' """)

arcpy.SelectLayerByLocation_management('adds_shape', 'WITHIN', 'esn_shape')
arcpy.FeatureClassToFeatureClass_conversion('adds_shape', outpath, 'dunklin_adds_campbell')
