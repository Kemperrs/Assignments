#--------------------------
# Kayla Kempers - 171429390
# CP460 (Fall 2019)
# Assignment 1
#--------------------------


import math
import string
import re

#---------------------------------
#       Given Functions          #
#---------------------------------
#-----------------------------------------------------------
# Parameters:   fileName (string)
# Return:       contents (string)
# Description:  Utility function to read contents of a file
#               Can be used to read plaintext or ciphertext
#-----------------------------------------------------------
def file_to_text(fileName):
    inFile = open(fileName,'r')
    contents = inFile.read()
    inFile.close()
    return contents

#-----------------------------------------------------------
# Parameters:   text (string)
#               filename (string)            
# Return:       none
# Description:  Utility function to write any given text to a file
#               If file already exist, previous content will be over-written
#-----------------------------------------------------------
def text_to_file(text, filename):
    outFile = open(filename,'w')
    outFile.write(text)
    outFile.close()
    return

#-----------------------------------------------------------
# Parameters:   r: #rows (int)
#               c: #columns (int)
#               pad (str,int,double)
# Return:       empty matrix (2D List)
# Description:  Create an empty matrix of size r x c
#               All elements initialized to pad
#               Default row and column size is 2
#-----------------------------------------------------------
def new_matrix(r,c,pad):
    r = r if r >= 2 else 2
    c = c if c>=2 else 2
    return [[pad] * c for i in range(r)]

#-----------------------------------------------------------
# Parameters:   marix (2D List)
# Return:       None
# Description:  prints a matrix each row in a separate line
#               Assumes given parameter is a valid matrix
#-----------------------------------------------------------
def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j],end='\t')
        print()
    return
#-----------------------------------------------------------
# Parameters:   marix (2D List)
# Return:       text (string)
# Description:  convert a 2D list of characters to a string
#               left to right, then top to bottom
#               Assumes given matrix is a valid 2D character list
#-----------------------------------------------------------
def matrix_to_string(matrix):
    text = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            text+=matrix[i][j]
    return text

#--------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (string)
# Return:       ciphertext (string)
# Description:  Encryption using Scytale Cipher
#               Key is the diameter, i.e. # rows
#               Assume infinte length rod (infinte #columns)
#--------------------------------------------------------------
def e_scytale(plaintext, key):
    # By definition, number of rows is key
    r = int(key)
    # number of columns is the length of ciphertext/# rows    
    c = int(math.ceil(len(plaintext)/key))
    # create an empty matrix for ciphertext rxc
    cipherMatrix = new_matrix(r,c,"")

    # fill matrix horizontally with characers, pad empty slots with -1
    counter = 0
    for i in range(r):
        for j in range(c):
            cipherMatrix[i][j] = plaintext[counter] if counter < len(plaintext) else -1
            counter+=1

    #convert matrix into a string (vertically)
    ciphertext = ""
    for i in range(c):
        for j in range(r):
            if cipherMatrix[j][i]!=-1:
                ciphertext+=cipherMatrix[j][i]
    return ciphertext


###############################################################################################################




#   Developed Functions          #
#---------------------------------
#       Problem 1                #
#---------------------------------
      
#----------------------------------------------------
# Parameters:   ciphertext(string)
#               key (string)
# Return:       plaintext (string)
# Description:  Decryption using Scytale Cipher
#               Assumes key is a valid integer in string format             
#---------------------------------------------------
def d_scytale(ciphertext, key):
    plaintext = ''

    numCols = len(ciphertext) // int(key) + 1 #to determine grid size
    spaces = (numCols*int(key)) - len(ciphertext) #to determine how many spaces will be present

    if spaces > numCols: #too many spaces means not correct key
        return ""
    else:
        for i in range(int(key)):
            j = i
            counter = 0
        
            while j < len(ciphertext) and len(plaintext) < len(ciphertext):
                if counter < (numCols-spaces):
                    plaintext=plaintext+ciphertext[j]
                    j = j+(int(key))
      
                else:
                    plaintext=plaintext+ciphertext[j]
                    j = j+(int(key)-1)
              
                counter += 1
        

        return plaintext
    

#---------------------------------
#       Problem 2                #
#---------------------------------

#-----------------------------------------------------------
# Parameters:   dictFile (string): filename
# Return:       list of words (list)
# Description:  Reads a given dictionary file
#               dictionary file is assumed to be formatted: each word in a separate line
#               Returns a list of strings, each pertaining to a dictionary word
#-----------------------------------------------------------
def load_dictionary(dictFile):
    dictList = []

    fp = open(dictFile, 'r', encoding="mbcs")
    
    dictList = fp.readlines()
    
    for x in range(len(dictList)):  
        dictList[x] = dictList[x].strip()

    fp.close()
    return dictList

#-------------------------------------------------------------------
# Parameters:   text (string)
# Return:       list of words (list)
# Description:  Reads a given text
#               Each word is saved as an element in a list. 
#               Returns a list of strings, each pertaining to a word in file
#               Gets rid of all punctuation at the start and at the end 
#-------------------------------------------------------------------
def text_to_words(text):
    wordList = []
    wordList = text.split()

    for x in range(len(wordList)):
        # return if there is a char that's not in the alphabet at the beginning or end
        #of a word
        wordList[x] = re.sub("\B[^a-zA-Z0-9_]",'', wordList[x])  #/W
        wordList[x] = re.sub("[^a-zA-Z0-9_]\B",'', wordList[x])

        
        #! below method keeps removing middle punctuation, not just beginning and end
        #wordList[x] = wordList[x].translate(str.maketrans('', '', string.punctuation))
                
        

    return wordList


