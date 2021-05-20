# Author: Alfredo Mejia
# Class : CS 6375.001
# Date  : 10/14/20
# Descr : This is naive bayes with stop words. This program follows the instructions given in the assignment 3
#         description. It reads the training files from the spam and ham folder. It then tokenizes each document
#         and forms a dictionary containing the count of the word in each class. At the same time, the vocab of the
#         training files is formed. After, the prior probability is calculated and the conditional probability of the
#         term is calculated. Then the testing phase begins. In the testing phase, it reads from the testing folder and
#         uses naive bayes to calculate the probability of each class. Whichever one is higher is the class that the
#         program has predicted for the doc. The results are then outputted.


# Imports
import os
import math
import operator
import collections
import re


# Descr: This is the training phase. Input are the classes available. The function grabs the necessary documents and
# forms the vocab. From the vocab it calculates the probability of that term given a class. It then returns the vocab,
# the prior probability and the conditional probability based on the vocab. This is done with stop words.
def train(classes):
    # Get the paths for the training files
    ham_filenames = [str('./train/ham/' + filename) for filename in os.listdir('./train/ham')]
    spam_filenames = [str('./train/spam/' + filename) for filename in os.listdir('./train/spam')]
    total_files = ham_filenames + spam_filenames

    # Count the number of times a word appears in ham or spam
    word_count = {'ham': {}, 'spam': {}}

    # Count the total number of words inside each class
    class_total_word_count = {'ham': 0, 'spam': 0}

    # Create empty voacb
    vocab = set()

    # For each file either spam or ham
    for file in total_files:
        # Check what class is it
        if 'train/ham' in file:
            doc_class = 'ham'
        else:
            doc_class = 'spam'

        # Read the file and close it
        input_file = open(file, 'r', encoding='utf-8', errors='ignore')
        file_data = input_file.read().lower().strip()
        input_file.close()

        # Tokenize the document
        tokens = file_data.split(' ')
        tokens = [re.findall(r"[\w']+|[.,!?;@#$^&*~()-_]", word) for word in tokens]
        tokens = [item for sublist in tokens for item in sublist]

        # Add the number of words in this file to the total
        class_total_word_count[doc_class] = class_total_word_count[doc_class] + len(tokens)

        # For each word in the tokens
        for word in tokens:
            # If the word was counted already then simply add one
            if word in word_count[doc_class].keys():
                word_count[doc_class][word] = word_count[doc_class][word] + 1

            # If the word wasn't counted initialize it to one
            else:
                word_count[doc_class][word] = 1

        # Get the set of the tokens and add it to the vocab
        tokens_set = set(tokens)
        vocab = vocab.union(tokens_set)

    # Create dictionary with the len of docs (files) of each class
    doc_class_count = {'ham': len(ham_filenames), 'spam': len(spam_filenames)}

    # Create dictionary for the prior probability
    prior = {}

    # Create a nested dictionary for the probabilities of each word given a class
    cond_prob = collections.defaultdict(dict)

    # For each class
    for doc_class in classes:
        # Calculate the prior
        prior[doc_class] = doc_class_count[doc_class] / len(total_files)

        # For each word in the vocab
        for term in vocab:
            # If the word appears in the word count of this class then get the term frequency in this class
            if term in word_count[doc_class].keys():
                term_count = word_count[doc_class][term]

            # Otherwise it is zero
            else:
                term_count = 0

            # Calculate the probability of this term given the class
            cond_prob[term][doc_class] = (term_count + 1) / (class_total_word_count[doc_class] + len(vocab))

    # Return the vocab, priors, and the conditional probabilities
    return vocab, prior, cond_prob


# Descr: This is the training phase. It accepts the vocab, prior, conditional probabilities, and the classes.
# It grabs the necessary documents and gets the tokens from each document. It then calculates the probability of the
# doc using naive bayes with only the tokens inside the vocab and the cond_probability for the token given a certain
# class. The results are then outputted.
def test(vocab, prior, cond_prob, classes):
    # Get the files to test
    ham_filenames = [str('./test/ham/' + filename) for filename in os.listdir('./test/ham')]
    spam_filenames = [str('./test/spam/' + filename) for filename in os.listdir('./test/spam')]
    total_files = ham_filenames + spam_filenames

    # Create dictionary to count the amount of correctly classified documents
    classified_correctly = {'ham': 0, 'spam': 0}

    # For each file
    for filename in total_files:
        # Check which class it belongs
        if 'test/ham' in filename:
            correct_class = 'ham'
        else:
            correct_class = 'spam'

        # Create a dictionary to hold the probabilities
        score = {}

        # Read the file and close it
        input_file = open(filename, 'r', encoding='utf-8', errors='ignore')
        file_data = input_file.read().lower().strip()
        input_file.close()

        # Get the words and symbols of the document
        tokens = file_data.split(' ')
        tokens = [re.findall(r"[\w']+|[.,!?;@#$^&*~()-_]", word) for word in tokens]
        tokens = [item for sublist in tokens for item in sublist if item in vocab]

        # For each class
        for doc_class in classes:
            # Get the probability of each class by starting with the prior
            score[doc_class] = math.log10(prior[doc_class])

            # For each word in the doc get the probability add it to the score
            for word in tokens:
                score[doc_class] = score[doc_class] + math.log10(cond_prob[word][doc_class])

        # Get the max probability and return the class
        pred_class = max(score.items(), key=operator.itemgetter(1))[0]

        # If the predidcted class equals the correct then add one to the total classified correctly
        if pred_class == correct_class:
            classified_correctly[pred_class] = classified_correctly[pred_class] + 1

    # Print the results
    print('\nHam:\nTotal Docs: ' + str(len(ham_filenames)) + '\nClassified Correctly: ' + str(
        classified_correctly['ham']) + '\nAccuracy: ' + str(classified_correctly['ham'] / len(ham_filenames)))
    print('\nSpam:\nTotal Docs: ' + str(len(spam_filenames)) + '\nClassified Correctly: ' + str(
        classified_correctly['spam']) + '\nAccuracy: ' + str(classified_correctly['spam'] / len(spam_filenames)))
    print('\nAll Files:\nTotal Docs: ' + str(len(spam_filenames) + len(ham_filenames)) + '\nClassified Correctly: ' +
          str(classified_correctly['ham'] + classified_correctly['spam']) + '\nAccuracy: ' +
          str((classified_correctly['ham'] + classified_correctly['spam']) /
              (len(spam_filenames) + len(ham_filenames))))


# Main function
def main():
    # Create class
    classes = ['ham', 'spam']
    print('With Stop Words:')

    # Call training and testing phases
    vocab, prior, cond_prob = train(classes)
    test(vocab, prior, cond_prob, classes)


# Starting point of program
if __name__ == '__main__':
    main()
