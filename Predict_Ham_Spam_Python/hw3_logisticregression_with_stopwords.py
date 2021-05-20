# Author: Alfredo Mejia
# Class : CS 6375.001
# Date  : 10/16/20
# Descr : This is logistic regression with stop words. This program follows the instructions given in the assignment 3
#         description. It reads the training files from the spam and ham folder. It then tokenizes each document
#         and forms the vocab of the whole documents. It then creates the data set for each file being the count of each
#         word as an attribute. Gradient ascent is then performed to calculate the weights. Finally, it tests the test
#         files with the weights calculated and outputs the accuracy of the model.

# Imports
import os
import numpy as np
import re


# Descr: Arguments will be weights and the transposed data set. It will calculate P(Y^l = 1 | X^l, W) for each data
#        example. It will use a sigmoid function to calculate the probability. It will then return the a vector (list)
#        of size m (# of files) with the probability of each file.
def sigmoid(weights, data_set):
    # Get the sum of w(i)*x(i) for each file
    dot_product = np.dot(weights, data_set)

    # Create a function to apply the sigmoid function
    funct = lambda dot: 1 / (1 + np.exp(-dot)) if dot >= 0 else np.exp(dot) / (1 + np.exp(dot))

    # Return the list with each value being applied the sigmoid function
    return [funct(value) for value in dot_product]


# Descr: Arguments will be the vocab set, the training data set, the mu value, the lambda value and the number of
#        iterations. This function will only be called in the training method. It will perform gradient ascent and
#        calculate the weights. The weights will be returned.
def get_weights(vocab, data_set, mu_value, lambda_value, iterations):
    # Initialize the weights to some random value
    weights = np.array([0 for i in range(len(vocab) + 1)])

    # Take the transpose of the data set have attributes as rows and the files as columns
    new_data_set = data_set.T

    # For each iteration
    for i in range(iterations):
        # Create a new weight list
        new_weights = []

        # Each weight will have the same (Y^l - P(Y^l = 1 | X^l, W)). This is because the X & Y values don't change and
        # the weights stay the same until the next iteration.
        # This should return the error of each file thus a vector of size m (# of files)
        error = new_data_set[len(new_data_set) - 1] - sigmoid(weights, new_data_set[:-1])

        # For each weight
        for index, single_weight in enumerate(weights):
            # Calculate the dot product between the x(i) corresponding to w(i) and the error
            # This should return the sum of x(i)*(Y^l - P(Y^l = 1 | X^l, W))
            total = np.dot(new_data_set[index], error)

            # Calculate the new weight w(i) + mu * sum - mu * lambda * w(i)
            new_weights.append(single_weight + (mu_value * total) - (mu_value * lambda_value * single_weight))

        # Update the weights
        weights = np.array(new_weights)

    # Return the weights
    return weights


# Descr: Arguments will be a mu value, a lambda value, and the number of iterations. It will read in the training files
#        form the vocab and the training data needed to calculate the weights. The weights are then calculated using
#        gradient ascent using the formula given. The weights and vocab are then returned.
def train(mu_value, lambda_value, iterations):
    # Get file names
    ham_filenames = [str('./train/ham/' + filename) for filename in os.listdir('./train/ham')]
    spam_filenames = [str('./train/spam/' + filename) for filename in os.listdir('./train/spam')]
    total_files = ham_filenames + spam_filenames

    # Create lists needed to keep track of the data
    data_set = []
    words_in_file = []
    vocab = set()

    # Get the vocab
    for file in total_files:
        # Read file and close it
        input_file = open(file, 'r', encoding='utf-8', errors='ignore')
        file_data = input_file.read().lower().strip()
        input_file.close()

        # Tokenize the data
        tokens = file_data.split(' ')
        tokens = [re.findall(r"[\w']+|[.,!?;@#$^&*~()-_]", word) for word in tokens]
        tokens = [item for sublist in tokens for item in sublist]

        # Keep track this file is either ham or spam
        if 'train/ham' in file:
            tokens.insert(0, 0)
        else:
            tokens.insert(0, 1)

        # Append to the list having the data of all files
        words_in_file.append(tokens)

        # Get the set and add it to the vocab
        tokens_set = set(tokens)
        vocab = vocab.union(tokens_set)

    # Construct the data set to be used to calculate the weights
    for file_words in words_in_file:
        # Add 1 for the X0 for every data example
        training_data = [1]

        # For each word in the vocab count the number of times it appears. This is going to be Xn
        for word in vocab:
            training_data.append(file_words.count(word))

        # Lastly add the Y value which we kept track in the previous loop
        training_data.append(file_words[0])

        # Append this list to the total list of data examples
        data_set.append(training_data)

    # Convert to numpy array to faster computation later
    data_set = np.array(data_set)

    # Return the weights and vocab
    return get_weights(vocab, data_set, mu_value, lambda_value, iterations), vocab


