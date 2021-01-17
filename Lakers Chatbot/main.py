""""********************************************************************************************************************
Author: Alfredo Mejia
Date  : 11/1/20
Descrp: This program is an implementation of a very simple and naive chatbot. This chatbot has a domain knowledge around
        the Los Angeles Lakers and can only speak regarding that subject. At times, the chatbot answers perfectly at
        other times not so much. This program uses a lot of techniques discussed in class from tokenization, POS
        tagging, term count, tfidf, and machine learning. The chatbot works like  this. It introduces itself and gets
        the information of the user. The user information is stored and then allows the user the freedom to type
        anything. The program uses rule based and ML to determine if it is a question, if so it tries to answer it by
        doing cosine similarity between the query and the knowledge base. It returns the most common sentence. If the
        input is not a question, then it determines if it is a command using rule based, if so it tries to do that
        command by treating it as a question. Otherwise, it performs sentiment analysis using ML to determine if its an
        opinion that is negative or positive of the user. It then stores it with the connotation and replies to it. The
        process then repeats until the user enters a command that makes it exit.

        Note: You might have to have some things downloaded first to get this program to work.
              For example, nltk.download('twitter_samples') must have been prior to running this program.
              If any error occurs, please feel free to contact me or download the necessary files.
***********************************************************************************************************************
Possible Questions:
1) Who are the Los Angeles Lakers?
2) Who is Kobe Bryant?
3) Tell me who did the lakers draft in 2017
4) Who is the owner of the Lakers?
5) Who did the lakers play against in the 2020 nba finals?
6) How many championships do the lakers have?
7) What is the longest streak of the lakers?
8) How did the lakers get Wilt Chamberlain?
9) What are the colors of the lakers?
10) What does showtime mean for the lakers?
*********************************************************************************************************************"""
# Imports
from sql_helper import create_table, create_connection, get_db_data
import sys
import spacy
import random
import pandas as pd
import wikipedia
import nltk
import numpy as np
import re
import pickle
import string
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import NaiveBayesClassifier


"""
Args : Prompt(string)
Retur: answer(string)
Descr: This function is a helper function. It asks a question given to it and expects to receive a "yes" or "no" answer.
       If it does not, it will ask again for a yes or no answer.
"""
def binary_question(prompt):
    # Get input
    answ = input(prompt).strip().lower()

    # While not yes or no, repeat
    while 'yes' != answ and 'no' != answ:
        print("I don't really understand you. Please answer it in a yes or no format.")
        answ = input(prompt).lower()

    # Return results
    return "yes" if 'yes' in answ else "no"


"""
Args : None
Retur: username(string)
Descr: This function will introduce the bot and will store some information about the user such as the name and if the
       user is a Laker fan in a DB file. If the user is returning then the chatbot might ask other questions, like if
       the user has changed their mind in becoming a Laker fan (if they haven't said yes).
"""
def introduction():
    # Print a random greeting
    greetings = ("What's up.", "Hello.", "Bleep-Blop.", "What's good my friend.", "Hey.",
                 "I guess I gotta come to work again. Ugh.", "Greetings.", "HIIIII!!!!!!!", "Just like any other day.",
                 "LET'S GO LAKERS.", "ONE TWO THREE ACTION!", "Hi.")
    print(random.choice(greetings))

    # Print the intro
    intro = "My name is LA-BOT or call me LT for short. I am a chatbot that talks about the Los Angeles Lakers. If you " \
            "tell something that is not about the Lakers I might just say some random stuff. Also keep in mind, " \
            "I am just a new born so forgive me for not understanding you at times. However, you can simply just type " \
            "anything from questions to remarks, I'll try my best to understand you. \nTell me what is your name?"
    print(intro)

    # Store the username
    user_name = input().strip().split(" ")[0].lower()

    # If the username is empty then try again.
    while not user_name:
        user_name = input("No empty names allowed. ").strip().split(" ")[0].lower()

    # Create a database to store users
    db_name = "users.db"
    tb_name = db_name[:-3]
    db_conn = create_connection(db_name)

    if db_conn is None:
        sys.exit("Error! Cannot create the database connection")

    # Create table to store users. The columns are the username (string) which is the unique key and fan (string) which
    # shows if the user is a fan or not.
    create_table_query = "CREATE TABLE IF NOT EXISTS " + str(tb_name) + "(username text PRIMARY KEY, " \
                                                                        "fan text NOT NULL);"
    create_table(db_conn, create_table_query)

    # Get any data stored
    data = get_db_data(db_conn, tb_name)
    in_db = False

    # Possible responses, if the person is not a fan or is a fan
    responses = {"yes": ["Sweet!", "AHHH YEAHH!!", "I hope you aren't a bandwagon.", "Are you just saying that to"
                                                                                     " make me feel better? Wait do I "
                                                                                     "feel?",
                         "YEAH! The LAKERS are the BEST!"],
                 "no": ["You can't be serious.", "I respect your honestly.", "WHAT?! The Lakers are the best.",
                        "Well I guess it's now my job to convince to become a fan."]}

    # If there is a user in the table
    for user in data:
        # Find the user with the same username
        if user[0] == user_name:
            in_db = True

            # Welcome them back
            print(user_name.capitalize() + "!!! Welcome back. Glad you're here.")

            # If they weren't a fan previously, ask if they have changed their mind
            if user[1] == "no":
                # Ask the question
                answ = binary_question("Have you changed your mind of becoming a Lakers fan? ")

                # Print a response based on the answer
                print(random.choice(responses[answ.lower()]))

                # If they answered yes then update the DB file with the user info
                if answ.lower() == "yes":
                    update_query = "UPDATE " + str(tb_name) + " SET fan=? WHERE username=?"
                    cur = db_conn.cursor()
                    cur.execute(update_query, ("yes", user_name))
                    db_conn.commit()

    # If the user is not the database
    if not in_db:
        # Ask if they are a Laker fan
        answ = binary_question("So, " + user_name.capitalize() + " are you a fan of the Los Angeles Lakers? ")
        # Print response based on the answer
        print(random.choice(responses[answ.lower()]))

        # Insert new user into the db file
        sql = "INSERT INTO " + str(tb_name) + "(username, fan) VALUES(?,?)"
        cur = db_conn.cursor()
        cur.execute(sql, (user_name, answ))
        db_conn.commit()

    # Print message to continue conversation
    print("But anyhow, let's do it! Ask or tell me anything regarding the Lakers. Type exit, bye, quit or goodbye to "
          "end the convo.")

    db_conn.close()

    # Return username to later use for another DB file to store their likings/dislikings
    return user_name


