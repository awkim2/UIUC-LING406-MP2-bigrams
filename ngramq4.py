import os
import sys
from math import log

#Import english training data; the other languages and the testing data set do the same thing so not repeating comments
def import_training_data_english():
    #get link, open the file
    article_link = os.getcwd() + "/utf-8/LangId.train(1).English"
    article_content = open(article_link, "r")
    #this is where the preprocessed text will be stored
    processed_text_store=[]
    # per line in the file 
    for i in article_content.readlines():
        # split the line 
        i=i.split()
        #if it ends in puncuation as its own word, remove it 
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:-1]
        # include start and end characters for the bigram to be better able to calculate ordering probabilities 
        i = ['<s>'] + i[:-1] + ['</s>']
        processed_text_store.append(i)
    return processed_text_store

def import_training_data_French():
    article_link = os.getcwd() + "/utf-8/LangId.train(1).French"
    article_content = open(article_link, "r")
    processed_text_store=[]
    for i in article_content.readlines():
        i=i.split()
        if len(i)>0:
            if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
                i=i[:-1]
            i = ['<s>'] + i[:-1] + ['</s>']
            processed_text_store.append(i)
    return processed_text_store

def import_training_data_Italian():
    article_link = os.getcwd() + "/utf-8/LangId.train(1).Italian"
    article_content = open(article_link, "r")
    processed_text_store=[]
    for i in article_content.readlines():
        i=i.split()
        if len(i)>0:
            if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
                i=i[:-1]
            i = ['<s>'] + i[:-1] + ['</s>']
            processed_text_store.append(i)
    return processed_text_store

def import_testing_data():
    article_link = os.getcwd() + "/utf-8/LangId(1).test"
    article_content = open(article_link, "r")
    processed_text_store=[]
    for i in article_content.readlines():
        i=i.split()
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:-1]
        i = ['<s>'] + i[:-1] + ['</s>']
        processed_text_store.append(i)
    return processed_text_store


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

#For my advanced feature, I decided to implement good-turing smoothing
def good_turing_bigram_smoothing(bigram):
    #For good turing smoothing, I need to get the number of bigrams that only exist a single time
    #The total number of bigram instances we've found
    #And the unique bigrams we've found
    number_of_single_bigrams=0
    total_bigrams=0
    number_of_existing_pairs=0
    for parent in bigram.keys():
        for big in bigram[parent].keys():
            if bigram[parent][big]==1:
                number_of_single_bigrams+=1
            number_of_existing_pairs+=1
            total_bigrams+=bigram[parent][big]

    #Then, we define the probability that a bigram has just 1 occurence as number of single/total bigrams
    probability_of_bigram_with_1_occurence=number_of_single_bigrams/total_bigrams

    #The next step is to multiply every single bigram count by this probability value
    #To make space for all the 0 value'd bigrams that we're creating "cap space" for
    for parent in bigram.keys():
        for big in bigram[parent].keys():
            bigram[parent][big]=bigram[parent][big]*(1-probability_of_bigram_with_1_occurence)

    #Finally, i added a key to the bigram for the case where the bigram doesnt exist in our dictionary
    # this is simply the
    # total probability that the bigram has a 1 occurence
    # divided by
    # total number of possible bigrams- the number of existing bigrams
    # ie probability of one occurence/number of bigrams with 0 occurence

    bigram['NONEXISTANT_BIGRAM']=probability_of_bigram_with_1_occurence/(len(bigram.keys())*len(bigram.keys())-number_of_existing_pairs)
    return(bigram)

#Get the probability of this bigram
def get_prob(bigram,parent,word):
    #total is the number of times we saw word w-1
    total=0
    if parent in bigram.keys():
        for key in bigram[parent].keys():
            total += bigram[parent][key]
    #val is the number of times w appeared given this parent w-1
        if word in bigram[parent].keys():
            val = bigram[parent][word]
    #If the bigram doesnt exist, the probability of it is [NONEXISTANT BIGRAM]
    #AKA probability of a 0 bigram
        else:
            return(bigram['NONEXISTANT_BIGRAM'])
    else:
        return (bigram['NONEXISTANT_BIGRAM'])

    return(val/total)

def return_language(number,sentence):
    language=['English', 'French', 'Italian']
    #Initialize chance of each word to be 0
    chance=[0,0,0]
    #add the log probabilities of each bigram in the sentence to the 0
    for word in range(0,len(sentence)-1):
        chance[0]+=log(get_prob(english_bigram,sentence[word],sentence[word+1]))
        chance[1]+= log(get_prob(french_bigram, sentence[word], sentence[word + 1]))
        chance[2]+= log(get_prob(italian_bigram, sentence[word], sentence[word + 1]))
    #select the biggest number (aka the smallest one since log probailities are negative, as the language of choice
    print(number, language[chance.index(max(chance))])

if __name__ == "__main__":
    #declare the output to go to this file
    sys.stdout = open(os.getcwd()+'/plain/output.txt', "w")
    #Import and make smoothed bigrams for all 3 languages
    english_data=import_training_data_english()
    english_bigram=good_turing_bigram_smoothing(make_bigram(english_data))

    french_data=import_training_data_French()
    french_bigram=good_turing_bigram_smoothing(make_bigram(french_data))

    italian_data=import_training_data_Italian()
    italian_bigram=good_turing_bigram_smoothing(make_bigram(italian_data))

    #import test_Data
    test_data=import_testing_data()
    # test each line
    for sentence in range(0,len(test_data)):
        return_language(sentence+1,test_data[sentence])
