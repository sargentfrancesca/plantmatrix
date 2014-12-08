import datetime
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from flask import current_app
from app.models import User, Plant, Species
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

engine = create_engine('sqlite:///data-dev.sqlite', echo=False)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()


def importCSV():
	import csv
	with open('matrices-main.csv', 'rU') as csvfile:
		fileread = csv.reader(csvfile, delimiter=',', quotechar='"')
		allPlants = []
		allSpecies = []

		for i, row in enumerate(fileread):
			if i != 0:
				allPlants.append({
					'name' : row[21],
					'matrixnumber' : row[51], 
					'matrix' : row[55],
					'dimension' : row[53],
					'matrixclassnumber' : row[52],
					'matrixclassorganised' : row[50],
					'matrixsplit' : row[48],
					'classnames' : row[56],
					'observation' : row[49],
					'matrixcomposite' : row[27],
					'matrixtreatment' : row[28],
					'matrixcaptivity' : row[29],
					'matrixstartyear' : row[30],
					'matrixstartseason' : row[31],
					'matrixstartmonth' : row[32],
					'matrixendyear' : row[33],
					'matrixendseason' : row[34],
					'matrixendmonth' : row[35],
					'studiedsex' : row[26],
					'population' : row[36],
					'latdeg' : row[37],
					'latmin' : row[38],
					'latsec' : row[39],
					'londeg' : row[40],
					'lonmin' : row[41],
					'lonsec' : row[42],
					'latitudedec' : row[43],
					'longitudedec' : row[44],
					'altitude' : row[45],
					'country' : row[46],
					'continent' : row[47],
					'criteriasize' : row[10],
					'criteriaontogeny' : row[11],
					'authors' : row[0],
					'journal' : row[1],
					'yearpublication' : row[2],
					'doiisbn' : row[3],
					'additionalsource' : row[4],
					'enteredby' : row[22],
					'entereddate' : row[23],
					'source' : row[24],
					'statusstudy' : row[57],
					'statusstudyref' : row[58],
					'statuselsewhere' : row[59],
					'statuselsewhereref' : row[60]
					})
			

			allSpecies.append({
					'name' : row[21],
					'speciesauthor' : row[25],
					'kingdom' : row[13],
					'phylum' : row[14],
					'angiogymno' : row[15],
					'dicotmonoc' : row[16],
					'_class' : row[17],
					'_order' : row[18],
					'family' : row[19],
					'genus' : row[20],
					'ecoregion' : row[5],
					'growthtype' : row[6],
					'growthformraunkiaer' : row[7],
					'annualperiodicity' : row[9],
					'planttype' : row[54],
					'commonname' : '',
					'originalimageurl' : ''

				})

			# print allSpecies

			for species in allSpecies:
				
				speciesname = species['name']
				# print speciesname
				
				# check = session.query(Species).filter_by(name=speciesname).first()
				# print check 

				# checkname = session.query('Species').filter_by(speciesauthor=speciesname).first()


				if session.query(Species).filter_by(name=speciesname).first() is None:
					
					print "Entering new data", speciesname

					new_entry = Species(
						species['name'],
						species['speciesauthor'],
						species['kingdom'],
						species['phylum'],
						species['angiogymno'],
						species['dicotmonoc'],
						species['_class'],
						species['_order'],
						species['family'],
						species['genus'],
						species['ecoregion'],
						species['growthtype'],
						species['growthformraunkiaer'],
						species['annualperiodicity'],
						species['planttype'],
						species['commonname'],
						species['originalimageurl']
						)

					session.add(new_entry)

				else:
					# print species['name'], "Match!"
					pass
					

			session.commit()
				
					

			# for plant in allPlants:
			# 	print plant['matrixnumber']
				# # try:
				# # 	p = PlantMatrix(plant['name'], plant['matrix'], plant['classNames'], plant['dimension'])
				# # 	if not p.isValid():
				# # 		p.prettyPrint()
				# # 	else:
				# # 		p.dotGraph().write_png('graph/'+plant['matrixnumber']+'_'+p.name+'_dot.png', prog='dot')

				# # except:
				# 	pass



importCSV()			

 
# engine = create_engine('sqlite:///data-dev.sqlite', echo=False)
 
