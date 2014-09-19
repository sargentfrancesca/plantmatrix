from plantmatrix import PlantMatrix

import csv
with open('matrices-main.csv', 'rU') as csvfile:
	fileread = csv.reader(csvfile, delimiter=',', quotechar='"')
	allPlants = []

	for i, row in enumerate(fileread):
		if i != 0:
			allPlants.append({'name' : row[25], 'matrix' : row[55], 'classNames' : row[56], 'dimension' : row[53], 'matrixnumber' : row[51]})

		for plant in allPlants:
			print plant['matrixnumber']
			try:
				p = PlantMatrix(plant['name'], plant['matrix'], plant['classNames'], plant['dimension'])
				if not p.isValid():
					p.prettyPrint()
				else:
					p.dotGraph().write_png('graph/'+plant['matrixnumber']+'_'+p.name+'_dot.png', prog='dot')

			except:
				pass
