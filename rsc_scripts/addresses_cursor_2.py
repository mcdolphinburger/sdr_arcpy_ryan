import arcpy

arcpy.env.overwriteOutput = True

points = r'C:\Data\Dunklin County, MO\shapes\dunklin_adds.shp'
esns = r'C:\Data\Dunklin County, MO\shapes\dunklin_esn.shp'
outpath = r'C:\Data\Dunklin County, MO\shapes'

arcpy.MakeFeatureLayer_management(points, 'adds_shape')

with arcpy.da.SearchCursor(esns, ['FID', 'RESP_EMS']) as esn_cursor:
    for x in esn_cursor:
        print x[1]
        arcpy.MakeFeatureLayer_management(esns, 'esns_shape', """ "FID" = {} """.format(x[0]))
        arcpy.SelectLayerByLocation_management('adds_shape', 'WITHIN', 'esns_shape')
        arcpy.FeatureClassToFeatureClass_conversion('adds_shape', outpath, 'adds_in_{}_{}'.format(x[1], x[0]))


