# Author: Alfredo Mejia
# Class : CS 4395.001
# Date  : 10/4/20
# Descrp: This program will create a web crawler that starts from a google search and tries to crawl through the web
#         to find more relevant urls. This cycle is repeated until a url limit is reached. From the urls the program
#         will scrape the relevant text off the page, unprocessed, and write it to a txt file. These files will be
#         placed under the unprocessed folder. Then the program will get the data from these unprocessed files and
#         try to process the data to extract only the sentences. These sentences will then be written back to a file
#         under a processed folder having one sentence for each line. The program will then try to find the most
#         important terms using two methods. First it will use the tf-idf to get the most important words of each
#         document. Then the program will do some calculation based on the document size to determine how many
#         top-weighted words of each document to extract and add to the overall list of important words. From these
#         important words, a table will be created for each word. The entries of the table will be sentences from any
#         document containing that term. This would be the knowledge based. The knowledge base will be a database file
#         having a table for each important term and storing all the sentences from the corpus that contains that
#         term.


# Imports
from bs4 import BeautifulSoup
import re
import requests
import sys
import os
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import math
from sql_helper_hw5 import create_connection, create_table, create_list_entry, get_db_data


# Main function
def main():
    # Get urls: Q1
    url_db_name = get_urls()

    # Get raw text: Q2
    get_unprocessed_raw_data(url_db_name)

    # Process raw data: Q3
    get_processed_data()

    # Get important terms: Q4
    tf_idf_total = get_tf_idf()
    important_terms = get_important_terms(tf_idf_total)
    terms_db_name = store_important_terms(important_terms)

    # Build knowledge base: Q6
    knowledge_base = create_knowledge_base(terms_db_name)
    kb_db_name = store_knowledge_base(knowledge_base)

    # Print results
    print_results(url_db_name, terms_db_name, kb_db_name)


"""
Args : None
Retur: DB file name for the list of urls
Descr: Starts with a google search and crawls through the web to obtain relevant urls. The urls and then stored into
       a database file. 
"""
def get_urls():
    # Create database file to store the urls found
    db_name = "url_list.db"
    tb_name = db_name[:-3]
    db_conn = create_connection(db_name)

    # If the connection isn't establish quit the program
    if db_conn is None:
        sys.exit("Error! Cannot create the database connection for urls list")

    # Create the query to create table in the db file
    url_create_table_query = "CREATE TABLE IF NOT EXISTS " + str(tb_name) + "(id integer PRIMARY KEY, element text " \
                                                                           "NOT NULL); "
    # Execute the creation of table query
    create_table(db_conn, url_create_table_query)

    # Start with a google search of 'Lakers'
    initial_url = "https://www.google.com/search?source=hp&ei=3Kx4X96TN4SgsQWO05CQDA&q=Lakers&oq=Lakers&gs_lcp=CgZwc3ktYWIQAzILCC4QsQMQgwEQkwIyCAgAELEDEIMBMggIABCxAxCDATILCAAQsQMQgwEQiwMyCwgAELEDEIMBEIsDMgUIABCLAzIFCAAQiwMyCwgAELEDEIMBEIsDMggIABCxAxCDATILCAAQsQMQgwEQiwM6CwguELEDEMcBEKMCOgUIABCxAzoCCAA6CAguEMcBEKMCOg4ILhCxAxCDARDHARCjAjoLCC4QsQMQgwEQiwM6CAguELEDEIMBOgsILhDHARCjAhCLAzoOCC4QsQMQxwEQowIQiwM6CAgAELEDEIsDOggIABCSAxCLAzoFCC4QiwM6CAguELEDEIsDOg4ILhCxAxCLAxCoAxCdA0oFCAcSATFKBQgJEgExSgUIChIBN1CjCli7FGDxFWgBcAB4AIABSogBvgOSAQE3mAEAoAEBqgEHZ3dzLXdperABALgBAw&sclient=psy-ab&ved=0ahUKEwje8bbd8ZjsAhUEUKwKHY4pBMIQ4dUDCAk&uact=5"
    urls = [initial_url]

    # Limit of websites to obtain
    url_limit = 25

    # For each link in urls list
    for url in urls:
        # Get the beautiful soup object of the link
        data_soup = get_soup(url)

        # Find the links of the page
        for link in data_soup.find_all('a'):
            link_str = str(link.get('href'))

            # Link must have lakers in it
            if 'Lakers' in link_str or 'lakers' in link_str:
                # Filter the links to what we want
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]

                # If its an appropriate link append it to the list
                if link_str.startswith('http') and 'google' not in link_str:
                    urls.append(link_str)

        # Check if limit has been reached
        if len(urls) >= url_limit:
            break

    # Remove the initial url because that doesn't provide useful content (google search)
    urls.remove(initial_url)

    # Add the list to the table
    create_list_entry(db_conn, urls, tb_name)

    # Close db connection
    db_conn.close()

    # Return the db name
    return db_name