"""
Args : user_input(string)
Retur: is_question(boolean)
Descr: This is a helper function to getInput. Not all questions will follow a format, so this function will use ML
       to predict if it is a question or not. 
"""
def predict_is_question(user_input):
    # Create DF with the user input
    test_df = pd.DataFrame([user_input], columns=['test'])

    # Create DF with the training data that is positive (is question)
    file = open("train_question_positive.txt", "r", encoding='UTF-8')
    train_pos_data = file.readlines()
    train_pos_data = [sent.strip() for sent in train_pos_data]
    trn_pos_df = pd.DataFrame(train_pos_data, columns=['sent'])
    trn_pos_df['label'] = [1 for sent in train_pos_data]

    # Create DF with the training data that is negative (not question)
    file = open("train_question_negative.txt", "r", encoding='UTF-8')
    train_neg_data = file.readlines()
    train_neg_data = [sent.strip() for sent in train_neg_data]
    trn_neg_df = pd.DataFrame(train_neg_data, columns=['sent'])
    trn_neg_df['label'] = [0 for sent in train_neg_data]

    # Combine the data set
    frames = [trn_pos_df, trn_neg_df]
    trn_data_df = pd.concat(frames, ignore_index=True, sort=False)

    # Get the features and the labels
    sentences = trn_data_df['sent'].values
    y = trn_data_df ['label'].values

    # Vectorize the training data and the test data
    vectorizer = CountVectorizer()
    vectorizer.fit(sentences)
    X_train = vectorizer.transform(sentences)
    X_test = vectorizer.transform(test_df['test'].values)

    # Train the model on the train data
    classifier = LogisticRegression()
    classifier.fit(X_train, y)

    # Predict the user_input
    prob = classifier.predict_proba(X_test[0])[0][1]

    # If high probability then is_question = true
    if prob >= 0.7:
        return True

    # If probability is near half then ask just to be sure.
    elif prob < 0.7 and prob >= 0.60:
        clarify = binary_question("Sorry. I can figure out if it's a question or not. Is it? ")
        return True if clarify == "yes" else False

    # Otherwise it is not a question
    else:
        return False


"""
Args : user_input(string)
Retur: is_question(boolean) and user_input (string)
Descr: This function will get the input from the user. It will then determine if it is a question or not.
"""
def getInput():
    # Get user input
    user_input = input().strip().lower()

    # Load the spacy model and get more info regarding the input
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(user_input)

    count = 0
    is_question = False
    w_count = -1000

    # For each word in the user_input
    for token in doc:
        # Is it a w tag such as WHAT,WHO,HOW,etc.
        if 'W' in token.tag_:
            w_count = count
        # Does a v tag follow a w tag, if so then it is a question
        if 'V' in token.tag_ and w_count == count - 1:
            is_question = True
        count += 1

    # If the statement didn't follow the structure
    if not is_question:
        # Use ML to predict if it is a question
        is_question = predict_is_question(user_input)

    # Return boolean saying if it is a question and return user input
    return is_question, user_input


