#!/usr/bin/env python3

import re
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
import random
import string # to process standard python strings
import urllib.request
from tqdm import tqdm

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# first-time use only
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def is_greeting_test(user_response):
    for word in user_response.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

wnl = nltk.WordNetLemmatizer()
def lemmatize_sentence(sentence):

    # tokenize the sentence and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))

    # tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)

    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(wnl.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


def removeStopwords(sent):
    no_stop = [word for word in word_tokenize(sent) if not word in stopwords.words()]
    return " ".join(no_stop)


def removePunctuationSentence(sent):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    sent = sent.translate(remove_punct_dict)
    sent = re.sub(' +', ' ', sent)  # remove duplicate whitespaces
    return sent


def pre_process(sample):
    text = lemmatize_sentence(sample)
    text = removeStopwords(sample)
    text = removePunctuationSentence(sample)
    return sample


# Read Data
url = 'https://raw.githubusercontent.com/parulnith/Building-a-Simple-Chatbot-in-Python-using-NLTK/master/chatbot.txt'
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object
raw = data.decode('latin-1') # a `str`; this step can't be used if data is binary

# TESTING
# raw = """DENNIS: Listen, strange women lying in ponds and lakes distributing swords
#  is no basis for a system of government.  Supreme executive power derives from
#  a mandate from the masses, not from some farcical aquatic ceremony."""

# converts to list of sentences
samples = nltk.sent_tokenize(raw)

# compile corpus of samples / sentences
corpus = []
print('pre-processing corpus...')
for sample in tqdm(samples):
  corpus.append(pre_process(sample))

# Generating Response
def getBotResponse(user_response):

    vectorizer = TfidfVectorizer()

    # X : sparse matrix, [n_samples, n_features]
    X = vectorizer.fit_transform(corpus) # applied to tokenized training corpus `chatbot.txt`

    # compute similarity between user input X[-1] (i.e. the last sample) and all other sentences in corpus
    sims = cosine_similarity(X[-1], X) # [1 x 656] x [70, 656] >> sklearn takes of transposing
    most_sim_score = sorted(sims[0])[-2] # sim is a nested list hence we use [0]

    # sort and get index of most similar sentence
    idx_sims_sorted = sims.argsort()[0]  # sim is a nested list hence we use [0]
    most_sim_idx = idx_sims_sorted[-2]

    # get most similar sentence
    most_sim = corpus[most_sim_idx]


    if(most_sim_score==0):
        robo_response = "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = most_sim
        return robo_response


flag=True
print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("ROBO: You are welcome..")
        else:
            if(is_greeting_test(user_response)!=None):
                print("ROBO: " + is_greeting_test(user_response))
            else:
                print("ROBO: The sentence in my corpus that is most similar to your input is ...: \n",end="")

                # we add the user's input to the corpus BEFORE producing TFIDF matrix X
                # in this way the user's input becomes effectively the last row in X
                corpus.append(pre_process(user_response))

                print(getBotResponse(user_response))
                corpus.remove(user_response)
    else:
        flag=False
        print("ROBO: Bye! take care..")
