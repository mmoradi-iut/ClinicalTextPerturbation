import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

from builtins import str

import csv
import sys, getopt

import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, Node
import xml.dom.minidom       
from numpy import double

from random import seed
from random import randint


seed(1)

#--------------------------------------------------------------------------------------------------------------------

def return_random_number(begin, end):
    return randint(begin, end)


class Synonym:
    
    def __init__(self, first_word, second_word, input_similarity, input_frequency):
        self.first_word = first_word
        self.second_word = second_word
        self.similarity = input_similarity
        self.frequency = input_frequency

#--------------------------------------------------------------------------------------------------------------------

input_address = 'Corpus\\Synonyms.csv'

synonym_list = []

with open(input_address) as input_file:
    input_data = csv.reader(input_file, delimiter=',')
    
    for row in input_data:
        first_word = row[0]
        second_word = row[1]
        similarity = double(row[2])
        frequency = int(row[3])
        
        synonym_pair = Synonym(first_word, second_word, similarity, frequency)
        synonym_list.append(synonym_pair)



max_replace = 3

input_address = 'Dataset\\i2b2.tsv'

output_text = 'text' + '\t' + 'label' + '\n'

num_perturbed_samples = 0
    
with open(input_address) as input_file:
        
    input_data = csv.reader(input_file, delimiter='\t')
    
    line_num = 0
    
    for row in input_data:
        
        if (line_num > 0):
        
            print(row[0], '\t', row[1])
        
            is_sample_perturbed = False
            
            sample_text = row[0]
            sample_label = row[1]
            sample_tokenized = nltk.word_tokenize(sample_text)
        
            word_replaced = False
            perturbed_sample = sample_text
            
            candidate_synonym = []
            can_be_replaced_list = []
            
            for i in range(0, len(synonym_list)):
                if (synonym_list[i].first_word in sample_tokenized):
                    candidate_synonym.append(synonym_list[i])
                    if (synonym_list[i].first_word not in can_be_replaced_list):
                        can_be_replaced_list.append(synonym_list[i].first_word)
                elif (synonym_list[i].second_word in sample_tokenized):
                    candidate_synonym.append(synonym_list[i])
                    if (synonym_list[i].second_word not in can_be_replaced_list):
                        can_be_replaced_list.append(synonym_list[i].second_word)
            
                    
            if (len(candidate_synonym) > 0):
                print('Words that can be replaced:', can_be_replaced_list)
                
                unique_words = len(can_be_replaced_list)
                num_perturbed_words = 0
                
                
                index = 0
                while (num_perturbed_words < max_replace and num_perturbed_words < unique_words):
                    possible_replacement = []
                    
                    for i in range(0, len(candidate_synonym)):
                        if (candidate_synonym[i].first_word == can_be_replaced_list[index] or candidate_synonym[i].second_word == can_be_replaced_list[index]):
                            possible_replacement.append(candidate_synonym[i])
                            
                    temp_list = possible_replacement
                    possible_replacement = []
                    
                    for i in range(0, len(temp_list)):
                        repeat = int(temp_list[i].similarity * 100)
                        for j in range(0, repeat):
                            possible_replacement.append(temp_list[i])
                            
                    random_candidate = return_random_number(0, len(possible_replacement)-1)
                    
                    original_word = ''
                    new_word = ''
                    if (possible_replacement[random_candidate].first_word == can_be_replaced_list[index]):
                        original_word = possible_replacement[random_candidate].first_word
                        new_word = possible_replacement[random_candidate].second_word
                    elif (possible_replacement[random_candidate].second_word == can_be_replaced_list[index]):
                        original_word = possible_replacement[random_candidate].second_word
                        new_word = possible_replacement[random_candidate].first_word
                        
                    print(original_word, 'is replaced by', new_word)
                    
                    perturbed_sample_tokenized = nltk.word_tokenize(perturbed_sample)
                    replacement_position = -1
                    for i in range(0, len(perturbed_sample_tokenized)):
                        if (original_word == perturbed_sample_tokenized[i]):
                            replacement_position = i
                            
                    if (replacement_position > -1):
                        perturbed_sample = ""
                        for i in range(0, replacement_position):
                            perturbed_sample += perturbed_sample_tokenized[i] + ' '
                        perturbed_sample += new_word + ' '
                        for i in range(replacement_position+1, len(perturbed_sample_tokenized)):
                            perturbed_sample += perturbed_sample_tokenized[i] + ' '
                    
                        word_replaced = True
                        num_perturbed_words += 1
                        
                        
                    index += 1
                    
            elif (len(candidate_synonym) == 0):
                print('No word was replaced.')
        
            
            if (word_replaced == True):
                is_sample_perturbed = True
                num_perturbed_samples += 1
            
            print('Perturbed sample:', perturbed_sample)
            
            if (is_sample_perturbed == True):
                output_text += perturbed_sample + '\t' + sample_label + '\n'
            
        
            print('----------------------------------------------------------')
        line_num += 1
        
        
print('\nPerturbed Samples:', num_perturbed_samples)

output_file = open('Dataset\\i2b2-perturbed-word-replace-synonym.tsv', 'w')
output_file.write(output_text)
output_file.close()
        


if __name__ == '__main__':
    pass