"""
Args : user_input(string)
Retur: (term, term count) List of tuples and a knowledge base (list of strings)
Descr: This a helper function to get_answer(). This function will get the knowledge base and get the relevant terms of
       query that is related to the lakers.
"""
def is_laker_related(user_input):
    # Get raw data about the lakers
    raw_data = wikipedia.page('lakers')
    raw_data = raw_data.content

    # Process the data and retrieve the words and sentences
    tokens = nltk.word_tokenize(raw_data)
    sent_tokens = nltk.sent_tokenize(raw_data)
    sent_tokens = [sent.replace("\n", " ").replace("\t", " ").replace("==", "").lower() for sent in sent_tokens]

    # Further process the words and the words inside the user input
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word not in stopwords.words('english') and word.isalnum()]
    user_tokens = nltk.word_tokenize(user_input)
    user_tokens = [lemmatizer.lemmatize(word.lower()) for word in user_tokens if word not in stopwords.words('english')]


    term_count = []
    relevant = False

    # Check if the words in the query match with the ones in the knowledge base, if so keep track of how many.
    for word in user_tokens:
        if tokens.count(word) > 0:
            term_count.append((word, tokens.count(word)))
            relevant = True

    # If there are no relevant words
    if not relevant:
        # Return empty list and knowledge base
        return [], sent_tokens

    # Otherwise
    else:
        # Sort the list to get the most relevant in the beginning and return it along with the knowledge base
        return sorted(term_count, key=lambda x:-x[1]), sent_tokens


"""
Args : user_input(string)
Retur: response(string)
Descr: This function will try and answer the question asked. It will first get the relevant terms in the query and the 
       knowledge base. It will check if the query is laker related, if so then cosine similarity will be performed with
       each sentence in the knowledge base and the query. The closest sentence to the query will be returned. 
"""
def get_answer(user_input):
    # Get relevant terms in the query and the knowledge base
    relevant_terms, lakers_kb = is_laker_related(user_input)

    # If no relevant terms then the query might not be laker related
    while len(relevant_terms) <= 0:
        # Get input again
        user_input = input("Are you sure this is Laker related? If so, please ask the question one more time in a "
                           "simpler way. ").strip().lower()

        # If not a question then exit
        if "no" in user_input:
            return "No worries then. Let's continue."

        # Repeat
        relevant_terms, lakers_kb = is_laker_related(user_input)

    # Sentence tokenize the knowledge base and fit it into a TfidfVectorizer
    sent_tokens = lakers_kb + nltk.sent_tokenize(user_input)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_docs = tfidf_vectorizer.fit_transform(sent_tokens)

    # Perform cosine similarity the user input with the rest of documents (sentences)
    arry = cosine_similarity(tfidf_docs[-1], tfidf_docs)

    # Flatten the array and get the index with the closest similarity
    arry = arry.flatten()
    index = np.where(arry == np.max(arry[:-1]))[0][0]

    sent_relevant = False

    # For each relevant term at least one has to be inside the response
    for term in relevant_terms:
        if term[0] in sent_tokens[index]:
            sent_relevant = True

    # Otherwise, the response was not relevant and return message
    if not sent_relevant:
        responses = ["Sorry. I don't know how to answer that.", "Who do you think I am? I'm not that smart. At least "
                     "not yet.", "Dang. I don't know the answer.", "Thinking...brain exploded...sorry I don't know the "
                     "answer", "Umm...well good luck with that because I don't know the answer.", "Did I ever tell you "
                     "I'm just a few days old? Well I don't have the knowledge to answer."]
        return random.choice(responses)

    # Return most closest sentence
    return sent_tokens[index]


