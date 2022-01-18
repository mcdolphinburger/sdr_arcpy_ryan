
"""

Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Script: parsefullstreetnames.py
Created: 20130313
Modified: 20190123
About: Parses full street name values.

"""



# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(fields, fname):
	doesexist = "FALSE"
	for fld in fields:
		if fld.name == fname:
			doesexist = "TRUE"
	return doesexist
	
def FindStreetType(val):
	z = ""
	for typ in strtypes:
		x = " " + typ[1]								# the street type abbreviation with a leading space added on
		k = len(x)											# the length of the street type abbreviation with a leading space added on
		if val[k*-1:] == x:							# the right-most "k" characters of the street name
			z = x
	return z
	
def FindStreetType2(nam, suf):
	z = ""
	for typ in strtypes:
		if typ[2] != "-":
			x = " " + typ[2]
			k = len(x)
			if nam[k*-1:] == x:
				z = x
	return z

# This function parses a compiled road name based strictly on postal standards. No exceptions
# are considered or looked for.	
#	----------------------------------------------------------------------------------------------------
def ParseIt1(nam):

	p = ""
	n = nam
	s = ""
	d = ""


#	Parse Post Directional
#	------------------------------
	if nam[-2:] == " N":
		d = "N"
		n = nam[:-2]
	elif nam[-2:] == " S":
		d = "S"
		n = nam[:-2]
	elif nam[-2:] == " E":
		d = "E"
		n = nam[:-2]
		msg(n)
	elif nam[-2:] == " W":
		d = "W"
		n = nam[:-2]
	elif nam[-3:] == " NE":
		d = "NE"
		n = nam[:-3]
	elif nam[-3:] == " NW":
		d = "NW"
		n = nam[:-3]
	elif nam[-3:] == " SE":
		d = "SE"
		n = nam[:-3]
	elif nam[-3:] == " SW":
		d = "SW"
		n = nam[:-3]
	
#	Parse Pre Directional
#	------------------------------	
	if n[:2] == "N ":
		p = "N"
		n = n[2:]
	elif n[:2] == "S ":
		p = "S"
		n = n[2:]
	elif n[:2] == "E ":
		p = "E"
		n = n[2:]
	elif n[:2] == "W ":
		p = "W"
		n = n[2:]
	elif n[:3] == "NE ":
		p = "NE"
		n = n[3:]
	elif n[:3] == "NW ":
		p = "NW"
		n = n[3:]
	elif n[:3] == "SE ":
		p = "SE"
		n = n[3:]
	elif n[:3] == "SW ":
		p = "SW"
		n = n[3:]
	
#	Parse Street Type
#	------------------------------
	s = FindStreetType(n)
	if s != "":
		x = len(s)
		n = n[:x*-1]
		s = s.strip()

#	Parse Non-Standard Street Type
#	------------------------------
	if s == "":
		s = FindStreetType2(n, s)
		if s != "":
			x = len(s)
			n = n[:x*-1]
			s = s.strip()
			f = "FLAG"

	n = n.strip()
	return [p, n, s, d]
	
# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================

