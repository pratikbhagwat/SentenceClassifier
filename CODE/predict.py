
import math
import pickle
import sys

if len(sys.argv) >1:
    modelFile = sys.argv[1]
    testingFile = sys.argv[2]
else:
    modelFile = input("Enter the model file")
    testingFile = input("Enter the testing file")

class Node:

    def __init__(self):
        self.leftChild = None
        self.rightChild = None
        self.data = []  # this will be the list of index of the example in the dataset
        self.dutchExamples = []
        self.englishExamples = []
        self.questionToBeAsked = None
        self.successfulGuessExamples = []
        self.unsuccessfulGuessExampless = []
        self.weight = None


with open(modelFile, 'rb') as handle:
    rootLoaded = pickle.load(handle)

root = rootLoaded


englishFeatures = ["appearenceOfThe", "appearenceOfOf",
                   "appearenceOfAnd",
                   "appearenceOfTo",
                   "appearenceOfIn", "startingLetterIsS", "numberOfNAndT"]

dutchFeatures = ["wordSize",
                 "averageWordSize", "appearenceOfAls", "appearenceOfZijn",
                 "appearenceOfDat",
                 "appearenceOfVoor",
                 "appearenceOfHij", "appearenceOfDutchExtraCharacters"]










def checkIfStartingLetterIsSinMostOfTheWordsOfSentence(wordListOfSentence:list):
    numberOfWordsStartingWithS = 0
    numberOfWordsStartingWithOtherThanS = 0

    for word in wordListOfSentence:
        if word[0].lower() == "s":
            numberOfWordsStartingWithS+=1
        else:
            numberOfWordsStartingWithOtherThanS+=1

    return numberOfWordsStartingWithS > numberOfWordsStartingWithOtherThanS






def checkForAppearenceOfDutchExtraCharacters(wordListOfSentence : list):

    for word in wordListOfSentence:
        for letter in word.lower():
            if letter in "éëïóöü":
                return True

    return False



def checkForAverageWordSize(wordListOfSentence: list , averageWordSize = 5):

    wordSizeSum = 0
    for word in wordListOfSentence:
        wordSizeSum += len(word)

    if ( wordSizeSum/len(wordListOfSentence) ):
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


def checkIfSentenceContainsWordOfSizeGreaterThanGivenSize(wordListOfSentence: list,  wordLength = 9 ):
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


featureFunctionMapping = {
    "wordSize": checkIfSentenceContainsWordOfSizeGreaterThanGivenSize,
    "averageWordSize" : checkForAverageWordSize,
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

    "appearenceOfDutchExtraCharacters" : checkForAppearenceOfDutchExtraCharacters,
    "startingLetterIsS" : checkIfStartingLetterIsSinMostOfTheWordsOfSentence

}


def traverseAndDetect(stringToBeDetected: str, node: Node):

    if node.questionToBeAsked:

        if featureFunctionMapping.get(node.questionToBeAsked)(stringToBeDetected.split()):
            if node.rightChild:
                return traverseAndDetect(stringToBeDetected, node.rightChild)
            else:
                if len(node.englishExamples) > len(node.dutchExamples):
                    return "en"
                else:
                    return "nl"
        else:
            if node.leftChild:
                return traverseAndDetect(stringToBeDetected, node.leftChild)
            else:
                if len(node.englishExamples) > len(node.dutchExamples):
                    return "en"
                else:
                    return "nl"
    else:
        if len(node.englishExamples) > len(node.dutchExamples):
            return "en"
        else:
            return "nl"


fpTestingData = open(testingFile,"r")

completeData = fpTestingData.readlines()



if type(root) == Node:

    successfulExamples = 0
    unsuccessfulExamples = 0
    for line in completeData:
        answer = traverseAndDetect(line[3:] , root)

        if line[0] == answer[0]:
            successfulExamples+=1
        else:
            unsuccessfulExamples+=1

        print(answer)

    # uncomment this to see the accuracy
    print("******************************************")
    print((successfulExamples/(successfulExamples+unsuccessfulExamples))*100)

else:
    successfulExamples = 0
    unsuccessfulExamples = 0
    for line in completeData:
        sumOfTheDescision = 0
        for stump in root:#now root is a list of stumps
            if stump.questionToBeAsked in englishFeatures:
                if featureFunctionMapping.get(stump.questionToBeAsked)(line[3:].split()):
                    sumOfTheDescision+= 1 * stump.weight
                else:
                    sumOfTheDescision+= -1*stump.weight
            else:
                if featureFunctionMapping.get(stump.questionToBeAsked)(line[3:].split()):
                    sumOfTheDescision += -1*stump.weight
                else:
                    sumOfTheDescision += 1*stump.weight
        if sumOfTheDescision>0:
            print("en")
            if line[0] == "e":
                successfulExamples+=1
            else:
                unsuccessfulExamples+=1
        else:
            print("nl")
            if line[0] == "n":
                successfulExamples+=1
            else:
                unsuccessfulExamples+=1

    # uncomment this to see the accuracy
    print("******************************************")
    print((successfulExamples/(successfulExamples+unsuccessfulExamples))*100)