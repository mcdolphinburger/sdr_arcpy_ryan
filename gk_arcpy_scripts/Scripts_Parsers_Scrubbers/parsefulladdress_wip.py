
"""
Author: Glenn Kammerer
Email: gkammerer@sdrmaps.com
Tool: parsefulladdress_wip.py
Created: 20170510
Modified: 20170510
About: Parses the full address from a field containing full address values.
"""

# Import modules
# ---------------------------
import arcpy, arcpy.mapping, sys, string, datetime, fractions
from arcpy import env
from fractions import Fraction


# ==============================================================================================================
#                                                                     F U N C T I O N S / D E F I N I T I O N S
# ==============================================================================================================
def msg(msg):
	arcpy.AddMessage(msg)
	
def FieldExists(fields, fname):
	for fld in fields:
		if fld.name == fname:
			return True
			break
	return False
	
def FindStreetType(val):
	z = ""
	for typ in strtypes:
		x = " " + typ[1]					# the street type abbreviation with a leading space added on
		k = len(x)							# the length of the street type abbreviation with a leading space added on
		if val[k*-1:] == x:					# the right-most "k" characters of the street name
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
	
def IsANumber(n):
	try:
		float(n)
		return True
	except ValueError:
		try:
			Fraction(n)
			return True
		except ValueError:
			return False


#   This function parses a compiled road name based strictly on postal standards. No exceptions
#   are considered or looked for.	
#	----------------------------------------------------------------------------------------------------
def ParseIt1(fulladd):
	# Establish default values for the return values before any parsing takes place
	a = 0
	p = ""
	n = fulladd
	s = ""
	d = ""
	# Check that the full address value passed in actually has characters
	if len(fulladd) == 0:
		# no characters, set blank values for return values
		a = 0
		p = ""
		n = ""
		s = ""
		d = ""
	else:
		# has characters, split the full address into words separated by a space
		fulladdlist = fulladd.split()
        # check the count of words in the words list. if greater than 1 then proceed
        if len(fulladdlist) = 1:
            # only one word in full address value, let's try something else
            msg("Full address is all one text string, trying something else.")
        else:
            # more than 1 word in list, proceed as normal
            msg("Proceeding as normal.")
            # is the first word of the string a number?
            if IsANumber(fulladdlist[0]):
                # it is, set the house number and then the street name value to be parsed
                a = fulladdlist[0]
                nam = fulladd[len(a):].strip()
                # Parse Post Directional
                if nam[-2:] == " N":
                    d = "N"
                    n = nam[:-2]
                elif nam[-2:] == " S":
                    d = "S"
                    n = nam[:-2]
                elif nam[-2:] == " E":
                    d = "E"
                    n = nam[:-2]
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
                else:
                    n = nam
                
                # Parse Pre Directional
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
                
                # Parse Street Type
                s = FindStreetType(n)
                if s != "":
                    x = len(s)
                    n = n[:x*-1]
                    s = s.strip()

                n = n.strip()
            else:
                # first word not numeric, set flag value in house number and put full address value in name field
                a = -999
                n = fulladd
	return [a, p, n, s, d]
	
	
	
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
lyr = arcpy.GetParameterAsText(0)			  	# Feature Layer containing Full Address data
fld = arcpy.GetParameterAsText(1)				# Field containing Full Address values



# Initialize main variables.
# --------------------------------------------------------------------------------------------------------------
fields = arcpy.ListFields(lyr)
fds = []
fds.append('OID@')
fds.append(fld)
fds.append('A1')
fds.append('R1')
fds.append('R2')
fds.append('R3')
fds.append('R4')




# Introduction message (if necessary)
# -------------------------------------------------------------------------------------------------------------	





# ==============================================================================================================
#                                                                                        D O   T H E   W O  R K
# ==============================================================================================================


# Verify parsing fields exist; create if necessary
# -----------------------------------------------------------------------------------------------------------
msg("\nChecking fields:")

	
# check for house number field
if not FieldExists(fields, "A1"):
	msg("  A1 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "A1", "LONG", "", "", "", "A1", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  A1 field exists: TRUE")

# check for pre directional field	
if not FieldExists(fields, "R1"):
	msg("  R1 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "R1", "TEXT", "", "", "8", "R1", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  R1 field exists: TRUE")

# check for root name field
if not FieldExists(fields, "R2"):
	msg("  R2 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "R2", "TEXT", "", "", "64", "R2", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  R2 field exists: TRUE")

# check for street type field	
if not FieldExists(fields, "R3"):
	msg("  R3 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "R3", "TEXT", "", "", "16", "R3", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  R3 field exists: TRUE")

# check for post directional field
if not FieldExists(fields, "R4"):
	msg("  R4 field exists: FALSE (field created)")
	arcpy.AddField_management(lyr, "R4", "TEXT", "", "", "2", "R4", "NULLABLE", "NON_REQUIRED", "")
else:
	msg("  R4 field exists: TRUE")

	
# Get the first N characters in a string: val[:N], where val is a string value
# Get the last N characters in a string: val[-N:], where val is a string value
# Strip off the first N characters in a string: val[N:], where val is a string value
# Strip off the last N characters in a string: val[:-N], where val is a string value
	
	
	
# Checking for optional parameters
# -----------------------------------------------------------------------------------------------------------	
	
with arcpy.da.UpdateCursor(lyr, fds) as cur:
	for row in cur:
		fadd = row[1].strip().upper()
		fulladdparse = ParseIt1(fadd)
		if fulladdparse[0] == -999:
			msg("Can't parse OID " + str(row[0]) + ", value: " + fadd)
		row[2] = fulladdparse[0]
		row[3] = fulladdparse[1]
		row[4] = fulladdparse[2]
		row[5] = fulladdparse[3]
		row[6] = fulladdparse[4]
		cur.updateRow(row)





arcpy.AddMessage("\n\nDone!\n\n")



	




