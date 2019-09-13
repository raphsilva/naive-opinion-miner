# -*- coding: utf-8 -*-


#   This script reads the crawled data. 

#   Each file has the name ID.txt, where ID is the product ID.

#   Each entry in the file has the format: 
#   REVIEW_ID.SENTENCE_ID   ::  SENTENCE FROM REVIEW

#   Before each review, there is a line starting with the symbol * that indicates the rating made by the reviewer. 

#   Additionally, each file may contain: 
#       Metadata (extra information) in lines sarting with >
#       Comments (bypassed text) in lines starting with #
#       Dates in lines starting with @ (thay indicate when the subsequent reviews where published)


# Made by: Raphael Rocha da Silva
# October 2018
# VERSION: 2018-10-16




import io
import os
import json
from pprint import pprint
from pprint import pformat



SENTENCE_BEGIN_INDICATOR = '::' # Symbol used to indicate the beginning of a sentence in the data files. 



# Definition of directories 
path_DATA = '../DATA/raw' # Path to the main data folder



# Extracts the product ID from a filename in string format.
def getIDfromFilename(filename):
    return filename.split('/')[-1].split('.')[0]



# Removes any spaces in the beginning or end of a string; transforms double spaces into single spaces. 
def cleanExtraSpaces(text):
    r = text
    while len(r) > 0 and r[0] == ' ':
        r = r[1:]
    while len(r) > 0 and r[-1] == ' ':
        r = r[:-1]
    return r.replace('  ', ' ')



# Returns metadata of a product datafile. 
def getMetadata(filename):    
    data = io.open(filename, 'r', encoding="utf-8").read()
    r = {}
    for line in data.splitlines():
        if len(line) == 0:
            continue
        if line[0] == '>':
            if ':' not in line: 
                print("STRANGE LINE IN FILE %s. PLEASE CHECK: " % filename)
                print(line)
                input("ENTER TO CONTINUE...")
                print('\r')
            line = line.replace('> ', '')
            meta_key = cleanExtraSpaces(line.split(':')[0])
            meta_value = cleanExtraSpaces(''.join([i for i in line.split(':')[1:]]))
            r[meta_key] = meta_value
            continue  
    return r



# Reads a tagged file and returns its data information as a list of dictionaries
def getData(filename):
    r = []
    data = io.open(filename, 'r', encoding="utf-8").read()
    
    review_date = None
    review_rate = None
    review_upvotes = None
    review_downvotes = None
    
    for line in data.splitlines():
        
        flag = ''
        
        # Skip blank lines
        if len(line) == 0:
            continue
        
        # Skip comments and metadata
        elif line[0] in ['#', '>']:
            continue
        
        elif line[0] == '@': # Update date 
            review_date = line[2:]
            continue
        
        elif line[0] == '*':
            review_rate = int(line[2])
            votes = line[3:].replace('-','').replace('+','').split()
            review_upvotes = int(votes[0])
            review_downvotes = int(votes[1])
            
            continue
        
        elif not line[0].isdigit():
            flag = line[0]
            line = line[2:]
                        
        # Break a data entry into 'sentence' (text from review) and 'info' (polarity and aspect)
        sentence_text = line.split(SENTENCE_BEGIN_INDICATOR)[-1]        
        sentence_id = line.split(SENTENCE_BEGIN_INDICATOR)[0].replace(' ', '')
        
        n = {} # New entry
        
        n['id'] = sentence_id        
            
        n['sentence'] = cleanExtraSpaces(sentence_text)
        
        n['date'] = review_date
        
        n['rate'] = review_rate
        
        n['flag'] = flag
        
        n['upvotes'] = review_upvotes
        n['downvotes'] = review_downvotes

        r.append(n)
        
    return r

          
          
 
# Used to format output text  
class oformat:
    def bold(text):
        return '\33[1m' + text + '\33[0m' 
    def gray(text):
        return '\33[90m' + text + '\33[0m' 
    def green(text):
        return '\33[32m' + text + '\33[0m' 
    def data(text):
        try:
            text = pformat(text)
        except:
            pass
        return text





def read(path_DATA=path_DATA):
    
    r = []

    # Gets the file names 
    files_to_read = []
    list_of_files = os.listdir(path_DATA) # List of data files already saved in the disk
    for i in list_of_files:
        i_filename = i.split('.')[0] # Get filename without extension, which is that product's ID
        if i_filename.isdigit() == True: # If filename is not a number, then it's not actually a product data file.
            files_to_read.append(i)


    # Main script
    for filename in files_to_read: # Each file contains data of a different product    
        
        productID = getIDfromFilename(filename) 
        
        meta = getMetadata(path_DATA + '/' + filename)
        
        data = getData(path_DATA + '/' + filename)

        #r[productID] = {}
        #r[productID]['data'] = data
        #r[productID]['meta'] = meta
        
        r.append({'data': data, 'meta': meta})
        
    return r
            
        
        
        
if __name__ == "__main__":        
    info = read()

    for i in info:
        print (oformat.bold("Information from product #%s" % (i)))
        input(oformat.gray("Will show metadata:  [PRESS ENTER]"))
        print(oformat.data(info[i]['meta']))
        
        input(oformat.gray("Will show data separated by excerpts:  [PRESS ENTER]"))
        print(oformat.data(info[i]['data']))
        print()   
        
        print()
        input(oformat.gray('PRESS ENTER TO GO TO THE NEXT PRODUCT'))
        
    
    
