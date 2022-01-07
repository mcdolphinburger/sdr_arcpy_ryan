import arcpy

points = arcpy.GetParameterAsText(0)

field_list = arcpy.ListFields(points)
list_field = [] 

for x in field_list:

    print x.name
    print x.type
    if x.type == 'String':
        list_field.append(x.name)
    else:
        arcpy.AddMessage('Field is {} format'.format(x.type))
            
for field in list_field:

    with arcpy.da.UpdateCursor(points, [field]) as address_cursor:
        for x in address_cursor:
            arcpy.AddMessage(x[0])
            if x[0] == ' ':
                x[0] = 'jawn'
                address_cursor.updateRow(x)
                arcpy.AddMessage('{} value updated.'.format(x[0]))