# Descr: Arguments will be the weights and the vocab obtained from the training phase. It will test the weights on newly
#        unseen files and classify them as either ham or spam. The results will be outputted. No return value.
def test(weights, vocab):
    # Get file names
    ham_filenames = [str('./test/ham/' + filename) for filename in os.listdir('./test/ham')]
    spam_filenames = [str('./test/spam/' + filename) for filename in os.listdir('./test/spam')]
    total_files = ham_filenames + spam_filenames

    # Create counters to keep track of files classified correctly
    ham_classified_correct = 0
    spam_classified_correct = 0

    # Data from the testing files
    for file in total_files:

        # Read the file and then close the file
        input_file = open(file, 'r', encoding='utf-8', errors='ignore')
        file_data = input_file.read().lower().strip()
        input_file.close()

        # Tokenize the data
        tokens = file_data.split(' ')
        tokens = [re.findall(r"[\w']+|[.,!?;@#$^&*~()-_]", word) for word in tokens]
        tokens = [item for sublist in tokens for item in sublist if item]

        # Create the data set for the file
        training_data = [1]
        for word in vocab:
            training_data.append(tokens.count(word))

        # Calculate the probability
        pred_class = np.dot(training_data, weights)

        # If file correctly classified, add one to the appropriate counter
        if 'test/ham' in file and pred_class <= 0:
            ham_classified_correct += 1
        elif 'test/spam' in file and pred_class > 0:
            spam_classified_correct += 1

    # Print the results
    print('\nHam:\nTotal Docs: ' + str(len(ham_filenames)) + '\nClassified Correctly: ' + str(
        ham_classified_correct) + '\nAccuracy: ' + str(ham_classified_correct / len(ham_filenames)))
    print('\nSpam:\nTotal Docs: ' + str(len(spam_filenames)) + '\nClassified Correctly: ' + str(
        spam_classified_correct) + '\nAccuracy: ' + str(spam_classified_correct / len(spam_filenames)))
    print('\nAll Files:\nTotal Docs: ' + str(len(spam_filenames) + len(ham_filenames)) + '\nClassified Correctly: ' +
          str(spam_classified_correct + ham_classified_correct) + '\nAccuracy: ' +
          str((spam_classified_correct + ham_classified_correct) / (len(spam_filenames) + len(ham_filenames))))


# Descrp: Main function. This function will call the train method with different lambda values and then test the model.
def main():
    # Initialize parameters
    lambda_values = [0.1, 0.05, 0.03, 0.01, 0.001]
    mu_value = 0.05
    iterations = 100

    print('\nWith Stop Words: \n')

    # Train and test with different lambda values. Test will output the results
    for lam_val in lambda_values:
        print('\nPrinting accuracy for lamda value: ' + str(lam_val) + '\n')
        weights, vocab = train(mu_value, lam_val, iterations)
        test(weights, vocab)

    # Program takes a couple minutes

# Starting point of the program
if __name__ == '__main__':
    main()
