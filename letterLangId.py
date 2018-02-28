import os
import sys
from math import log

#Import english training data; the other languages and the testing data set do the same thing so not repeating comments
def import_training_data_english():
    #get link, open the file
    article_link = os.getcwd() + "/utf-8/LangId.train(1).English"
    article_content = open(article_link, "r")
    #this is where the preprocessed text will be stored
    preprocessed_text=[]
    # per line in the file
    for i in article_content.readlines():
        # split the line into a list of individual characters
        i=list(i)
        #remove both the trailing whitespace and the trailing newline character in every line 
        i=i[:-2]
        #if it ends in puncuation, remove it
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:-1]
        # include start and end characters for the bigram to be better able to calculate ordering probabilities
        i = ['<s>']+i+ ['</s>']+[None]
        #append to the preprocessed text storage
        preprocessed_text.append(i)
    return preprocessed_text

def import_training_data_French():
    article_link = os.getcwd() + "/utf-8/LangId.train(1).French"
    article_content = open(article_link, "r")
    preprocessed_text=[]
    # per line in the file
    for i in article_content.readlines():
        # split the line into a list of individual characters
        i=list(i)
        if len(i)>2:
            #remove both the trailing whitespace and the trailing newline character in every line
            i=i[:-2]
            #if it ends in puncuation, remove it
            if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
                i=i[:-1]
            # include start and end characters for the bigram to be better able to calculate ordering probabilities
            i = ['<s>']+i+ ['</s>']+[None]
            #append to the preprocessed text storage
            preprocessed_text.append(i)
    return preprocessed_text

def import_training_data_Italian():
    article_link = os.getcwd() + "/utf-8/LangId.train(1).Italian"
    article_content = open(article_link, "r")
    preprocessed_text=[]
    # per line in the file
    for i in article_content.readlines():
        # split the line into a list of individual characters
        i=list(i)
        if len(i)>2:
            #remove both the trailing whitespace and the trailing newline character in every line
            i=i[:-2]
            #if it ends in puncuation, remove it
            if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
                i=i[:-1]
            # include start and end characters for the bigram to be better able to calculate ordering probabilities
            i = ['<s>']+i+ ['</s>']+[None]
            #append to the preprocessed text storage
            preprocessed_text.append(i)
    return preprocessed_text

def import_testing_data():
    article_link = os.getcwd() + "/utf-8/LangId(1).test"
    article_content = open(article_link, "r")
    preprocessed_text=[]
    # per line in the file
    for i in article_content.readlines():
        # split the line into a list of individual characters
        i=list(i)
        #remove both the trailing whitespace and the trailing newline character in every line
        i=i[:-2]
        #if it ends in puncuation, remove it
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:-1]
        # include start and end characters for the bigram to be better able to calculate ordering probabilities
        i = ['<s>']+i+ ['</s>']+[None]
        #append to the preprocessed text storage
        preprocessed_text.append(i)
    return preprocessed_text

#Produce the bigram given the input data
def make_bigram(data):
    bigram={}
    #per sentence
    for sentence in data:
        #per word index in the sentence
        for word in range(0,len(sentence)-1):
            #if this word is a key in the bigram already
            if sentence[word] in bigram.keys():
                #If the next word is a key in the previous words dictionary, increment it
                if sentence[word+1] in bigram[sentence[word]].keys():
                    bigram[sentence[word]][sentence[word+1]] += 1
                #If the next word is not a key, make it a key and set it to 1 occurence
                else:
                    bigram[sentence[word]][sentence[word + 1]] = 1
            #if the word is not a key yet, make it a key
            #and also give it a bigram key and set the value to 1
            else:
                bigram[sentence[word]]={}
                bigram[sentence[word]][sentence[word + 1]] = 1

    return(bigram)

def get_prob(bigram,parent,word):
    #number of times we saw this word w in our training set
    val=0
    # number of times we saw the parent w-1 in our training set
    total=0

    if parent in bigram.keys():
        if word in bigram[parent].keys():
            #if along with the parent we also saw w in our training set, set val to the count
            val = bigram[parent][word]
        #if we didnt see w return a probability of 0
        else:
            return(0)
        #we only get here if we saw both w-1 and w in our training set; the denominator needs the full count of the number of times w-1 showed up
        for key in bigram[parent].keys():
            total += bigram[parent][key]
    #if we didnt see the parent at all return 0
    else:
        return(0)
    #since we saw parent and child, return the probability
    return(log(val/total))


def return_language(number,sentence):
    language=['English', 'French', 'Italian']
    #Initialize chance of each word to be 0
    chance=[0,0,0]
    #add the log probabilities of each bigram in the sentence to the 0
    for word in range(0,len(sentence)-1):
        chance[0]+=get_prob(english_bigram,sentence[word],sentence[word+1])
        chance[1]+=get_prob(french_bigram, sentence[word], sentence[word + 1])
        chance[2]+=get_prob(italian_bigram, sentence[word], sentence[word + 1])
    #select the biggest number (aka the smallest one since log probailities are negative, as the language of choice
    print(number, language[chance.index(max(chance))])

if __name__ == "__main__":
    #declare the output to go to this file
    sys.stdout = open(os.getcwd()+'/letterLangId.out', "w")
    #Import and make smoothed bigrams for all 3 languages
    english_data=import_training_data_english()
    english_bigram=make_bigram(english_data)

    french_data=import_training_data_French()
    french_bigram=make_bigram(french_data)

    italian_data=import_training_data_Italian()
    italian_bigram=make_bigram(italian_data)

    #import test_Data
    test_data=import_testing_data()

    # test each line
    for sentence in range(0,len(test_data)):
        return_language(sentence+1,test_data[sentence])

