#!/usr/bin/env python3

import re
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
import random
import string # to process standard python strings
import urllib.request
from tqdm import tqdm
import nlp_utils

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


# Read Data
url = 'https://raw.githubusercontent.com/parulnith/Building-a-Simple-Chatbot-in-Python-using-NLTK/master/chatbot.txt'
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object
raw = data.decode('latin-1')

# TESTING
# raw = """DENNIS: Listen, strange women lying in ponds and lakes distributing swords
#  is no basis for a system of government.  Supreme executive power derives from
#  a mandate from the masses, not from some farcical aquatic ceremony."""


corpus = nlp_utils.pre_process(raw)
# print(corpus)

# Generating Response
def getBotResponse(user_response):

    vectorizer = TfidfVectorizer()
    # print(corpus)
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
                corpus.append(nlp_utils.pre_process(user_response)[0]) #TODO review nlp_utils to not return a list?

                print(getBotResponse(user_response))
                corpus.remove(user_response)
    else:
        flag=False
        print("ROBO: Bye! take care..")
