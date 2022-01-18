import arcpy

points = arcpy.GetParameterAsText(0)

with arcpy.da.UpdateCursor(points, ['ASIAUSER']) as address_cursor:
    for x in address_cursor:
        print x[0]
        x[0] = 'obsolete'
        address_cursor.updateRow(x)
        arcpy.AddMessage('{} value updated.'.format(x[0]))