# -*- coding: utf-8 -*-
"""CS471Assignment3-MillerApril.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Tr-o2qoDj8X6xC6iobl_KumGr2T0DqZd
"""

import numpy as np
from collections import defaultdict
import string

#Step one: Load the dataset and split into training and testing sets (first 20 into training and the rest into testing)
dataset = np.genfromtxt('SpamDetection.csv', delimiter=',', dtype=None, names=True, encoding='utf-8')

trainingSet = dataset[:20]
testingSet = dataset[20:30]

#Step two: Compute the prior probabilities: P(spam) and P(ham)

for entry in trainingSet:
  spamCount = sum(1 for item in trainingSet if item[0] == 'spam')
  hamCount = sum(1 for item in trainingSet if item[0] == 'ham')

trainingSetLength = len(trainingSet)

pSpam = spamCount/trainingSetLength
pHam = hamCount/trainingSetLength

#Step three: Compute the conditional probabilities P(sentence/spam)

spamWordCounts = defaultdict(int)
hamWordCounts = defaultdict(int)

#Count how many times a word is in a class.
for label, phrase in trainingSet:
    words = phrase.split()
    if label == "spam":
        for word in words:
          spamWordCounts[word] += 1
    else:
        for word in words:
         hamWordCounts[word] += 1

totalSpamWords = sum(spamWordCounts.values())
totalHamWords = sum(hamWordCounts.values())

uniqueWords = set()

#Clean the string and make a set of all the unique words
for label, phrase in dataset:
    cleanedPhrase = phrase.lower().translate(str.maketrans('', '', string.punctuation))
    words = cleanedPhrase.split()
    uniqueWords.update(words)

totalWords = totalSpamWords + totalHamWords

#Laplace smoothing numerator and denominator
laplaceNumer = 1
laplaceDenom = len(uniqueWords)

#Function to compute probability of a word being in a sentence given its class
def compute_conditional_probability(word, label):
  if label == "spam":
    return ((spamWordCounts[word] + laplaceNumer) / (totalSpamWords + laplaceDenom))
  else:
    return ((hamWordCounts[word] + laplaceNumer) / (totalHamWords + laplaceDenom))

#Helper function to multiply numbers in a list
def multiply(lis):
  product = 1
  for i in lis:
    product *= i

  return product

#Step four: Compute the posterior probabilities (probability of a sentence belonging to a spam or ham)

correctPredictions = 0

#Calculate the probability of a sentence belonging to spam or ham
for trueLabel, sentence in testingSet:

  #Split the sentences into words
  wordsList = sentence.split()

  #Probability that sentence is spam or ham
  pSentenceGivenSpam = pSpam * multiply(compute_conditional_probability(word, "spam") for word in wordsList)
  pSentenceGivenHam = pHam * multiply(compute_conditional_probability(word, "ham") for word in wordsList)

  #Make a prediction based off of which one has a higher probability
  if pSentenceGivenSpam > pSentenceGivenHam:
    predictedLabel = "spam"
  else:
    predictedLabel = "ham"

  #If the prediction is correct, increment the counter of correct predictions
  if predictedLabel == trueLabel:
    correctPredictions += 1

  #Print the results
  print("Sentence | " + sentence)
  print("P(sentence|spam) | " + str(pSentenceGivenSpam))
  print("P(sentence|ham) | " + str(pSentenceGivenHam))
  print("Prediction | " + predictedLabel)
  print("Actual | " + trueLabel)
  print("----------------------------------------------------\n")

#Calculate the accuracy
totalSentencesCount = len(testingSet)
accuracy = correctPredictions/totalSentencesCount

print("Accuracy | " + str(accuracy))