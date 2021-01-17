import spacy
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

if __name__ == '__main__':
    # while True:
    #     nlp = spacy.load('en_core_web_sm')
    #     sent = input()
    #     doc=nlp(sent)
    #
    #     # sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
    #
    #
    #     count = 0
    #     question = False
    #     w_count = -1
    #     for token in doc:
    #         print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #               token.shape_, token.is_alpha, token.is_stop)
    #
    #         if 'W' in token.tag_:
    #             w_count = count
    #             print('Hello')
    #
    #         if 'V' in token.tag_ and w_count == count - 1:
    #             question = True
    #         count += 1
    #
    #     if question:
    #         print('Its a question')
    #
    #     print(sum([1 for i in doc.ents]))
    #     print(len(doc.ents))
    #     for i in doc.ents:
    #         print(i)
    import pandas as pd

    filepath_dict = {'yelp': 'data/sentiment_analysis/yelp_labelled.txt',
                     'amazon': 'data/sentiment_analysis/amazon_cells_labelled.txt',
                     'imdb': 'data/sentiment_analysis/imdb_labelled.txt'}

    df_list = []
    for source, filepath in filepath_dict.items():
        df = pd.read_csv(filepath, names=['sentence', 'label'], sep='\t')
        df['source'] = source  # Add another column filled with the source name
        df_list.append(df)

    df = pd.concat(df_list)
    print(df)

    sentences = df['sentence'].values
    y = df['label'].values

    sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, y, test_size=0.15, random_state=1000)

    vectorizer = CountVectorizer()
    vectorizer.fit(sentences_train)
    X_train = vectorizer.transform(sentences_train)
    X_test = vectorizer.transform(sentences_test)

    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    print(classifier.predict(X_test[-10]))
    print(classifier.predict_proba(X_test[-10])[0][1])
    print(X_test)
    print(y_test[0])
    print(sentences_test[0])

    print('Accuracy for data: ' + str(score))