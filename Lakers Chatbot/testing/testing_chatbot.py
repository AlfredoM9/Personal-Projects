import nltk
import numpy as np
import random
import string
import wikipedia
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

subject = input()
# while subject != "quit":
#     pages = wikipedia.search(subject)
#     if len(pages) == 0:
#         pages = wikipedia.suggest(subject)
#         print("Did you mean: ")
#     print(pages)
#     subject = input()
raw = wikipedia.page(subject)
raw = raw.content

# print(type(raw))

raw = raw.lower()
sent_tokens = nltk.sent_tokenize(raw)
sent_tokens = [sent.replace("\n", " ").replace("\t", " ").replace("==", "") for sent in sent_tokens]
word_tokens = nltk.word_tokenize(raw)
word_tokens = [word for word in word_tokens if word.isalpha()]

# print(sent_tokens)
# print(word_tokens)

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad you're talking to me", "Howdy",
                      "Howdy Stranger", "Introduce Yourself! JK. Hello"]

lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower()))


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)

    tfIdfVec = TfidfVectorizer( stop_words='english')
    tfidf = tfIdfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    print(vals.argsort()[0])
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        robo_response = robo_response + "I am sorry! I don't understand you."
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


flag = True
print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
while (flag == True):
    user_response = input()
    user_response = user_response.lower()
    if user_response != 'bye':
        if user_response == 'thanks' or user_response == 'thank you':
            flag = False
            print("ROBO: You are welcome..")
        else:
            if greeting(user_response) is not None:
                print("ROBO: " + greeting(user_response))
            else:
                print("ROBO: ", end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag = False
        print("ROBO: Bye! take care..")

