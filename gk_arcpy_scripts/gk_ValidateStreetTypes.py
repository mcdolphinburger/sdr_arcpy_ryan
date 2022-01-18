# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# ValidateStreetTypes.py
# Created on: 2013-04-07
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
import arcpy, arcpy.mapping, sys, string, datetime, os
from arcpy import env


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def IsValidStreetType(x):
	for t in strtypes:
		if x.upper() == t[1]:
			return True
	return False


	
# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================
	


# Script arguments
# --------------------------------------------------------------------------------------------------------------
lyr = arcpy.GetParameterAsText(0)						# Feature Layer; the layer to act on
fld = arcpy.GetParameterAsText(1)						# Field; from the feature layer above
fix = arcpy.GetParameterAsText(2)						# Boolean; fix street types or not


# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
oidfld = arcpy.Describe(lyr).OIDFieldName

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
	["PARKWAY","PKWY","PKY"],
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
	["WAY","WAY","WY"],
	["WAYS","WAYS","-"],
	["WELL","WL","-"],
	["WELLS","WLS","-"]
	]


# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	



# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================

msg("\nEvaluating Street Type values in " + lyr)
msg("--------------------------------------------------------------------------\n")



cur = arcpy.SearchCursor(lyr)
for row in cur:
	st = row.getValue(fld).strip()
	vid = row.getValue(oidfld)
	if st != "" and not IsValidStreetType(st):
		msg(str(vid) + ":  " + st)
row, cur = None, None


arcpy.AddMessage("\n\nDone!\n\n")



	