#-----------------------------------------------------------
# Parameters:   text (string)
#               dictFile (string): dictionary file
# Return:       (#matches, #mismatches)
# Description:  Reads a given text, checks if each word appears in dictionary
#               Returns a tuple of number of matches and number of mismatches.
#               Words are compared in lowercase.
#-----------------------------------------------------------
def analyze_text(text, dictFile):
    matches = 0
    mismatches = 0

    wordList = text_to_words(text)
    dictionary = load_dictionary(dictFile) #now have two lists

    for word in wordList:
        if word.lower() in dictionary: matches += 1
        else: mismatches += 1

 
    return(matches,mismatches)

#-----------------------------------------------------------
# Parameters:   text (string)
#               dictFile (string): dictionary file
#               threshold (float): number between 0 to 1
# Return:       True/False
# Description:  Check if a given file is a plaintext
#               If #matches/#words >= threshold --> True
#                   otherwise --> False
#               If invalid threshold given, default is 0.9
#               An empty string is assumed to be non-plaintext.
#-----------------------------------------------------------
def is_plaintext(text, dictFile, threshold):
    if threshold > 1 or threshold < 0: threshold = 0.9

    if text == "":
        return False
    else:
        matches, mismatches = analyze_text(text, dictFile)
        if (matches/(matches + mismatches)) >= threshold:
            return True
        else:
            return False

#---------------------------------
#       Problem 3                #
#---------------------------------
      
#----------------------------------------------------
# Parameters:   cipherFile (string)
#               dictFile (string)
#               startKey (int)
#               endKey (int)
#               threshold (float)
# Return:       key (string)
# Description:  Apply brute-force to break scytale cipher
#               Valid key range: 2-100 (if invalid --> print error msg and return '')
#               Valid threshold: 0-1 (if invalid --> print error msg and return '')
#               If decryption is successful --> print plaintext and return key
#               If decrytpoin fails: print error msg and return ''
#---------------------------------------------------
def cryptanalysis_scytale(cipherFile, dictFile, startKey, endKey, threshold):

    fp = open(cipherFile, 'r', encoding="mbcs")
    cFile = fp.read()

    fp.close()

    
    if startKey < 2 or endKey > 100:
        print("Error, the key range is invalid")
        return ''
    if threshold > 1 or threshold < 0:
        print("Error, the threshold is invalid")
        return ''

    for x in range(startKey, endKey):
        print("Checking key: ", x)
        plainText = d_scytale(cFile, x) #plaintext given ciphertext and key
        textCheck = is_plaintext(plainText, dictFile, threshold)
        if textCheck:
            print("\nKey found: ", x)
            key = x
            break
    
    if textCheck:
        print(plainText)
        return key
    else:
        print("Error, could not decrypt (no key found)")
        return ''

#---------------------------------
#       Problem 4                #
#---------------------------------
      
#----------------------------------------------------
# Parameters:   None
# Return:       polybius_square (string)
# Description:  Returns the following polybius square
#               as a sequential string:
#               [1] [2]  [3] [4] [5] [6] [7] [8]
#           [1]      !    "   #   $   %   &   '
#           [2]  (   )    *   +   '   -   .   /
#           [3]  0   1    2   3   4   5   6   7
#           [4]  8   9    :   ;   <   =   >   ?
#           [5]  @   A    B   C   D   E   F   G
#           [6]  H   I    J   K   L   M   N   O
#           [7]  P   Q    R   S   T   U   V   W
#           [8]  X   Y    Z   [   \   ]   ^   _
#---------------------------------------------------
def get_polybius_square():
    polybius_square = ''

    for i in range(31, 96):
        polybius_square = polybius_square + chr(i)
    
    return polybius_square

#--------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (none)
# Return:       ciphertext (string)
# Description:  Encryption using Polybius Square
#--------------------------------------------------------------
def e_polybius(plaintext, key):
    ciphertext = ''
    pSquare = get_polybius_square()

    # !"#$%&'
    #()*+,-./
    #01234567
    #89:;<=>?
    #@ABCDEFG
    #HIJKLMNO
    #PQRSTUVW
    #XYZ[\]^_

    uText = plaintext.upper()

    for i in uText:
        if i == "\n": #try if i == 'r/n'
            ciphertext = ciphertext + "\r\n"
        else:
            indx = pSquare.index(i)
            row = int((ord(i) - ord(' ')) / 8) + 1
            col = ((ord(i) - ord(' ')) % 8) + 1
            ciphertext += str(row) + str(col)


    return ciphertext

#---------------------------------
#       Problem 5                #
#---------------------------------

#-------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (none)
# Return:       plaintext (string)
# Description:  Decryption using Polybius Square Cipher
#               Detects invalid ciphertext --> print error msg and return ''
#               Case 1: #of chars (other than \n) is not even
#               Case 2: the ciphertext contains non-numerical chars (except \n')
#-------------------------------------------------------
def d_polybius(ciphertext, key):
    plaintext = ''
    pSquare = get_polybius_square()

    cipherCheck = []
    for i in ciphertext:
        if i != "\n":
            cipherCheck.append(i)


    if len(cipherCheck) % 2 == 0:
    

        i = 0
        while i < len(ciphertext):
            if ciphertext[i] == "\n":
                plaintext += "\r\n"
                i += 1
            else:
                if ciphertext[i].isnumeric():
                    row = int(ciphertext[i])
                    col = int(ciphertext[i+1])

                    indx = row*8 - (8-col)

                    plaintext += pSquare[indx]

                    i += 2 #increment by 2 each time
                else:
                    print("Error; invalid ciphertext. Decryption failed.")
                    return ''

    else:
        print("Error; invalid ciphertext. Decryption failed.")
        return ''
        

    return plaintext
    



