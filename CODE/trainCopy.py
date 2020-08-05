import copy
import math
import pickle
import sys
import random
featureDictionary = {"unused": ["wordSize",
                                "averageWordSize",
                                "numberOfNAndT",

                                "appearenceOfOf",
                                "appearenceOfAnd",
                                "appearenceOfTo",
                                "appearenceOfIn",
                                "appearenceOfZijn",
                                "appearenceOfDat",
                                "appearenceOfVoor",
                                "appearenceOfHij",
                                "appearenceOfThe",
                                "appearenceOfAls",
                                "appearenceOfDutchExtraCharacters",
                                "startingLetterIsS"
                                ],
                     "used": []}

englishFeatures = ["appearenceOfThe", "appearenceOfOf",
                   "appearenceOfAnd",
                   "appearenceOfTo",
                   "appearenceOfIn", "startingLetterIsS", "numberOfNAndT"]

dutchFeatures = ["wordSize",
                 "averageWordSize", "appearenceOfAls", "appearenceOfZijn",
                 "appearenceOfDat",
                 "appearenceOfVoor",
                 "appearenceOfHij", "appearenceOfDutchExtraCharacters" ]

sampleWeightArray = []
newCompleteData = []

finalListOfStumpsForPrediction = []


class Node:

    def __init__(self):
        self.leftChild = None
        self.rightChild = None
        self.data = []  # this will be the list of index of the example in the dataset
        self.dutchExamples = []
        self.englishExamples = []
        self.questionToBeAsked = None
        self.isDTnode = None
        self.successfulGuessExamples = []
        self.unsuccessfulGuessExampless = []
        self.weight = None


trainingFile = None
modelFile = None
learningType = None

if len(sys.argv) > 1:
    trainingFile = sys.argv[1]
    modelFile = sys.argv[2]
    learningType = sys.argv[3]
else:
    trainingFile = input("Enter the path of examples file")
    modelFile = input("Enter the path of model file")
    learningType = input("Enter the learning type")

fpTrainingData = open(trainingFile, "r")
completeData = fpTrainingData.readlines()

root = Node()

for i in range(len(completeData)):
    root.data.append(i)
    if completeData[root.data[i]][0] == "n":
        root.dutchExamples.append(i)
    else:
        root.englishExamples.append(i)

leftNode = Node()
rightNode = Node()


def checkIfStartingLetterIsSinMostOfTheWordsOfSentence(wordListOfSentence: list):
    numberOfWordsStartingWithS = 0
    numberOfWordsStartingWithOtherThanS = 0

    for word in wordListOfSentence:
        if word[0].lower() == "s":
            numberOfWordsStartingWithS += 1
        else:
            numberOfWordsStartingWithOtherThanS += 1

    return numberOfWordsStartingWithS > numberOfWordsStartingWithOtherThanS


def checkForAppearenceOfDutchExtraCharacters(wordListOfSentence: list):
    for word in wordListOfSentence:
        for letter in word.lower():
            if letter in "éëïóöü":
                return True

    return False


def checkForAverageWordSize(wordListOfSentence: list, averageWordSize=5):
    wordSizeSum = 0
    for word in wordListOfSentence:
        wordSizeSum += len(word)

    if (wordSizeSum / len(wordListOfSentence) > averageWordSize):
        return True

    return False