strtypes = []
strtypes = [
	["ALLEY","ALY","-"],
	["ANNEX","ANX","-"],
	["ARCADE","ARC","-"],
	["AVENUE","AVE","AV"],
	["BAYOU","BYU","-"],
	["BEACH","BCH","-"],
	["BEND","BND","-"],
	["BLUFF","BLF","-"],
	["BLUFFS","BLFS","-"],
	["BOTTOM","BTM","-"],
	["BOULEVARD","BLVD","BLV"],
	["BRANCH","BR","-"],
	["BRIDGE","BRG","-"],
	["BROOK","BRK","-"],
	["BROOKS","BRKS","-"],
	["BURG","BG","-"],
	["BURGS","BGS","-"],
	["BYPASS","BYP","-"],
	["CAMP","CP","-"],
	["CANYON","CYN","-"],
	["CAPE","CPE","-"],
	["CAUSEWAY","CSWY","-"],
	["CENTER","CTR","-"],
	["CENTERS","CTRS","-"],
	["CIRCLE","CIR","CR"],
	["CIRCLES","CIRS","-"],
	["CLIFF","CLF","-"],
	["CLIFFS","CLFS","-"],
	["CLUB","CLB","-"],
	["COMMON","CMN","-"],
	["COMMONS","CMNS","-"],
	["CORNER","COR","-"],
	["CORNERS","CORS","-"],
	["COURSE","CRSE","-"],
	["COURT","CT","-"],
	["COURTS","CTS","-"],
	["COVE","CV","-"],
	["COVES","CVS","-"],
	["CREEK","CRK","-"],
	["CRESCENT","CRES","-"],
	["CREST","CRST","-"],
	["CROSSING","XING","-"],
	["CROSSROAD","XRD","-"],
	["CROSSROADS","XRDS","-"],
	["CURVE","CURV","-"],
	["DALE","DL","-"],
	["DAM","DM","-"],
	["DIVIDE","DV","-"],
	["DRIVE","DR","-"],
	["DRIVES","DRS","-"],
	["ESTATE","EST","-"],
	["ESTATES","ESTS","-"],
	["EXPRESSWAY","EXPY","-"],
	["EXTENSION","EXT","-"],
	["EXTENSIONS","EXTS","-"],
	["FALL","FALL","-"],
	["FALLS","FLS","-"],
	["FERRY","FRY","-"],
	["FIELD","FLD","-"],
	["FIELDS","FLDS","-"],
	["FLAT","FLT","-"],
	["FLATS","FLTS","-"],
	["FORD","FRD","-"],
	["FORDS","FRDS","-"],
	["FOREST","FRST","-"],
	["FORGE","FRG","-"],
	["FORGES","FRGS","-"],
	["FORK","FRK","-"],
	["FORKS","FRKS","-"],
	["FORT","FT","-"],
	["FREEWAY","FWY","-"],
	["GARDEN","GDN","-"],
	["GARDENS","GDNS","-"],
	["GATEWAY","GTWY","-"],
	["GLEN","GLN","-"],
	["GLENS","GLNS","-"],
	["GREEN","GRN","-"],
	["GREENS","GRNS","-"],
	["GROVE","GRV","-"],
	["GROVES","GRVS","-"],
	["HARBOR","HBR","-"],
	["HARBORS","HBRS","-"],
	["HAVEN","HVN","-"],
	["HEIGHTS","HTS","-"],
	["HIGHWAY","HWY","-"],
	["HILL","HL","-"],
	["HILLS","HLS","-"],
	["HOLLOW","HOLW","-"],
	["INLET","INLT","-"],
	["ISLAND","IS","-"],
	["ISLANDS","ISS","-"],
	["ISLE","ISLE","-"],
	["JUNCTION","JCT","-"],
	["JUNCTIONS","JCTS","-"],
	["KEY","KY","-"],
	["KEYS","KYS","-"],
	["KNOLL","KNL","-"],
	["KNOLLS","KNLS","-"],
	["LAKE","LK","-"],
	["LAKES","LKS","-"],
	["LAND","LAND","-"],
	["LANDING","LNDG","-"],
	["LANE","LN","LA"],
	["LIGHT","LGT","-"],
	["LIGHTS","LGTS","-"],
	["LOAF","LF","-"],
	["LOCK","LCK","-"],
	["LOCKS","LCKS","-"],
	["LODGE","LDG","-"],
	["LOOP","LOOP","LP"],
	["MALL","MALL","-"],
	["MANOR","MNR","-"],
	["MANORS","MNRS","-"],
	["MEADOW","MDW","-"],
	["MEADOWS","MDWS","-"],
	["MEWS","MEWS","-"],
	["MILL","ML","-"],
	["MILLS","MLS","-"],
	["MISSION","MSN","-"],
	["MOTORWAY","MTWY","-"],
	["MOUNT","MT","-"],
	["MOUNTAIN","MTN","-"],
	["MOUNTAINS","MTNS","-"],
	["NECK","NCK","-"],
	["ORCHARD","ORCH","-"],
	["OVAL","OVAL","-"],
	["OVERPASS","OPAS","-"],
	["PARK","PARK","-"],
	["PARKS","PARK","-"],
	["PARKWAY","PKWY","-"],
	["PARKWAYS","PKWY","-"],
	["PASS","PASS","-"],
	["PASSAGE","PSGE","-"],
	["PATH","PATH","-"],
	["PIKE","PIKE","-"],
	["PINE","PNE","-"],
	["PINES","PNES","-"],
	["PLACE","PL","-"],
	["PLAIN","PLN","-"],
	["PLAINS","PLNS","-"],
	["PLAZA","PLZ","-"],
	["POINT","PT","-"],
	["POINTS","PTS","-"],
	["PORT","PRT","-"],
	["PORTS","PRTS","-"],
	["PRAIRIE","PR","-"],
	["RADIAL","RADL","-"],
	["RAMP","RAMP","-"],
	["RANCH","RNCH","-"],
	["RAPID","RPD","-"],
	["RAPIDS","RPDS","-"],
	["REST","RST","-"],
	["RIDGE","RDG","-"],
	["RIDGES","RDGS","-"],
	["RIVER","RIV","-"],
	["ROAD","RD","-"],
	["ROADS","RDS","-"],
	["ROUTE","RTE","-"],
	["ROW","ROW","-"],
	["RUE","RUE","-"],
	["RUN","RUN","-"],
	["SHOAL","SHL","-"],
	["SHOALS","SHLS","-"],
	["SHORE","SHR","-"],
	["SHORES","SHRS","-"],
	["SKYWAY","SKWY","-"],
	["SPRING","SPG","-"],
	["SPRINGS","SPGS","-"],
	["SPUR","SPUR","-"],
	["SPURS","SPUR","-"],
	["SQUARE","SQ","-"],
	["SQUARES","SQS","-"],
	["STATION","STA","-"],
	["STRAVENUE","STRA","-"],
	["STREAM","STRM","-"],
	["STREET","ST","-"],
	["STREETS","STS","-"],
	["SUMMIT","SMT","-"],
	["TERRACE","TER","-"],
	["THROUGHWAY","TRWY","-"],
	["TRACE","TRCE","-"],
	["TRACK","TRAK","-"],
	["TRAFFICWAY","TRFY","-"],
	["TRAIL","TRL","-"],
	["TRAILER","TRLR","-"],
	["TUNNEL","TUNL","-"],
	["TURNPIKE","TPKE","-"],
	["UNDERPASS","UPAS","-"],
	["UNION","UN","-"],
	["UNIONS","UNS","-"],
	["VALLEY","VLY","-"],
	["VALLEYS","VLYS","-"],
	["VIADUCT","VIA","-"],
	["VIEW","VW","-"],
	["VIEWS","VWS","-"],
	["VILLAGE","VLG","-"],
	["VILLAGES","VLGS","-"],
	["VILLE","VL","-"],
	["VISTA","VIS","-"],
	["WALK","WALK","-"],
	["WALKS","WALK","-"],
	["WALL","WALL","-"],
	["WAY","WAY","-"],
	["WAYS","WAYS","-"],
	["WELL","WL","-"],
	["WELLS","WLS","-"]
	]
	



# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			  	# Feature Layer containing compiled road name attributes
fld = arcpy.GetParameterAsText(1)				# Field containing road name values
dotrim = arcpy.GetParameter(2)					# boolean on whether to trim compiled road name values prior to parsing
opt = arcpy.GetParameter(3)					 	# boolean to optimize parsed data or not

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)



# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	










# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# Verify parsing fields exist; create if necessary
# -----------------------------------------------------------------------------------------------------------
msg("\nChecking fields:")

	
# check for pre directional field
if FieldExists(fields, "R1") == "FALSE":
	msg("  R1 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "R1", "TEXT", "", "", "8", "R1", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  R1 field exists: TRUE")

# check for root name field
if FieldExists(fields, "R2") == "FALSE":
	msg("  R2 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "R2", "TEXT", "", "", "64", "R2", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  R2 field exists: TRUE")

# check for street type field	
if FieldExists(fields, "R3") == "FALSE":
	msg("  R3 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "R3", "TEXT", "", "", "16", "R3", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  R3 field exists: TRUE")

# check for post directional field
if FieldExists(fields, "R4") == "FALSE":
	msg("  R4 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "R4", "TEXT", "", "", "2", "R4", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  R4 field exists: TRUE")

# # check for parse flag field	
# if FieldExists(fields, "RF") == "FALSE":
	# msg("  RF field exists: FALSE (field created)\n")
	# arcpy.AddField_management(lyr, "RF", "TEXT", "", "", "16", "RF", "NULLABLE", "NON_REQUIRED", "")
# else:
	# msg("  RF field exists: TRUE\n")
	
	
# Checking for optional parameters
# -----------------------------------------------------------------------------------------------------------

# trim compiled road name field, if necessary
if dotrim:
	msg("Compiled Road Name values will be trimmed.")
	# arcpy.CalculateField_management(lyr, fld, "!"+ fld + "!.strip()", "PYTHON_9.3", "")
	arcpy.CalculateField_management(lyr, fld, "TRIM([" + fld + "])", "VB", "")
else:
	msg("Compiled Road Name values will not be trimmed.")

# optimize parsing
if opt:
	msg("Parsed road name components will be optimized.\n")
else:
	msg("Parsed road name components will not be optimized.\n")


# Pass 1: Parsing based strictly on postal standards
# -----------------------------------------------------------------------------------------------------------
cur, row = None, None
cur = arcpy.UpdateCursor(lyr)
for row in cur:
	x = row.getValue(fld)
	q = ParseIt1(x)

	row.R1 = q[0]
	row.R2 = q[1]
	row.R3 = q[2]
	row.R4 = q[3]

	cur.updateRow(row)

cur, row = None, None	






arcpy.AddMessage("\n\nDone!\n\n")



	