"""
Args : user_id (string), user_input(string), remark_model(NaiveBayesClassifier)
Retur: response(string)
Descr: This function will determine the type of statement the user has made. If the statement is a command like "tell
       me" or "I want to know" then a query is going to be made in the knowledge base. Otherwise, sentiment analysis
       will be performed and it will be recorded into a db file. Based on the sentiment, the chatbot will simply reply
       acknowledging the input.
"""
def reply_to_remark(user_id, user_input, remark_model):
    # Predict the sentiment of the user input
    pred_input = remove_noise(word_tokenize(user_input))
    pred = remark_model.classify(dict([token, True] for token in pred_input))

    # If user input has any of these words, then we know it is negative
    negatives = ["don't", "do not", "not", "dont"]
    for neg_word in negatives:
        if neg_word in user_input:
            pred = 'Negative'

    # Common commands to query something
    commands = ["tell me", "let me know", "talk to me", "want to know", "show me"]

    # If a common command is in the user input
    for comm in commands:
        # Then query the command and return the response
        if  comm in user_input:
            answ = get_answer(user_input)
            return answ

    # Create database to register users likings
    db_name = "user_preference.db"
    db_conn = create_connection(db_name)
    tb_name = user_id
    if db_conn is None:
        sys.exit("Error! Cannot create the database connection")

    # Each user will have their own table in the DB
    create_table_query = "CREATE TABLE IF NOT EXISTS " + str(tb_name) + "(id INTEGER PRIMARY KEY, " \
                                                                        "remark text NOT NULL," \
                                                                        "sentiment text NOT NULL);"

    # Create table
    create_table(db_conn, create_table_query)

    # Insert the user input and sentiment into the table
    insert_query = "INSERT INTO " + str(user_id) + "(remark, sentiment) VALUES (?, ?)"
    cur = db_conn.cursor()
    cur.execute(insert_query, (user_input, pred))

    # Close db
    db_conn.close()

    # If the sentiment is positive
    if pred == 'Positive':
        # Reply with a positive response
        positive_responses = ["Really? That's pretty cool.", "Awesome! Tell me more.", "I believe you.", "I guess so.",
                              "Cool. But are going to ask a question?", "I'll keep track of that.", "Your opinion "
                              "matters so thanks for letting me know.", "Well, that's good to know."]
        return random.choice(positive_responses)

    # Otherwise
    else:
        # Reply with a negative response
        negative_responses = ["I am sorry you feel that way.", "I appreciate your honesty.", "You can't be negative "
                              "about that.", "I understand how you feel. Well, not really, I am a bot.", "I don't know what "
                              "to say.", "I'll keep this mind or should I say memory. I know not funny."]
        return random.choice(negative_responses)


"""
Args : List of strings (tokens)
Retur: List of strings (processed tokens)
Descr: This a helper function to get_remark_model(). This function will return the tokens passed to it only after it has
       been processed and any noise data is removed
"""
def remove_noise(tokens):
    # List to be returned
    cleaned_tokens = []

    # For each token, get the token and the pos tag
    for token, tag in pos_tag(tokens):
        # Get rid of any noise data
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        # Lemmatize the word
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        # Append the token only if it is a valid token
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stopwords.words('english'):
            cleaned_tokens.append(token.lower())

    # Return list of tokens
    return cleaned_tokens


"""
Args : List of strings (tokens)
Retur: List of strings (tokens)
Descr: This a helper function to get_remark_model().
"""
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


"""
Args : List of strings (tokens)
Retur: List of dictionaries (tweets)
Descr: This a helper function to get_remark_model(). This function will return the tweets made by the tokens passed.
"""
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


"""
Args : None
Retur: NaiveBayesClassifier
Descr: This function will create a model using the tweets in NLTK to predict the sentiment of the input.
"""
def get_remark_model():
    # Get tweets
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    # Create list for processed tokens
    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    # For each token remove any unnecessary data
    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens))

    # For each token remove any unnecessary data
    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens))

    # Form the tokens into tweets
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    # Add their labels to each tweet
    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]
    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    # Combine the data to have one data set
    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)

    # Train the classifier
    classifier = NaiveBayesClassifier.train(dataset)

    # Return the classifier
    return classifier


"""
Args : None
Retur: None
Descr: Main function. This where the main iteration is occurring and calling the necessary functions to generate a
       response to the user.
"""
def main():
    # If the pickle file that holds the model doesn't exit, then make the model and store it for later.
    if not os.path.exists("ml_model.pkl"):
        print("Waking up chatbot (Training ML Model)...This might take a few minutes...")
        remark_model = get_remark_model()
        pickle.dump(remark_model, open("ml_model.pkl", "wb"))
    # Otherwise, load the model
    else:
        remark_model = pickle.load(open("ml_model.pkl", "rb"))

    # Introduce the chatbot and understand which user this is
    user_id = introduction()

    # Get the user input and determine if it is a question
    is_question, user_input = getInput()

    # While the input is not any of the terminating key words then generate a response
    while 'goodbye' not in user_input and 'quit' not in user_input and 'exit' not in user_input and 'bye' not in \
            user_input:
        # If its a question, then answer it
        if is_question:
            # Generate result and print it
            given_answer = get_answer(user_input)
            print(given_answer.capitalize())
        # Otherwise, simply to reply to the statement
        else:
            # Generate result and print it
            given_answer = reply_to_remark(user_id, user_input, remark_model)
            print(given_answer)

        # Wait for another input
        is_question, user_input = getInput()

    # List of potential responses
    exit_responses = ["PEACE!", "Later!", "See ya!", "Bye.", "Bye! Go Lakers!", "Goodbye", "Hope you come back!",
                      "Peace. PURPLE AND GOLD!"]
    # Print a goodbye message
    print(random.choice(exit_responses))


# Starting point of the program
if __name__ == '__main__':
    main()
