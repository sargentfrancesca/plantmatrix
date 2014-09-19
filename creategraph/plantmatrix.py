import pydot
import math
import re
import utils

class PlantMatrix:
	def __init__(self, name, matrix, classNames, dimension):
		self.name = name
		self.matrix = utils.stringFromText(matrix)
		self.classNames = utils.classNamesFromText(classNames)
		self.dimension = int(dimension)

	def isValid(self):
		return len(self.classNames)==self.dimension and len(self.matrix)==self.dimension*self.dimension

	def prettyPrint(self):
		print "Name: "+self.name
		print "Class Name Size: "+str(len(self.classNames))+" Squared: "+str(len(self.classNames)*len(self.classNames))
		print "Matrix Size: "+str(len(self.matrix))+" Square Root: "+str(math.sqrt(len(self.matrix)))
		print "Reported Dimension: "+str(self.dimension)
		if str(self.dimension) != str(len(self.classNames)):
			print self.classNames

	def dotGraph(self):
		graph = pydot.Dot(graph_type='digraph', rankdir="LR")
		#Organise into stages
		classIndices = {}

		#Add classNames to graph as nodes 
		for (i, className) in enumerate(self.classNames):
			#print className	
			classIndices[className] = i
			graph.add_node(pydot.Node(className, shape="circle"))

		print classIndices

		for rowClassName in self.classNames:
			row = classIndices[rowClassName]
			for colClassName in self.classNames:
				col = classIndices[colClassName]
				v = self.matrix[(row*self.dimension) + col]
				if v > 0:
					graph.add_edge(pydot.Edge(colClassName, rowClassName, label=str(v)))

		return graph



def test(): 
	name = 'Asplenium_Cuneifolium'
	matrix = '[0.367439333 0 0.001552 0.219795;0.299513 0.503854 0 0;0.125465 0.375199333 0.605873 0.014981333;0 0.017544 0.302857 0.966292]'
	classNames = '"One developed leaf, maximum of one pair of fronds","No leaf has more than two pairs of fronds","No leaf has more than four pairs of fronds","At least one leaf has more than 4 pairs of fronds"'
	dimension = "4"

	p = PlantMatrix(name, matrix, classNames, dimension)
	assert(p.isValid())
 	p.dotGraph().write_png(p.name+'_dot.png', prog='dot')

