import arcpy

arcpy.env.overwriteOutput = True

points = r'C:\Data\Dunklin County, MO\shapes\dunklin_adds.shp'
esns = r'C:\Data\Dunklin County, MO\shapes\dunklin_esn.shp'
outpath = r'C:\Data\Dunklin County, MO\shapes'

esn_selection = ['861', '866', '871', '876', '879']

arcpy.MakeFeatureLayer_management(points, 'adds_shape')

for x in esn_selection:
    print x
    arcpy.MakeFeatureLayer_management(esns, 'esn_shape', """ "ESN" = '{}' """.format(x)) 
    arcpy.SelectLayerByLocation_management('adds_shape', 'WITHIN', 'esn_shape')
    arcpy.FeatureClassToFeatureClass_conversion('adds_shape', outpath, 'dunklin_adds_{}'.format(x))

