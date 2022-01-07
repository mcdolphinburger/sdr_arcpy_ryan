import arcpy, arcpy.mapping, sys, string, datetime
from arcpy import env

workspace = arcpy.GetParameterAsText(0)
arcpy.env.workspace = workspace

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = ['']  + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_datasets=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        arcpy.AddMessage(path)