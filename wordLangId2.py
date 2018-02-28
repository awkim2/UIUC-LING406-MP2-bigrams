import os
import sys
from math import log
from math import exp

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

#For my advanced feature, I decided to implement simple good-turing smoothing
def good_turing_bigram_smoothing(bigram):
    #create the dataset for my linear regression
    # count of counts will store c values
    #occurence of count will store the coressponding Nc value
    count_of_counts=[]
    occurence_of_count=[]
    for parent in bigram.keys():
        for child in bigram[parent].keys():
            count = bigram[parent][child]
            if count in count_of_counts:
                occurence_of_count[count_of_counts.index(count)]+=1
            else:
                count_of_counts.append(count)
                occurence_of_count.append(1)

    # The lines of code from here until the b0 are slightly modified lines of code from
    #https://machinelearningmastery.com/implement-simple-linear-regression-scratch-python/
    #since I did not want to import a linear regression function from a library that may or may not exist on other machines
    #All they do is calculate the linear regression for the Nc versus the log(c)
    #So that the log space linear regression can be used to approximate missing Nc values
    def mean(values):
        return sum(values) / float(len(values))
    def variance(values, mean):
        return sum([(x - mean) ** 2 for x in values])
    occurence_of_count2 = [log(x) for x in occurence_of_count]
    def covariance(x, mean_x, y, mean_y):
        covar = 0.0
        for i in range(len(x)):
            covar += (x[i] - mean_x) * (y[i] - mean_y)
        return covar
    x_mean, y_mean = mean(count_of_counts), mean(occurence_of_count2)
    b1 = covariance(count_of_counts, x_mean, occurence_of_count2, y_mean) / variance(count_of_counts, x_mean)
    b0 = y_mean - b1 * x_mean

    #Update the counts as the good-turing smoothing wants us too
    for parent in bigram.keys():
        for child in bigram[parent].keys():
            old_count = bigram[parent][child]
            if old_count in count_of_counts:
                if old_count+1 in count_of_counts:
                    #if both Nc and Nc+1 are not 0, simply apply the formula c+1*Nc+1/Nc
                    bigram[parent][child] = (old_count+1) * (occurence_of_count[count_of_counts.index(old_count+1)]/occurence_of_count[count_of_counts.index(old_count)])
                else:
                    # if Nc+1 is 0, simply apply the formula c+1*Nc+1/Nc where Nc+1 is calculated from the linear regression above
                    bigram[parent][child]= old_count+1 * ((old_count+1)*exp(b0+b1*(old_count+1))/exp((b0+b1*old_count))/occurence_of_count[count_of_counts.index(old_count)])
    #Otherwise for c=0, the new probability value is N1/N
    bigram['NONEXISTANT_BIGRAM']=occurence_of_count[count_of_counts.index(1)]/(len(bigram.keys())*len(bigram.keys())-sum(occurence_of_count))

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
    #print(chance)
    print(number, language[chance.index(max(chance))])

if __name__ == "__main__":
    #declare the output to go to this file
    sys.stdout = open(os.getcwd()+'/wordLangId2.out', "w")
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
