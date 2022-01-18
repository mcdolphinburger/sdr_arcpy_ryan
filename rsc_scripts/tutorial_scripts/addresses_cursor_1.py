import arcpy

arcpy.env.overwriteOutput = True

points = r'C:\Data\Dunklin County, MO\shapes\dunklin_adds.shp'
esns = r'C:\Data\Dunklin County, MO\shapes\dunklin_esn.shp'
outpath = r'C:\Data\Dunklin County, MO\shapes'

with arcpy.da.SearchCursor(points, ['COMP_STR_N', 'STRUCTURE_', 'E911_COMM']) as addresses_cursor:
    for x in addresses_cursor:
        print x[0]
        print x[1]
        print x[2] + '\n'
