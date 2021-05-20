# Author: Alfredo Mejia
# Class : CS 4395.001
# Date  : 9/16/20
# Descrp: This program follows the instructions given in the description for
# homework 4. The program accepts two arguments. The testing data (file) and
# the correct results (file). If incorrect number of arguments passed an error
# will appear and the program will terminate. The program first loads the dictionaries
# from the pickle files into a overall dictionary with the key being its language.
# The test data is then read and each line corresponds to one data point so it is split
# on newline characters. Then the probability of that data point being a specific language
# is  calculated using Laplace smoothing. The calculated language is written to file. Then
# the accuracy is computed by comparing the testing results with the actual correct results.
# The accuracy is then printed as per the hw4 description.


# Imports
import pickle
import os
import re
import sys
from nltk import word_tokenize
from nltk.util import ngrams


# Descr: Reads a file as test data. If unable to open the file, an error will be displayed,
# and the program will be terminated. Each line represents a data point so the data will be split
# on new lines and the data will then be returned.
def readTestData():
    # Try to open and read the file
    try:
        file = open(sys.argv[1], 'r', encoding='utf-8')
        raw_text = file.read()
        file.close()

    # If unable to read/open, display error, exit program
    except OSError:
        sys.exit('An error as occurred. Please make sure the path is correct.')

    # Split on newlines and get rid of last element (empty)
    data = raw_text.split('\n')
    data = data[:-1]

    # Return list
    return data


# Descr: This function accepts the line(text), the unigram and bigram for that language, and the
# total size of the 3 unigram dictionaries. It will calculate the probability using Laplace smoothing
# as described in the hw and github.
def compute_prob(line, unigram_dict, bigram_dict, total_unigram_size):
    # Create n-grams for the test data
    unigrams_test = word_tokenize(line)
    bigrams_test = list(ngrams(unigrams_test, 2))

    # Initialize probability
    p_laplace = 1

    # For each bigram in the test data
    for bigram in bigrams_test:
        # Get the bigram count in the language bigram
        b = bigram_dict[bigram] if bigram in bigram_dict else 0
        # Get the unigram count in the language using the first word of the bigram of the test data
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        # Calculate probability
        p_laplace = p_laplace * ((b + 1) / (u + total_unigram_size))

    # Return probability
    return p_laplace


# Descr: This function will read from two files. One file holds the correct classifications and
# the other holds the calculated classification. The program will compare the two files and determine
# the accuracy of the calculated classification depending on the correct classifications. The percentage
# of correctness will be outputted.
def compute_accuracy():
    # Try to open the files (correct classification file and calculated classification file)
    try:
        file_correct = open(sys.argv[2], 'r', encoding='utf-8')
        file_created = open('TestResults.txt', 'r')
        correct_results = file_correct.read()
        test_results = file_created.read()
        file_correct.close()
        file_created.close()

    # Otherwise, display error, and terminate program
    except OSError:
        sys.exit('An error as occurred. Please make sure the path is correct.')

    # Split the data and get rid of last element (empty)
    correct_results = correct_results.split('\n')
    test_results = test_results.split('\n')
    correct_results = correct_results[:-1]
    test_results = test_results[:-1]

    # Get rid of everything besides only the string containing the language
    regex = re.compile('[^a-zA-Z]')
    correct_results = [regex.sub('', result).lower() for result in correct_results]
    test_results = [regex.sub('', result[4:]).lower() for result in test_results]
    test_results = [result[:-1] for result in test_results]

    # Initialize variables to do calculated
    total_results = len(correct_results)
    total_correct = 0
    incorrect_lines = []
    counter = 1

    # For every line in the results
    for correct_r, test_r in zip(correct_results, test_results):
        # If the strings equal each other, add to total correct
        if correct_r == test_r:
            total_correct += 1

        # Otherwise keep track of the lines being wrong
        else:
            incorrect_lines.append(counter)

        counter += 1

    # Print findings/calculations
    print('Accuracy: ' + str(total_correct) + ' classified correctly out of ' + str(total_results))
    print('Percentage: ' + '%.2f' % ((total_correct / total_results) * 100) + ' %')
    print('Lines misclassified: ' + str(incorrect_lines))


# Start of program
# Descr: Verifies the correct number of arguments is passed. Gets the data from the pickle files.
# Reads in the test data and calculates every data point and its probability of its language. The
# predicted language and percentage is written to a file and a function is called to check its accuracy.
if __name__ == '__main__':
    # If incorrect number of arguments, display error message, and exit program.
    if len(sys.argv) != 3:
        sys.exit('Invalid number of arguments.')

    # Retrieve all the files in the current directory
    dirs = os.listdir(os.getcwd())

    # If pickle files are found extract the names
    dirs = [fileName for fileName in dirs if 'pickle' in fileName]

    # Convert the name to include dict to show which language corresponds to which dictionary
    dict_names = [name.replace('.pickle', '_dict').lower() for name in dirs]

    # An overall dictionary with the key being the language and type of dictionary
    # And the value being a sub-dictionary of the counts
    all_dicts = {}

    # For each pickle extract it and add the dictionary to the overall dictionary
    for pickle_file, dict_name in zip(dirs, dict_names):
        with open(pickle_file, 'rb') as handle:
            all_dicts[dict_name] = pickle.load(handle)

    # Read the test data
    test_data = readTestData()

    # Separate the keys from dict_names to specific unigram keys and bigrams keys to help us later do computations
    unigram_names = [uni_name for uni_name in dict_names if 'unigram' in uni_name]
    bigram_names = [bi_name for bi_name in dict_names if 'bigram' in bi_name]

    # Total size of 3 unigram dictionaries
    total_unigram_size = 0

    # For every key corresponding to a unigram dictionary
    # Add the size of that unigram dictionary
    for unigram in unigram_names:
        total_unigram_size += len(all_dicts[unigram])

    # Open a file to write results to
    file = open('TestResults.txt', 'w')
    counter = 1

    # For every data point (line)
    for line in test_data:
        # Dictionary to hold probabilities for each language
        probabilites = {}

        # For each language
        for unigram, bigram in zip(unigram_names, bigram_names):
            # Get the language name
            name = unigram.replace('_unigram_dict', '')

            # Add the key as the language name and call the function to get the probability for that data point
            # Using the unigram and bigram from the language currently being used. Also pass total unigram size.
            probabilites[name] = compute_prob(line, all_dicts[unigram], all_dicts[bigram], total_unigram_size)

        # Get the highest probability for this line
        max_prob = max(probabilites.values())
        # Identify the key for this probability
        max_key = [k for k, v in probabilites.items() if v == max_prob]

        # Write to the file what line it is, the language, and the probability
        file.write('Line ' + str(counter) + ': ' + str(max_key[0]) + ' ' + str(format(max_prob, '.2e')) + '\n')
        counter += 1

    # Close file
    file.close()

    # Calculate and display accuracy
    compute_accuracy()

    # end of program
