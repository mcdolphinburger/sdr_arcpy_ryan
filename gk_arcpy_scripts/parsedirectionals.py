
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: parsedirectionals.py
Created: 20191115
Modified: 20191115
About: Parses Pre and Post Directionals from root street name
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
	
def ParseStreetType(val):
    val.strip()
    strtyp = ""
    strnam = val
    for typ in strtypes:
        x = " " + typ[1]			# the street type abbreviation with a leading space added on
        k = len(x)					# the length of the street type abbreviation with a leading space added on
        if val[k*-1:] == x:			
            strtyp = typ[1]
            strnam = val[:len(val)-k]
            return [strnam, strtyp]

    return [strnam, strtyp]

	

	
# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value


# ==============================================================================================================
#                                                                             I N I T I A L I Z E   S C R I P T
# ==============================================================================================================

directionals = []
directionals = [[" N"], [" S"], [" E"], [" W"], [" NE"], [" NW"], [" SE"], [" SW"]]

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
lyr = arcpy.GetParameterAsText(0)			  		# Feature Layer containing compiled road name attributes
fldPre = arcpy.GetParameterAsText(1)				# Field containing pre directional values
fldNam = arcpy.GetParameterAsText(2)				# Field containing street name values
fldTyp = arcpy.GetParameterAsText(2)				# Field containing street type values
fldPdr= arcpy.GetParameterAsText(2)					# Field containing post directional values

# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
oidfld = arcpy.Describe(lyr).OIDFieldName

# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	
msg("\n\nParsing street types from field " + fldN + " and putting them in field " + fldT + ".\n\n")

# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================
	

# Pass 1: Parsing pre directional values
# -----------------------------------------------------------------------------------------------------------
curfields = [fldPre, fldNam, fldTyp, fldPdr, oidfld]
cur, row = None, None
cur = arcpy.da.UpdateCursor(lyr, curfields)
for row in cur:
    pre = row[0]
	nam = row[1]




    # q = ParseStreetType(x)
    # if q[1] != "" and len(row[1].strip()) > 0:
        # msg("  " + str(row[2]) + ": Already has a street type, skipping")
    # elif q[1] != "":
        # msg("  " + x + " --->  " + q[0] + " | " + q[1])
        # row[0] = q[0]
        # row[1] = q[1]
        # cur.updateRow(row)

cur, row = None, None	






arcpy.AddMessage("\n\nDone!\n\n")



	




