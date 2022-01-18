# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# DetectTextInNumbers.py
# Created on: 2016-09-27
#
#
# Description: 
# ----------------
#  
# 
# 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)

	
# def FieldExists(fields, fname):
	# doesexist = "FALSE"
	# for fld in fields:
		# if fld.name == fname:
			# doesexist = "TRUE"
	# return doesexist

	
# def FindStreetType(val):
	# z = ""
	# for typ in strtypes:
		# x = " " + typ[1]			# the street type abbreviation with a leading space added on
		# k = len(x)					# the length of the street type abbreviation with a leading space added on
		# if val[k*-1:] == x:			# the right-most "k" characters of the street name
			# z = x
	# return z
	
	
# def FindStreetType2(nam, suf):
	# z = ""
	# for typ in strtypes:
		# if typ[2] != "-":
			# x = " " + typ[2]
			# k = len(x)
			# if nam[k*-1:] == x:
				# z = x
	# return z

	
# def CheckStreetType(t):
	# for i in strtypes:
		# if t == str(i[1]):
			# return True
	# return False
	
	
# def CheckNameOK(n):
	# for t in strtypes:
		# x = " " + str(t[0])
		# if n[-1*len(x):] == x:
			# return True
			# break
	# return False
		

# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================





# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			  		# Feature Layer
fld = arcpy.GetParameterAsText(1)			  		# The the field to check


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
oidfld = arcpy.Describe(lyr).OIDFieldName



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\n\nAnd away we go!\n-------------------------------------------------\n")




# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# cur = arcpy.UpdateCursor(lyr)
cur = arcpy.SearchCursor(lyr)
for row in cur:
	i = row.getValue(oidfld)
	val = row.getValue(fld)
	#msg(val)
	if val is None:
		msg(str(i) + ":  NULL")
	elif not val.isnumeric():
		msg(str(i) + ":  " + val)

row, cur = None, None



arcpy.AddMessage("\n\nDone!\n\n")



	




