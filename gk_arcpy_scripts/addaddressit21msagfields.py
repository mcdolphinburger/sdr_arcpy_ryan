

"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: addaddressit21msagfields.py
Created: 20110817
Modified: 20161216
About: Adds the AddressIt 2.1 MSAG fields to the feature layer selected by the user. Provides options to add
       just one set of MSAG bound info or all three.
"""

# Import modules
# ---------------------------
import arcpy, sys, string, datetime, _My_Python_Functions
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)

def FieldExists(flds, nam):
	for fld in flds:
		if fld.name == nam:
			return True
	return False

	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
layerRCL = arcpy.GetParameterAsText(0)		# the Feature layer to add the fields to
useCOM = arcpy.GetParameter(1)				# boolean on whether to add the COMM, ECOMM and OCOMM fields
useEXC = arcpy.GetParameter(2)				# boolean on whether to add the TELCO, ETELCO and OTELCO fields
useESN = arcpy.GetParameter(3)				# boolean on whether to add the ESN, EESN and OESN fields


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
d = arcpy.Describe(layerRCL)
fc = d.FeatureClass
fds = arcpy.ListFields(layerRCL)


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\n")



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# Add Community fields (if necessary)
if useCOM:
	msg("\nValidating Community fields")
	v = "OK"
	if FieldExists(fds, "COMM"): v = "FLAG"
	if FieldExists(fds, "ECOMM"): v = "FLAG"
	if FieldExists(fds, "OCOMM"): v = "FLAG"
	if v == "OK":
		msg("Adding Community fields")
		arcpy.AddField_management(layerRCL, "COMM", "TEXT", "", "", "32", "COMM", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(layerRCL, "ECOMM", "TEXT", "", "", "32", "ECOMM", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(layerRCL, "OCOMM", "TEXT", "", "", "32", "OCOMM", "NULLABLE", "NON_REQUIRED", "")
	else:
		msg("One or more of the Community fields already exists.\n    Not creating Community fields.")

# Add Telco fields (if necessary)
if useEXC:
	msg("\nValidating Telco Exchange fields")
	v = "OK"
	if FieldExists(fds, "TELCO"): v = "FLAG"
	if FieldExists(fds, "ETELCO"): v = "FLAG"
	if FieldExists(fds, "OTELCO"): v = "FLAG"
	if v == "OK":
		msg("Adding Telco Exchange fields")
		arcpy.AddField_management(layerRCL, "TELCO", "TEXT", "", "", "4", "TELCO", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(layerRCL, "ETELCO", "TEXT", "", "", "4", "ETELCO", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(layerRCL, "OTELCO", "TEXT", "", "", "4", "OTELCO", "NULLABLE", "NON_REQUIRED", "")
	else:
		msg("One or more of the Exchange fields already exists.\n    Not creating Exchange fields.")

# Add ESN fields (if necessary)
if useESN:
	msg("Validating ESN fields")
	v = "OK"
	if FieldExists(fds, "TELCO"): v = "FLAG"
	if FieldExists(fds, "ETELCO"): v = "FLAG"
	if FieldExists(fds, "OTELCO"): v = "FLAG"
	if v == "OK":
		msg("Adding ESN fields")
		arcpy.AddField_management(layerRCL, "ESN", "LONG", "", "", "", "ESN", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(layerRCL, "EESN", "LONG", "", "", "", "EESN", "NULLABLE", "NON_REQUIRED", "")
		arcpy.AddField_management(layerRCL, "OESN", "LONG", "", "", "", "OESN", "NULLABLE", "NON_REQUIRED", "")
	else:
		msg("One or more of the ESN fields already exists.\n    Not creating ESN fields.")






arcpy.AddMessage("\n\nDone!\n\n")



	




