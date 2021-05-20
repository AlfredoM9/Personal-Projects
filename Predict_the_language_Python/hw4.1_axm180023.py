# Author: Alfredo Mejia
# Class : CS 4395.001
# Date  : 9/16/20
# Descrp: This program follows the instructions given in the description for
# homework 4. The programs reads multiple arguments for file reading. The program
# reads from a file passed through the system arguments and reads in the text.
# New-line characters are removed and the data is tokenize and n-grams are created.
# The dictionary counts are created for unigrams and bigrams and the function returns
# two dictionaries. This is done for 3 different files having 3 different languages.
# These dictionaries are then pickled into their separate file. For this program please
# pass 3 paths to files to be read.

# Imports
from nltk import word_tokenize
from nltk.util import ngrams
import copy
import sys
import pickle


# Descr: This function will accept a valid path to a file to be read. The function
# will remove new-lines and create unigrams and bigrams. After the count dictionaries for
# the unigrams and bigrams will be created and then returned.
def readFile(fileName):
    # Try to read the file
    try:
        file = open(fileName, 'r', encoding='utf-8')
        raw_text = file.read()
        file.close()

    # If unable to read, display error message and exit program
    except OSError:
        sys.exit('An error as occurred. Please make sure the path is correct.')

    # Remove newlines
    text = raw_text.replace('\n', '')

    # Tokenize the text
    tokens = word_tokenize(text)

    print('Please wait. Processing might take a while...')

    # Create a unigrams list (unnecessary in this case but for simplicity and for the hw)
    unigrams = copy.deepcopy(tokens)
    # Create a bigrams list
    bigrams = list(ngrams(tokens, 2))

    # Create dictionary counts for unigrams and bigrams
    unigram_dict = {token: unigrams.count(token) for token in set(unigrams)}
    bigram_dict = {pair: bigrams.count(pair) for pair in set(bigrams)}

    # Return dictionaries
    return unigram_dict, bigram_dict


# Start of program
# Descr: This calls the function to read in the files passed. It then pickles the data returned
# from the function into its own separate file.
if __name__ == '__main__':
    # Check if at least three files are passed. Otherwise display error message and exit program
    if len(sys.argv) < 4:
        sys.exit('Invalid number of arguments')

    # Overall dictionary that is going to hold the two dictionaries based on language
    dict_pickle = {}

    # Iterate over arguments
    for arg in sys.argv:
        # If the argument has train. It means it is a file for training
        if 'train' in arg:
            # Get the language name for this training file
            name = arg.index('train')
            name = arg[name + 6:]
            # Add to the dictionary the sub-dictionaries for this language(name)
            # Function will return the sub-dictionaries
            dict_pickle[name] = readFile(arg)

    # Get the names of languages
    keynames = list(dict_pickle.keys())

    # Iterate over the language names
    for key in keynames:
        # Get the sub-dictionaries for each language
        unigram_dict = dict_pickle[key][0]
        bigram_dict = dict_pickle[key][1]

        # Create the pickle file names for this language and dictionary
        unigram_fileName = key + '_unigram.pickle'
        bigram_fileName = key + '_bigram.pickle'

        # Create pickle files
        with open(unigram_fileName, 'wb') as handle:
            pickle.dump(unigram_dict, handle)

        with open(bigram_fileName, 'wb') as handle:
            pickle.dump(bigram_dict, handle)

    print('Program finished.')

    # end of program
