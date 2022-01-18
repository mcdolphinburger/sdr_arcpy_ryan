import arcpy
from arcpy import env

#env.workspace = arcpy.GetParameterAsText(0)
path = r"C:\Data\Dunklin County, MO\MO_Dunklin_Live.gdb"
env.workspace = path

datasetList = arcpy.ListDatasets('*', 'Feature')

#def msg(msg):
#	arcpy.AddMessage(msg)

for dataset in datasetList:
    arcpy.env.workspace = dataset
    fcList = arcpy.ListFeatureClasses()
    for fc in fcList:
        #msg(arcpy.env.workspace + ", " + fc)
        print(arcpy.env.workspace,fc)