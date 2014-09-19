import re
import collections
 

def stringFromText(string):
	#Formatting string and separating for use as a list
	#string usually contained within [], remove these
	if string.startswith('[') and string.endswith(']'):
	    string = string[1:-1]

	 
	#substitute non-alphanumeric with a space
	#string = re.sub('[^\w.\s-+]+', ' ', string)

	string = string.replace(';', ' ')

	#split into list by whitespace

	#string = [float(x.strip()) for x in string.split(' ')]
	matrix = []
	xl = string.split(' ')
	for x in xl:
		# print x
		if x != '':
			if x == 'NA':
				matrix.append(0)
			else:
				if x == 'NDY':
					matrix.append(0)
				else:
					matrix.append(float(x.strip()))

	return matrix

def classNamesFromText(string):
	classNames = []
	string = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', string)


	for className in string:
		if className.startswith('"') and className.endswith('"'):
	   		className = className[1:-1]
	   		className = className.replace(':', ';')
	   		classNames.append(className)

	return classNames

def test():
	m = stringFromText('[0.367439333 0 0.001552 0.219795;0.299513 0.503854 0 0;0.125465 0.375199333 0.605873 0.014981333;0 0.017544 0.302857 0.966292]')
	assert(m[0]==0.367439333)
	assert(m[2]==0.001552)
	assert(len(m)==16)
	t = classNamesFromText('"One developed leaf, maximum of one pair of fronds","No leaf has more than two pairs of fronds","No leaf has more than four pairs of fronds","At least one leaf has more than 4 pairs of fronds"')
	assert(t[0]=="One developed leaf, maximum of one pair of fronds")
	assert(len(t)==4)