"""
Args : Database name for the urls
Retur: None
Descr: Iterates through the urls and extract its raw data. If the raw data is somewhat relevant then a text file is 
       created and the raw data is written to it. Note, not all urls will have a text file because not all urls will 
       have relevant data. 
"""
def get_unprocessed_raw_data(url_db_name):
    # Get the urls from the db file passed
    db_conn = create_connection(url_db_name)
    db_data = get_db_data(db_conn, url_db_name[:-3])
    db_conn.close()

    # If a unprocessed folder does not exists, then make it to contain unprocessed text
    if not os.path.exists('./unprocessed'):
        os.mkdir('./unprocessed')

    # For each url in the db file
    for id, element in db_data:
        # Get the Beautiful soup of the link
        data_soup = get_soup(element)

        # Create a file name based on the link
        file_name = get_file_name(element)

        # Get all p tags and title tag
        all_revelant_data = data_soup.findAll('p')
        title = data_soup.find('title')

        # If there is a title
        if title is not None:
            # Get the text of the title
            title = title.getText()
            # Add it to the beginning containing all the data
            all_revelant_data.insert(0, title)

            # However, if title is forbidden that means the url was denied
            # Continue to the next url
            if 'forbidden' in title.lower():
                continue

        # Get rid of sites without content like ecommerce, social media, etc.
        if len(all_revelant_data) <= 3:
            continue

        # Open a file with the name generated
        file = open('./unprocessed/' + str(file_name), 'w+', encoding='utf-8')

        # Add the unfiltered content of the url to the file
        for sent in all_revelant_data:
            file.write(str(sent) + '\n')

        # Close file
        file.close()


"""
Args : None
Retur: None
Descr: Iterates through the unprocessed files and processes the data and writes the results into another file
"""
def get_processed_data():
    # Create processed folder if there isn't one
    if not os.path.exists('./processed'):
        os.mkdir('./processed')

    # For each file in the unprocessed folder
    for filename in os.listdir('./unprocessed'):
        # Open it and read it
        input_file = open('./unprocessed/' + str(filename), 'r', encoding='utf-8')
        file_data = input_file.readlines()
        file_data = [sent.strip() for sent in file_data]
        input_file.close()

        # Create a file for the processed version
        output_file = open('./processed/' + str(filename), 'w+', encoding='utf-8')

        # Call a function to process (filter) the unprocessed data and write to the file
        write_to_file(file_data, output_file)

        # Close file
        output_file.close()


"""
Args : None
Retur: Sorted dictionary having TF-IDF for each document (nested dictionary)
Descr: Calculates the TF-IDF for each document
"""
def get_tf_idf():
    # Create dictionary for term frequency
    tf_dict = {}

    # Get stop words from NLTK
    eng_stopwords = stopwords.words('english')

    # Get the file names from the processed folder
    filenames = [filename for filename in os.listdir('./processed')]

    # Create an empty set for the total vocab found
    total_vocab = set()

    # For each file in the processed folder
    for filename in filenames:
        # Create a nested dictionary for each file
        tf_dict[filename] = {}

        # Open the file and read it
        file = open('./processed/' + str(filename), 'r', encoding='utf-8')
        file_data = file.read().lower()
        file_data.replace('\n', '')

        # Tokenize the data and filter it
        tokens = word_tokenize(file_data)
        tokens = [word for word in tokens if word.isalpha() and word not in eng_stopwords]

        # Get set of tokens and then get the count for each element in the set
        # This is stored as a nested dictionary with the term being the key and value being the count
        token_set = set(tokens)
        tf_dict[filename] = {t: tokens.count(t) for t in token_set}

        # For each term divide it by the len of total tokens to get the term frequency
        for t in tf_dict[filename].keys():
            tf_dict[filename][t] = tf_dict[filename][t] / len(tokens)

        # Combine the set of tokens to form the total vocabulary of the corpus
        total_vocab = total_vocab.union(set(tf_dict[filename].keys()))

    # Create dictionary for inverse document frequency
    idf_dict = {}

    # Get the set of tokens from each document
    vocab_by_doc = [tf_dict[fname].keys() for fname in filenames]

    # For a word in the total vocabulary
    for term in total_vocab:
        # Add x to temp if the term appears in one document
        temp = ['x' for voc in vocab_by_doc if term in voc]
        # Calculate the IDF for that term
        idf_dict[term] = math.log((1 + len(filenames)) / (1 + len(temp)))

    # Create tf-idf metric dictionary
    tf_idf_dict = {}

    # For every file
    for name in filenames:
        # Create a nested dictionary
        tf_idf_dict[name] = {}

        # For every term in the file, calculate the tf-idf
        for t in tf_dict[name].keys():
            tf_idf_dict[name][t] = tf_dict[name][t] * idf_dict[t]

    # Sorted TF-IDF dictionary
    sorted_tf_idf = {}

    # For every file, sort its TF-IDF for every term
    for name in filenames:
        doc_term_weights = sorted(tf_idf_dict[name].items(), key=lambda x: x[1], reverse=True)
        sorted_tf_idf[name] = doc_term_weights

    # Return the sorted TF-IDF dictionary
    return sorted_tf_idf


