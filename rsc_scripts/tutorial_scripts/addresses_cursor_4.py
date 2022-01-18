import arcpy

arcpy.env.overwriteOutput = True

points = arcpy.GetParameterAsText(0)
esns = arcpy.GetParameterAsText(1)
outpath = arcpy.GetParameterAsText(2)
esn_area = arcpy.GetParameterAsText(3)
total_count = 0
created_count = 0

arcpy.MakeFeatureLayer_management(points, 'adds_shape')

with arcpy.da.SearchCursor(esns, ['FID', 'RESP_EMS', 'SHAPE_Area']) as esn_cursor:
    for x in esn_cursor:
    
        total_count += 1
        if x[2] >= float(esn_area):
        
            created_count += 1
            print x[1]
            arcpy.MakeFeatureLayer_management(esns, 'esns_shape', """ "FID" = {} """.format(x[0]))
            arcpy.SelectLayerByLocation_management('adds_shape', 'WITHIN', 'esns_shape')
            arcpy.FeatureClassToFeatureClass_conversion('adds_shape', outpath, 'adds_in_{}_{}'.format(x[1], x[0]))
            
        else:
            print '{} did not meet conversion criteria'.format(x[1])
            arcpy.AddMessage('{} did not meet conversion criteria'.format(x[1])) 
        
print 'Finished'
print '{0} of {1} met conversion criteria'.format(created_count, total_count)
arcpy.AddMessage('Finished')
arcpy.AddMessage('{0} of {1} met conversion criteria'.format(created_count, total_count)) 


