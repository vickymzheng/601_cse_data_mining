# import sys
import math

def divideList(someList, divisor):
	for index in range(0, len(someList)):
		someList[index] = someList[index]/divisor

def getData(fileName):
	toRead = open(fileName)
	samples = []
	line = toRead.readline()
	while line != "":
	    sample = line.split()
	    myAssignment = -1
	    sample.append(myAssignment)
	    samples.append(sample)
	    line = toRead.readline()
	return samples

def getVariance(numList, mean, numSamples):
	sumSquareDiff = 0
	for sample in numList:
		sumSquareDiff = sumSquareDiff + (mean - sample)**2
	variance = sumSquareDiff/numSamples
	return variance

def isNumeric(potentialNumber):
	try:
		float(potentialNumber)
		return True
	except ValueError:
		return False

def addLists(list1, list2):
	#the two lists should be the same length
	numElements = len(list1)
	for index in range(0, numElements):
		if (isNumeric(list2[index])):
			list1[index] = list1[index] + list2[index]

def dataPreprocess(data, numSamples, numAttributes):
	for attributeNum in range(0, numAttributes):
		if (isNumeric(data[0][attributeNum])):
			for sampleNum in range(0, numSamples):
				data[sampleNum][attributeNum] = float(data[sampleNum][attributeNum])
		# else:
		# 	for sampleNum in range(0, numSamples):
		# 		if data[sampleNum][attributeNum] == "Present":
		# 			data[sampleNum][attributeNum] = 1
		# 		else:
		# 			data[sampleNum][attributeNum] = 0
	return data

def statData(samples, meansPresent, meansAbsent, variancesPresent, variancesAbsent, 
	nominalPresentAndPresent, nominalAbsentAndPresent, nominalPresentAndAbsent, nominalAbsentAndAbsent):
	numPresent = 0
	numAbsent = 0
	presentSamples = []
	absentSamples = []
	numAttributes = len(samples[0])-2
	for sample in samples:
		if sample[-2] == 1:
			#this means present
			presentSamples.append(sample)
			numPresent+=1
			#meansPresent =  map(lambda x,y: x + y, meansPresent, sample[0:-2])
			addLists(meansPresent, sample[0:-2])
		else:
			absentSamples.append(sample)
			numAbsent+=1
			#meansAbsent =  map(lambda x,y: x + y, meansAbsent, sample[0:-2])
			addLists(meansAbsent, sample[0:-2])

	#meansPresent = map(lambda x: x/numPresent, meansPresent)
	#meansAbsent = map(lambda x: x/numAbsent, meansAbsent)
	divideList(meansPresent, numPresent)
	divideList(meansAbsent, numAbsent)

	for i in range(0, numAttributes):
		if (isNumeric(samples[0][i])):
			presentCol = []
			absentCol = []
			for presentSample in presentSamples:
				presentCol.append(presentSample[i])

			for absentSample in absentSamples:
				absentCol.append(absentSample[i])

			variancesPresent[i] = getVariance(presentCol, meansPresent[i], numPresent)
			variancesAbsent[i] = getVariance(absentCol, meansAbsent[i], numAbsent)
		else:
			presentAndPresent = 0
			presentAndAbsent = 0
			absentAndPresent = 0
			absentAndAbsent = 0

			for presentSample in presentSamples:
				if (presentSample[i] == "Present"):
					presentAndPresent+=1
				if (presentSample[i] == "Absent"):
					absentAndPresent+=1

			if (not (presentAndPresent + absentAndPresent == numPresent)):
				print "Something went wrong in nominal counting 1"

			for absentSample in absentSamples:
				if (absentSample[i] == "Present"):
					presentAndAbsent+=1
				if (absentSample[i] == "Absent"):
					absentAndAbsent+=1

			if (not (presentAndAbsent + absentAndAbsent == numAbsent)):
				print "Something went wrong in nominal counting 2"
			
			nominalPresentAndPresent[i] = float(presentAndPresent)/numPresent
			nominalAbsentAndPresent[i] = float(absentAndPresent)/numPresent
			nominalPresentAndAbsent[i] = float(presentAndAbsent)/numAbsent
			nominalAbsentAndAbsent[i] = float(absentAndAbsent)/numAbsent

	return (numPresent, numAbsent)

def prior(samples, present, notPresent):
	for sample in samples:
		if sample[-1] == 1:
			present+=1
		if sample[-1] == 0:
			notPresent+=1
	return (present, notPresent)

def probability(x, mean, variance):
	exponent = .5*(((x - mean)**2)/(variance))
	base = 1/math.sqrt(math.pi*variance*2)
	return base**exponent

def listProduct(probList):
	product = 1
	for prob in probList:
		product*=prob
	return product

def checkCorrect(samples):
	numCorrect = 0.0
	numSamples = len(samples)
	for sample in samples:
		if (sample[-2] == sample[-1]):
			numCorrect+=1

	return numCorrect/numSamples

def bayes(fileName):
	samples = getData(fileName)

	numSamples = len(samples)
	numCols = len(samples[0]) 
	dataPreprocess(samples, numSamples, numCols)

	numAttributes = numCols - 2 #removing ground truth column and my assignment column

	meansPresent = [0]*(numAttributes)
	variancesPresent = [0]*(numAttributes)
	meansAbsent = [0]*numAttributes
	variancesAbsent = [0]*numAttributes

	nominalPresentAndPresent = [0]*numAttributes
	nominalAbsentAndPresent = [0]*numAttributes
	nominalPresentAndAbsent = [0]*numAttributes
	nominalAbsentAndAbsent = [0]*numAttributes

	numPresent = 0
	numAbsent = 0
	(numPresent, numAbsent) = statData(samples, meansPresent, meansAbsent, variancesPresent, variancesAbsent,
		nominalPresentAndPresent, nominalAbsentAndPresent, nominalPresentAndAbsent, nominalAbsentAndAbsent)

	if (not (numPresent + numAbsent == numSamples)):
		print "Something went wrong"
		return

	# print meansPresent
	# print meansAbsent
	# print variancesPresent
	# print variancesAbsent

	present = 0.0
	notPresent = 0.0
	(present, notPresent) = prior(samples, present, notPresent)
	present = present/numSamples
	notPresent = notPresent/numSamples

	for sample in samples:
		attributes = sample[0:numAttributes]
		attributeProbabilitiesPresent = [0]*numAttributes
		attributeProbabilitiesAbsent = [0]*numAttributes
		for i in range(0, numAttributes):
			currentAttribute = attributes[i]
			if (isNumeric(currentAttribute)):
				attributeProbabilitiesPresent[i] = probability(currentAttribute, meansPresent[i], variancesPresent[i])
				attributeProbabilitiesAbsent[i] = probability(currentAttribute, meansAbsent[i], variancesAbsent[i])
			else: 
				#count num present and x div present
				#count num absent and x div absent
				if (currentAttribute == "Present"):
					attributeProbabilitiesPresent[i] = nominalPresentAndPresent[i]
					attributeProbabilitiesAbsent[i] = nominalPresentAndAbsent[i]
				else:
					attributeProbabilitiesPresent[i] = nominalAbsentAndPresent[i]
					attributeProbabilitiesAbsent[i] = nominalAbsentAndAbsent[i]

		probPresent =  listProduct(attributeProbabilitiesPresent)*present
		probAbsent = listProduct(attributeProbabilitiesAbsent)*notPresent

		if (probPresent > probAbsent):
			sample[-1] = 1
		else:
			sample[-1] = 0

	print checkCorrect(samples)

bayes("project3_dataset1.txt") 