# # create a Session
# Session = sessionmaker(bind=engine)
# session = Session()


# new_entry = Species("Alaria nana", 
# 		   "Alaria_nana",
# 		   "Chromalveolata",
# 		   "Heterokontophyta",
# 		   "NA",
# 		   "NA",
# 		   "Phaeophyceae",
# 		   "Laminariales",
# 		   "Alariaceae",
# 		   "Alaria",
# 		   "TCF",
# 		   "Algae",
# 		   "Hydrophyte",
# 		   5,
# 		   "Alga",
# 		   "Unknown",
# 		   "http://")

# new_entry.plants = [Plant(1, 
# 	"[0.46145 0.153 0.33615 0.24765 0.5238 0.59225;0.2096 0.2118 0.33615 0.24765 0.5238 0.59225;0.0705 0.0633 0.10815 0.0827 0 0;0.0267 0.0947 0.03155 0.15405 0 0;0.06295 0.19195 0.3909 0.24355 0 0;0.02305 0.281 0.1321 0.35145 0 0]", 
# 	6, 
# 	1, 
# 	"active", 
# 	"Divisible", 
# 	'\"<600cm_; Growth rate 1 (slow)","600-1199cm_; Growth rate 2 (fast)","<600cm_; Growth rate 1 (slow)","600-1199cm_; Growth rate 2 (fast)","<600cm_; Growth rate 1 (slow)","600-1199cm_; Growth rate 2 (fast)\"', 
# 	"1997 was El Nino Year", 
# 	"Mean", 
# 	"Unmanipulated", 
# 	"W", 
# 	1997, 
# 	"NA", 
# 	5, 
# 	2001, 
# 	"NA", 
# 	9, 
# 	"A", 
# 	"Tatoosh Island", 
# 	48, 
# 	24, 
# 	0, 
# 	-124, 
# 	44, 
# 	0, 
# 	48.4, 
# 	-123.2666667, 
# 	1, 
# 	"USA", 
# 	"N America", 
# 	"Frond width", 
# 	"Based on size",
# 	"Pfister; Wang", 
# 	"Ecol",
# 	2005,
# 	"10.1890/04-1952",
# 	"Pfister Ecol 2005_pers_communication.xlsx",
# 	"Stefan",
# 	"12.13.2013",
# 	"NDY",
# 	"native",
# 	"see authors",
# 	"not introduced",
# 	"NA")]


# # new_entry.species = Species("Alaria nana", 
# #                            "Alaria_nana",
# #                            "Chromalveolata",
# #                            "Heterokontophyta",
# #                            "NA",
# #                            "NA",
# #                            "Phaeophyceae",
# #                            "Laminariales",
# #                            "Alariaceae",
# #                            "Alaria",
# #                            "TCF",
# #                            "Algae",
# #                            "Hydrophyte",
# #                            5,
# #                            "Alga")


# # new_entry.sourceinfo = [SourceInfo("Pfister; Wang", 
# # 								"Ecol",
# # 								2005,
# # 								"10.1890/04-1952",
# # 								"Pfister Ecol 2005_pers_communication.xlsx")]

# # new_entry.submissioninfo = SubmissionInfo("Stefan",
# # 										"12.13.2013",
# # 										"NDY")

# # new_entry.invasivestatus = InvasiveStatus("native",
# # 										"see authors",
# # 										"not introduced",
# # 										"NA")

 
# # add more albums
# # more_ingredients = [Ingredient("Sweet Vermouth",
# #                      "1", "oz")]
# # new_recipe.ingredients.extend(more_ingredients)
 
# # Add the record to the session object

# # session.add(new_entry)
# # session.commit()

# # indi = session.query(IndividualPlant).filter_by(id=1).first()



# # indi.sourceinfo = [SourceInfo("Pfister; Wang", 
# # 								"Ecol",
# # 								2005,
# # 								"10.1890/04-1952",
# # 								"Pfister Ecol 2005_pers_communication.xlsx")]

# # indi.sourceinfo = unicode(indi.sourceinfo)


# session.add(new_entry)
# session.commit()

# # Add several artists
# # session.add_all([
# #     Artist("MXPX"),
# #     Artist("Kutless"),
# #     Artist("Thousand Foot Krutch")
# #     ])
# # session.commit()