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


class Abbreviation:
    
    def __init__(self, input_abbreviation, input_expansion):
        self.abbreviation = input_abbreviation
        self.expansion = input_expansion
        self.start_position = -1

#--------------------------------------------------------------------------------------------------------------------

input_address = 'Abbreviation\\AbbreviationsList.tsv'

abbreviation_list = []

with open(input_address) as input_file:
    input_data = csv.reader(input_file, delimiter='\t')
    
    for row in input_data:
        abbreviation = row[0]
        expansion = row[1]
        
        abbreviation_pair = Abbreviation(abbreviation, expansion)
        abbreviation_list.append(abbreviation_pair)



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
            
            inserted_abbreviation = []
            num_inserted_abbreviations = 0
            
            for i in range(0, len(abbreviation_list)):
                expansion = abbreviation_list[i].expansion
                lower_expansion = expansion.lower()
                lower_sample_text = perturbed_sample.lower()
                start_position = lower_sample_text.find(lower_expansion)
                if (start_position > -1):
                    temp_abbreviation = Abbreviation(abbreviation_list[i].abbreviation, abbreviation_list[i].expansion)
                    temp_abbreviation.start_position = start_position
                    inserted_abbreviation.append(temp_abbreviation)
                    
                    temp_text = perturbed_sample
                    perturbed_sample = temp_text[:start_position]
                    perturbed_sample += abbreviation_list[i].abbreviation
                    perturbed_sample += temp_text[start_position+len(lower_expansion):]
                    word_replaced = True
                    
                    num_inserted_abbreviations += 1
                    
            
                    
            if (len(inserted_abbreviation) > 0):
                print('-----Inserted abbreviations:')
                for i in range(0, len(inserted_abbreviation)):
                    print(inserted_abbreviation[i].expansion, 'was replaced by', inserted_abbreviation[i].abbreviation)
            elif (len(inserted_abbreviation) == 0):
                print('No abbreviation was inserted.')
        
            
            if (word_replaced == True):
                is_sample_perturbed = True
                num_perturbed_samples += 1
            
            print('Perturbed sample:', perturbed_sample)
            
            if (is_sample_perturbed == True):
                output_text += perturbed_sample + '\t' + sample_label + '\n'
            
        
            print('----------------------------------------------------------')
        line_num += 1
        
        
print('\nPerturbed Samples:', num_perturbed_samples)

output_file = open('Dataset\\i2b2-perturbed-word-abbreviation.tsv', 'w')
output_file.write(output_text)
output_file.close()
        


if __name__ == '__main__':
    pass