"""
Args : TF-IDF for each document (expects a dictionary)
Retur: Set of important terms for the whole corpus
Descr: Iterates through the TF-IDF of each document and extracts only a certain amount of the top terms from each doc
"""
def get_important_terms(tf_idf_total):
    # List to hold important terms
    important_terms = []

    # Nth root to decide how many important terms to retrieve from every document
    root = 5

    # For every document in the dictionary
    for doc in tf_idf_total:
        # Calculate the amount of terms to extract from this document
        num_of_terms = round(len(tf_idf_total[doc]) ** (1.0 / root))

        # Get the whole set of terms for this document
        list_of_terms = tf_idf_total[doc]
        counter = 0

        # For every term in the list
        for term, weight in list_of_terms:
            # If it does not exceed the maximum amount of terms for this document
            if counter >= num_of_terms:
                break
            counter += 1

            # Add the term to important terms list
            important_terms.append(term)

    # Return the set of the important terms list
    return set(important_terms)


"""
Args : List of important terms
Retur: Database file name containing the important terms
Descr: Creates a db file to store the important terms
"""
def store_important_terms(important_terms):
    # Name the db and tb for important terms
    db_name = "important_terms.db"
    tb_name = db_name[:-3]

    # Delete the important terms db file if there is one because we don't want to add to it
    # The important terms reflect on the current corpus thus adding to it will include previous important terms
    # From previous documents. Thus we only want to store the important terms from the current corpus
    if os.path.exists('./' + str(db_name)):
        os.remove('./' + str(db_name))

    # Create db connection
    db_conn = create_connection(db_name)

    # If connection isn't establish, exit program
    if db_conn is None:
        sys.exit("Error! Cannot create the database connection for important terms")

    # Create the query for the table
    terms_create_table_query = "CREATE TABLE IF NOT EXISTS " + str(tb_name) + "(id integer PRIMARY KEY, element text " \
                                                                       "NOT NULL); "

    # Create table
    create_table(db_conn, terms_create_table_query)

    # Create entries in the table with the important terms
    create_list_entry(db_conn, important_terms, tb_name)

    # Close connection
    db_conn.close()

    # Return database name
    return db_name


"""
Args : Database file name containing the important terms 
Retur: Knowledge base dictionary with key as an important term and value as a list of sents containing the key
Descr: Creates the knowledge base based off the important terms
"""
def create_knowledge_base(terms_db_name):
    # Create connection to the db file and read the data
    db_conn = create_connection(terms_db_name)
    db_data = get_db_data(db_conn, terms_db_name[:-3])
    db_conn.close()

    # Create a dictionary for knowledge base
    # The important term will be the key and the value will be a list of sentences from the whole corpus containing
    # that term
    knowledge_base = {}

    # Get the list of files from the processed folder
    filenames = [filename for filename in os.listdir('./processed')]

    # For each term in the important terms db
    for id, term in db_data:
        # Create a list based on the term
        knowledge_base[term] = []

        # For each file in processed folder
        for filename in filenames:
            # Open the file and read it
            input_file = open('./processed/' + str(filename), 'r', encoding='utf-8')
            file_data = input_file.readlines()
            input_file.close()

            # Get rid of newlines and lower the sentences
            file_data = [sent.strip().lower() for sent in file_data]

            # Get the sentences that have the term in the sentence
            interested_data = [sent for sent in file_data if term in sent]

            # Add the sentences to the knowledge base
            knowledge_base[term] = knowledge_base[term] + interested_data

    # Return the knowledge base
    return knowledge_base


"""
Args : Knowledge base dictionary
Retur: Database file name of the knowledge base 
Descr: Creates a db file to store each important term as its own table with its sents as entries using the KB dictionary
"""
def store_knowledge_base(knowledge_base):
    # Create a database for the knowledge base
    db_name = "knowledge_base.db"
    db_conn = create_connection(db_name)

    # If connection isn't established, exit program
    if db_conn is None:
        sys.exit("Error! Cannot create the database connection for knowledge base")

    # For each term in the knowledge base
    for term in knowledge_base.keys():
        # Table query creation
        one_term_create_table = "CREATE TABLE IF NOT EXISTS " + str(term) + "(id integer PRIMARY KEY, element text " \
                                                                            "NOT NULL); "
        # Create table for the term
        create_table(db_conn, one_term_create_table)

        # Add the sentences containing that term to the table
        create_list_entry(db_conn, knowledge_base[term], term)

    # NOTE: In total, we will have N tables, each table will correspond to an important term. The entries in the table
    # will be ONLY one sentence per entry that contains the term in it. These sentences will be from ALL documents
    # processed.

    # Close connection
    db_conn.close()

    # Return database name
    return db_name


