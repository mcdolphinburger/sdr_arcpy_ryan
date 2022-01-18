
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: detectbadstreettypes.py
Created: 20170204
Modified: 20170510
About: Scrubs street type values. Will fix common errors and notify on non-standard values
       that are not common or fixable.
       
       Only evaluates the values in a single field, presumably the Street Type field.

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

	

# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value




# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)			  		# Feature Layer containing street name fields
strtypfld = arcpy.GetParameterAsText(1)			  	# The street type field in lyr


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
oidfld = arcpy.Describe(lyr).OIDFieldName
curfields = []
curfields.append(oidfld)
curfields.append(strtypfld)

strtypes = []
strtypes = [
	["ALLEY","ALY","AL"],
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
	["LANE","LN","LANE"],
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
	["TERRACE","TER","TERR"],
	["THROUGHWAY","TRWY","-"],
	["TRACE","TRCE","TRC"],
	["TRACK","TRAK","-"],
	["TRAFFICWAY","TRFY","-"],
	["TRAIL","TRL","TR"],
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
	
dictStrType = {}
for t in strtypes:
	#msg(t[1])
	dictStrType[t[1]] = t[1]


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	

msg("\n\nScrubbing STREET_TYPE values in " + lyr + "\n-----------------------------------------------------------------\n")




# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# cur = arcpy.da.UpdateCursor(lyr)
cur = arcpy.da.UpdateCursor(lyr, curfields)
for row in cur:
	id = row[0]
	st = row[1]
	if st == "LP":
		msg("Fixing " + str(id) + ": " + "LP --> LOOP")
		row[1] = "LOOP"
		cur.updateRow(row)
	elif st == "AV":
		msg("Fixing " + str(id) + ": " + "AV --> AVE")
		row[1] = "AVE"
		cur.updateRow(row)
	elif st == "TERR":
		msg("Fixing " + str(id) + ": " + "TERR --> TER")
		row[1] = "TER"
		cur.updateRow(row)
	elif st == "TR":
		msg("Fixing " + str(id) + ": " + "TR --> TRL")
		row[1] = "TRL"
		cur.updateRow(row)
	elif st == "WY":
		msg("Fixing " + str(id) + ": " + "WY --> WAY")
		row[1] = "WAY"
		cur.updateRow(row)
	elif st == "VIEW":
		msg("Fixing " + str(id) + ": " + "VIEW --> VW")
		row[1] = "AVE"
		cur.updateRow(row)
	elif st == "CR":
		msg("Fixing " + str(id) + ": " + "CR --> CIR")
		row[1] = "CIR"
		cur.updateRow(row)
	elif st == "TRC":
		msg("Fixing " + str(id) + ": " + "TRC --> TRCE")
		row[1] = "TRCE"
		cur.updateRow(row)
	elif st == "AL":
		msg("Fixing " + str(id) + ": " + "AL --> ALY")
		row[1] = "ALY"
		cur.updateRow(row)
	elif st == "PKY":
		msg("Fixing " + str(id) + ": " + "PKY --> PKWY")
		row[1] = "PKWY"
		cur.updateRow(row)	
	elif st == "FRWY":
		msg("Fixing " + str(id) + ": " + "FRWY --> FWY")
		row[1] = "FWY"
		cur.updateRow(row)
	elif st != "" and not st in dictStrType:
		msg("Flagging " + str(id) + ":  " + st)

row, cur = None, None



arcpy.AddMessage("\n\nDone!\n\n")



	