def checkForAppearenceOfOf(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "of":
            return True

    return False


def checkForAppearenceOfAnd(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "and":
            return True

    return False


def checkForAppearenceOfTo(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "to":
            return True

    return False


def checkForAppearenceOfIn(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "in":
            return True

    return False


def checkForAppearenceOfZijn(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "zijn":
            return True

    return False


def checkForAppearenceOfDat(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "dat":
            return True

    return False


def checkForAppearenceOfVoor(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "voor":
            return True

    return False


def checkForAppearenceOfHij(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "hij":
            return True

    return False


def checkForAppearenceOfThe(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "the":
            return True

    return False


def checkForAppearenceOfAls(wordListOfSentence: list):
    for word in wordListOfSentence:
        if word.lower() == "als":
            return True

    return False


def checkIfSentenceContainsWordOfSizeGreaterThanGivenSize(wordListOfSentence: list, wordLength=9):
    for word in wordListOfSentence:
        if len(word) > wordLength:
            return True

    return False


def checkIfNumberOfNisGreaterThanNumberOfT(wordListOfSentence: list):
    numberOfN = 0
    numberOfT = 0

    for word in wordListOfSentence:
        numberOfN += word.lower().count("n")
        numberOfT += word.lower().count("t")

    if numberOfN > numberOfT:
        return True
    return False


featureFunctionMapping = {
    "wordSize": checkIfSentenceContainsWordOfSizeGreaterThanGivenSize,
    "averageWordSize": checkForAverageWordSize,
    "numberOfNAndT": checkIfNumberOfNisGreaterThanNumberOfT,

    "appearenceOfOf": checkForAppearenceOfOf,
    "appearenceOfAnd": checkForAppearenceOfAnd,
    "appearenceOfTo": checkForAppearenceOfTo,
    "appearenceOfIn": checkForAppearenceOfIn,
    "appearenceOfZijn": checkForAppearenceOfZijn,
    "appearenceOfDat": checkForAppearenceOfDat,
    "appearenceOfVoor": checkForAppearenceOfVoor,
    "appearenceOfHij": checkForAppearenceOfHij,
    "appearenceOfThe": checkForAppearenceOfThe,
    "appearenceOfAls": checkForAppearenceOfAls,

    "appearenceOfDutchExtraCharacters": checkForAppearenceOfDutchExtraCharacters,
    "startingLetterIsS": checkIfStartingLetterIsSinMostOfTheWordsOfSentence

}


#
def getAppripriateNodes(feature, currentNode):
    left = Node()
    right = Node()

    for lineIndex in currentNode.data:
        words = completeData[lineIndex][3:].split()
        if featureFunctionMapping.get(feature)(words):
            right.data.append(lineIndex)
            if completeData[lineIndex][0] == "n":
                right.dutchExamples.append(lineIndex)
            else:
                right.englishExamples.append(lineIndex)
        else:
            left.data.append(lineIndex)
            if completeData[lineIndex][0] == "n":
                left.dutchExamples.append(lineIndex)
            else:
                left.englishExamples.append(lineIndex)

    return left, right


def calculateSpecialLog(fraction):
    if fraction == 0:
        return 0
    else:
        return math.log(fraction ** -1, 2)


def buildDescisionTree(currentNode: Node, currentFeatureDictionary: dict):
    if len(currentNode.dutchExamples) < 1 or len(currentNode.englishExamples) < 1:
        return
    elif len(currentFeatureDictionary["unused"]) < 1:
        return

    featureEntropyTuple = ("", sys.maxsize)
    leftNodeToBeInserted = None
    rightNodeToBeInserted = None

    for feature in currentFeatureDictionary["unused"]:

        left, right = getAppripriateNodes(feature, currentNode)

        try:
            leftRemainder = 0
            rightRemainder = 0
            if len(left.data) > 0:
                leftRemainder = (len(left.data) / len(currentNode.data)) * (
                        (len(left.englishExamples) / len(left.data)) * calculateSpecialLog(
                    len(left.englishExamples) / len(left.data)) + (
                                len(left.dutchExamples) / len(left.data)) * calculateSpecialLog(
                    len(left.dutchExamples) / len(left.data)))
            if len(right.data) > 0:
                rightRemainder = (len(right.data) / len(currentNode.data)) * (
                        (len(right.englishExamples) / len(right.data)) * calculateSpecialLog(
                    len(right.englishExamples) / len(right.data)) + (
                                len(right.dutchExamples) / len(right.data)) * calculateSpecialLog(
                    len(right.dutchExamples) / len(right.data)))

            remainder = leftRemainder + rightRemainder

            if remainder < featureEntropyTuple[1]:
                featureEntropyTuple = (feature, remainder)
                leftNodeToBeInserted = left
                rightNodeToBeInserted = right
        except Exception as e:
            print(e)

    currentNode.questionToBeAsked = featureEntropyTuple[0]

    currentNode.leftChild = leftNodeToBeInserted
    currentNode.rightChild = rightNodeToBeInserted

    dictionaryForTheChildren = copy.deepcopy(currentFeatureDictionary)
    dictionaryForTheChildren["unused"].remove(featureEntropyTuple[0])
    dictionaryForTheChildren["used"].append(featureEntropyTuple[0])

    buildDescisionTree(currentNode.leftChild, dictionaryForTheChildren)
    buildDescisionTree(currentNode.rightChild, dictionaryForTheChildren)


def initialteSamplesAndWeights(completeData):
    for i in range(len(completeData)):
        sampleWeightArray.append(1 / len(completeData))


def calculateEntropyReductionFotTheStump(stump):

    successfulGuess = 0
    unsuccessfulGuess = 0
    stump.data = range(len(completeData))

    left, right = getAppripriateNodes(stump.questionToBeAsked, stump)
    stump.leftChild = left
    stump.rightChild = right

    leftRemainder = 0
    rightRemainder = 0
    if len(left.data) > 0:
        leftRemainder = (len(left.data) / len(stump.data)) * (
                (len(left.englishExamples) / len(left.data)) * calculateSpecialLog(
            len(left.englishExamples) / len(left.data)) + (
                        len(left.dutchExamples) / len(left.data)) * calculateSpecialLog(
            len(left.dutchExamples) / len(left.data)))
    if len(right.data) > 0:
        rightRemainder = (len(right.data) / len(stump.data)) * (
                (len(right.englishExamples) / len(right.data)) * calculateSpecialLog(
            len(right.englishExamples) / len(right.data)) + (
                        len(right.dutchExamples) / len(right.data)) * calculateSpecialLog(
            len(right.dutchExamples) / len(right.data)))

    return leftRemainder+ rightRemainder




def selectAStump(completeData):

    currentLowestEntropy = sys.maxsize
    bestStump = None

    for key in featureFunctionMapping.keys():
        stump = Node()
        stump.questionToBeAsked = key
        entropy = calculateEntropyReductionFotTheStump(stump)
        if entropy < currentLowestEntropy:
            bestStump = stump
            currentLowestEntropy =  entropy

    return bestStump




def changeTheSampleWeights(sampleWeightArray,totalError,lowestEntropyStump,amountOfSay):

    for sample in lowestEntropyStump.unsuccessfulGuessExampless:
        sampleWeightArray[sample] = sampleWeightArray[sample]*(math.e**amountOfSay)

    for sample in lowestEntropyStump.successfulGuessExamples:
        sampleWeightArray[sample] = sampleWeightArray[sample] * (math.e ** -amountOfSay)

    for i in range(len(sampleWeightArray)):
        sampleWeightArray[i] = sampleWeightArray[i]/sum(sampleWeightArray)








    


def calculateTheErrorProducedByTheStump(lowestEntropyStump : Node):

    if lowestEntropyStump.questionToBeAsked in englishFeatures:
        lowestEntropyStump.successfulGuessExamples += lowestEntropyStump.rightChild.englishExamples + lowestEntropyStump.leftChild.dutchExamples
        lowestEntropyStump.unsuccessfulGuessExampless += lowestEntropyStump.rightChild.dutchExamples + lowestEntropyStump.leftChild.englishExamples

    elif lowestEntropyStump.questionToBeAsked in dutchFeatures:
        lowestEntropyStump.unsuccessfulGuessExampless += lowestEntropyStump.rightChild.englishExamples + lowestEntropyStump.leftChild.dutchExamples
        lowestEntropyStump.successfulGuessExamples += lowestEntropyStump.rightChild.dutchExamples + lowestEntropyStump.leftChild.englishExamples

    totalError = len(lowestEntropyStump.unsuccessfulGuessExampless) / len(lowestEntropyStump.data)
    return totalError





def getTheNewExampleIndex(randomNumber):
    currentlyCumulatedSum = 0
    summ = sum(sampleWeightArray)
    for i in range(len(sampleWeightArray)):
        if randomNumber >=  currentlyCumulatedSum and randomNumber <= currentlyCumulatedSum + sampleWeightArray[i]:
            return i
        currentlyCumulatedSum += sampleWeightArray[i]
    return len(sampleWeightArray)-1

def changeTheCompleteDataArray():
    for i in range(len(completeData)):
        randomNumber = random.random()
        newCompleteData.append( completeData[getTheNewExampleIndex(randomNumber)] )


if learningType == "dt":
    root.isDTnode = "dt"
    buildDescisionTree(root, featureDictionary)
    with open(modelFile, 'wb') as handle:
        pickle.dump(root, handle, protocol=pickle.HIGHEST_PROTOCOL)
else:

    #ada Boost algorithm with 20 stumps
    initialteSamplesAndWeights(completeData)
    for i in range(20):
        lowestEntropyStump = selectAStump(completeData)

        totalError =  calculateTheErrorProducedByTheStump(lowestEntropyStump)

        weightOfTheStump = 0.5*math.log( (1-totalError)/totalError,2)
        lowestEntropyStump.weight = weightOfTheStump


        changeTheSampleWeights(sampleWeightArray,totalError,lowestEntropyStump,weightOfTheStump)

        changeTheCompleteDataArray()

        completeData = newCompleteData.copy()
        newCompleteData.clear()

        print(lowestEntropyStump.questionToBeAsked)
        print(weightOfTheStump)
        finalListOfStumpsForPrediction.append(lowestEntropyStump)

    with open(modelFile, 'wb') as handle:
        pickle.dump(finalListOfStumpsForPrediction, handle, protocol=pickle.HIGHEST_PROTOCOL)