"""
Args : One URL (string)
Retur: Beautiful Soup object
Descr: Creates a Beautiful Soup object based on the url passed (helper function)
"""
def get_soup(url):
    # Get the text of the url
    req = requests.get(url)
    raw_data = req.text

    # Create a Beautiful soup object based on the raw text
    data_soup = BeautifulSoup(raw_data, features="html.parser")

    # Return the Beautiful soup object
    return data_soup


"""
Args : One URL (string)
Retur: Allowable Windows file name based on the url (string)
Descr: Converts the url to a compatible windows file name (helper function)
"""
def get_file_name(element):
    # Convert url to an appropriate windows file name
    file_name = element.replace('https://', '')
    file_name = file_name.replace('www', '')
    file_name = file_name.replace('/', '-')
    file_name = re.compile('[^a-zA-Z_-]').sub('', file_name)[:200]
    file_name = file_name + ".txt"

    # Return file name created
    return file_name



"""
Args : List of strings from a doc, file connection
Retur: None
Descr: Filters and processes the list of strings to get rid of html tags. It then sentence tokenize the strings to be
       able to write one sentence to each line to the file passed. This is a helper function to the get_processed_data
       function.
"""
def write_to_file(file_data, output_file):
    # Create a list for sentences
    sentences = []

    # For each html tag found in the list
    for tag in file_data:
        # If it still has the HTML opening and closing tags
        while '<' in tag and '>' in tag:
            # Delete the tags
            tag_start_index = tag.find('<')
            tag_stop_index = tag.find('>')
            tag = tag[0:tag_start_index:] + tag[tag_stop_index + 1::]

        # Sentence tokenize the tag
        sentences = sentences + sent_tokenize(tag)

    # Gets rid of empty strings if any
    sentences = [nonempty for nonempty in sentences if nonempty]

    # Write the sentences in the file
    for sent in sentences:
        output_file.write(str(sent) + '\n')


"""
Args : URL database file name, important terms database file name, knowledge base database file name
Retur: None
Descr: Prints the urls stored, my predicted important terms, the important terms stored, and two sentences of the KB
       for each important term.
"""
def print_results(url_db_name, terms_db_name, knowledge_base_db_name):
    # Create db connections
    url_db_conn = create_connection(url_db_name)
    terms_db_conn = create_connection(terms_db_name)
    kb_db_conn = create_connection(knowledge_base_db_name)

    # If no connection establish, quit program
    if url_db_conn is None or terms_db_conn is None or kb_db_conn is None:
        sys.exit('Error! Cannot create a database connection')

    # Get urls and important terms
    url_db_data = get_db_data(url_db_conn, url_db_name[:-3])
    terms_db_data = get_db_data(terms_db_conn, terms_db_name[:-3])
    url_db_conn.close()
    terms_db_conn.close()

    # Print urls
    print('\nPrinting the URL list in the database...\n')
    for id, url in url_db_data:
        print(str(id) + ': ' + str(url))

    print('\nPlease note that not all URLs were converted to a txt file.'
          '\nAlthough some URLs seemed relevant their content was not.\n')

    # My prediction of important terms
    my_prediction = [ "lakers", "los", "angeles", "lebron", "james", "anthony", "davis", "kobe", "bryant", "nba",
                      "basketball", "finals", "championship", "shaq"]

    # Print my prediction
    print('\nPrinting my prediction for important terms...\n')
    for index, term in enumerate(my_prediction):
        print(str(index+1) + ': ' + str(term))

    # Print actual important terms calcaulted
    print('\nPrinting the actual important terms in the database...\n')
    for id, term in terms_db_data:
        print(str(id) + ': ' + str(term))

    # Print two sentences of each term in the knowledge base
    print('\nPrinting some sentences (NOT ALL) of the knowledge base...\n')

    # For each term
    for id, term in terms_db_data:
        # Grab the term's kb
        term_kb_data = get_db_data(kb_db_conn, term)
        print(str(term) + ':')
        counter = 0;

        # Print two sentences from the term's knowledge base
        for key, sent in term_kb_data:
            # Comment this to see whole knowledge base database
            if counter >= 2:
                break

            print('\t' + str(key) + ': ' + str(sent))
            counter += 1


# Starting point of the program
if __name__ == '__main__':
    main()
