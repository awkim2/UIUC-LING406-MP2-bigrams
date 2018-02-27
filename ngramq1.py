import os
import sys
from math import log

def import_training_data_english():
    article_link = os.getcwd() + "/utf-8/LangId.train(1).English"
    article_content = open(article_link, "r")
    bloop=[]
    for i in article_content.readlines():
        i=list(i)
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:-1]
        i = ['<s>'] + i[:-1] + ['</s>']+[None]
        bloop.append(i)
    return bloop

def import_training_data_French():
    article_link = os.getcwd() + "/utf-8/LangId.train(1).French"
    article_content = open(article_link, "r")
    bloop=[]
    for i in article_content.readlines():
        i=list(i)
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:-1]
        i = ['<s>'] + i[:-1] + ['</s>']+[None]
        bloop.append(i)
    return bloop

def import_training_data_Italian():
    article_link = os.getcwd() + "/utf-8/LangId.train(1).Italian"
    article_content = open(article_link, "r")
    bloop=[]
    for i in article_content.readlines():
        i=list(i)
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:-1]
        i = ['<s>'] + i[:-1] + ['</s>']+[None]
        bloop.append(i)
    return bloop

def import_testing_data():
    article_link = os.getcwd() + "/utf-8/LangId(1).test"
    article_content = open(article_link, "r")
    bloop=[]
    for i in article_content.readlines():
        i=list(i)
        if i[-1]=='.' or i[-1]=='?' or i[-1]=='!':
            i=i[:-1]
        i = ['<s>'] + i[:-1] + ['</s>']+[None]
        bloop.append(i)
    return bloop

def make_bigram(data):
    bigram={}
    for sentence in data:
        for word in range(0,len(sentence)-1):
            if sentence[word] in bigram.keys():
                if sentence[word+1] in bigram[sentence[word]].keys():
                    bigram[sentence[word]][sentence[word+1]] += 1
                else:
                    bigram[sentence[word]][sentence[word + 1]] = 1
            else:
                bigram[sentence[word]]={}
                bigram[sentence[word]][sentence[word + 1]] = 1
    return(bigram)

def get_prob(bigram,parent,word):
    val=0
    total=0
    if parent in bigram.keys():
        if word in bigram[parent].keys():
            val = bigram[parent][word]
        else:
            return(0)
        for key in bigram[parent].keys():
            total += bigram[parent][key]
    else:
        return(0)
    return(log(val/total))

def return_language(number,sentence):
    language=['English', 'French', 'Italian']
    chance=[0,0,0]
    for word in range(0,len(sentence)-1):
        chance[0]+= (get_prob(english_bigram,sentence[word],sentence[word+1]))
        chance[1]+= (get_prob(french_bigram, sentence[word], sentence[word + 1]))
        chance[2]+= (get_prob(italian_bigram, sentence[word], sentence[word + 1]))
    print(number, language[chance.index(max(chance))])

if __name__ == "__main__":
    sys.stdout = open(os.getcwd()+'/plain/letter_output.txt', "w")
    english_data=import_training_data_english()
    english_bigram=make_bigram(english_data)

    french_data=import_training_data_French()
    french_bigram=make_bigram(french_data)

    italian_data=import_training_data_Italian()
    italian_bigram=make_bigram(italian_data)

    test_data=import_testing_data()

    for sentence in range(0,len(test_data)):
        return_language(sentence+1,test_data[sentence])
