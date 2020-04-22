# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:22:12 2020
TheWikipediaBot                
@author: Akshay Prassanna
"""

import speech_recognition as sr
import urllib.request
from bs4 import BeautifulSoup    
import nltk
import pyttsx3
engine = pyttsx3.init()
try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import string
f=open('chatbot.txt','r')
raw=f.read()
raw=raw.lower()# converts to lowercasenltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)
lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
def wikipedia_response(user_response):

    # to search 
    query = user_response
    query+=" wikipedia"
    l=[]
    for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
        #print(j) 
        l.append(j)
    url=str(l[0])
    print(url)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    #print(soup.prettify())
    #center_text=soup.find('div', class_='mw-parser-output')
    #print(center_text)
    texttoprint=""
    texttoprint+=soup.find('p').getText()
    a=soup.find_all("p", limit=10)
    l1=[]
    for i in a:
        if i.getText()!=" " and len(i.getText())>15:
            l1.append(i.getText())
    print(l1[0])
    engine.say(l1[0])
    engine.runAndWait()
    
def response(user_response):
    
    robo_response = wikipedia_response(user_response)
    return robo_response

flag=True
print("Wikibot: My name is WikiBot. I will answer your wikipedia queries. If you want to exit, say Bye!")
engine.say("My name is WikiBot. I will answer your wikipedia queries. If you want to exit, say Bye!")
engine.runAndWait()
while(flag==True):
    r=sr.Recognizer()
   # print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        count=0
        r.adjust_for_ambient_noise(source,duration=1)
        # r.energy_threshold()
        print("Wikibot: say anything ")
        engine.say("say anything")
        engine.runAndWait()
        audio= r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
        except:
            print("Wikibot: sorry, could not recognise")
            engine.say(" sorry, could not recognise")
            engine.runAndWait()
            count=1
    user_response = text
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("Wikibot: You are welcome..")
            engine.say("You are welcome")
            engine.runAndWait()
        else:
            if(greeting(user_response)!=None):
                res = greeting(user_response)
                print("Wikibot: "+ res)
                engine.say(res)
                engine.runAndWait()
            else:
                if count==0:
                    print("Wikibot: ",end="")
                    response(user_response)
                    
                #sent_tokens.remove(user_response)
    else:
        flag=False
        print("ROBO: Bye! take care..")