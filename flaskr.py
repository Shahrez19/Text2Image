from flask import Flask
from flask import render_template
import json


import indicoio
from nltk import tokenize
import re


indicoio.config.api_key = '98b8ace96d4afc41cbb080a31ae1ea40'

def cleanText(txt):
    '''Takes a string txt and returns a list containing the words after the
    string has been cleaned.
    '''
    s = txt
    s = s.replace(',', '')
    s = s.replace(';', '')
    s = s.replace(':', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace('_', '')
    s = s.replace('--', '')
    s = s.replace("'", '')
    return s

def splitParagraphIntoSentences(paragraph):
    ''' break a paragraph into sentences
        and return a list '''
    # to split by multile characters

    #   regular expressions are easiest (and fastest)
    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList

def findTopN(sentence):
    ''' defines the top n keywords needed in a sentence'''
    length = len(sentence.split())
    n = length // 2
    return n

def findKeywords(inputString, top_n=5):
    ''' returns the keywords of a sentence in a list'''
    keywordDict = indicoio.keywords(inputString,top_n=top_n)
    return list(keywordDict)
    
def findNames(inputString):  
    #inputString = input('Insert some text here: ')    
    return indicoio.named_entities(inputString)
    
def main(inputString):
    #inputString = input('Insert a paragraph here: ')
    inputString = inputString[:-1]
    cleanedString = cleanText(inputString)
    splitIntoSentences = splitParagraphIntoSentences(cleanedString)
    
    keywords = []
    for sentence in splitIntoSentences:
        keywords += findKeywords(sentence, findTopN(sentence))
        
    return keywords



app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    result = main(request.form.get('text'))
    return json.dumps(result)


if __name__ == '__main__':
    app.debug = True
    app.run()


