#--------------------------
# Kayla Kempers - 171429390
# CP460 (Fall 2019)
# Assignment 2
#--------------------------

import math
from utilities_A2 import *
import re

#---------------------------------
#Q1: Vigenere Cipher (Version 2) #
#---------------------------------
#-------------------------------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (str): string of any length
# Return:       ciphertext (string)
# Description:  Genereic Encryption scheme using Vigenere Cipher
#               calls proper function depending on key length
#               if len(key) == 1 --> call e_vigenere1
#               else --> call e_vigenere2
#               If invalid key (not string or empty string or non-alpha string) -->
#                   print error and return '',''
#---------------------------------------------------------------------------------------
def e_vigenere(plaintext,key):
    if not isinstance(key,str) or key == '' or not key.isalpha():
        print('Error (e_vigenere): invalid key!')
        return ''
    key = key.lower()
    if len(key) == 1:
        return e_vigenere1(plaintext,key)
    else:
        return e_vigenere2(plaintext,key)

#-------------------------------------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (str): string of anylength
# Return:       ciphertext (string)
# Description:  Genereic Encryption scheme using Vigenere Cipher
#               calls proper function depending on key length
#               if len(key) == 1 --> call d_vigenere1
#               else --> call d_vigenere2
#               If invalid key (not string or empty string or contains no alpha char) -->
#                   print error and return '',''
#---------------------------------------------------------------------------------------
def d_vigenere(ciphertext,key):
    if not isinstance(key,str) or key == '' or not key.isalpha():
        print('Error (d_vigenere): invalid key!')
        return ''
    key = key.lower()
    if len(key) == 1:
        return d_vigenere1(ciphertext,key)
    else:
        return d_vigenere2(ciphertext,key)

#-------------------------------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (str): single character
# Return:       ciphertext (string)
# Description:  Encryption using Vigenere Cipher (Polyalphabetic Substitituion)
#               Non alpha characters --> no substitution
#               Algorithm preserves case of the characters
#---------------------------------------------------------------------------------------
def e_vigenere1(plaintext, key):
    square = get_vigenereSquare()

    ciphertext = ''
    for char in plaintext:
        if char.lower() in square[0]: #this position is the alphabet
            plainIndx = square[0].index(char.lower())
            keyIndx = square[0].index(key)
            cipherChar = square[keyIndx][plainIndx] # square at specified indices
            ciphertext += cipherChar.upper() if char.isupper() else cipherChar
            key = char.lower() # key is now the lowercase version of where we found the plaintext
                #becomes the key for the next round
        else:
            ciphertext += char #anything that isn't alpha is translated as it is (no encryption/change)

    return ciphertext

#-------------------------------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (str): a phrase
# Return:       ciphertext (string)
# Description:  Encryption using Vigenere Cipher (Polyalphabetic Substitituion)
#               Non alpha characters --> no substitution
#               Algorithm preserves case of the characters
#---------------------------------------------------------------------------------------
def e_vigenere2(plaintext, key):
    square = get_vigenereSquare()
    alph = square[0]
    ciphertext = ''
    
    for a in plaintext:
        i = 1
        for char in key:
            newTest = alph[alph.index(char.lower()):] + alph[:alph.index(char.lower())]
            for t in plaintext:
                if alph.count(t) == 1 :
                    ciphertext += newTest[alph.index(t)]
                    plaintext = plaintext[i:]
                    break
                elif alph.count(t.lower()) == 1:
                    ciphertext += newTest[alph.index(t.lower())].upper()
                    plaintext = plaintext[i:]
                    break
                else:
                    ciphertext += t
                    plaintext = plaintext[i:]
                    break
                i += 1
    return ciphertext

    
#-------------------------------------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (str): single character
# Return:       ciphertext (string)
# Description:  Decryption using Vigenere Cipher (Polyalphabetic Substitituion)
#               Non alpha characters --> no substitution
#               Algorithm preserves case of the characters
#---------------------------------------------------------------------------------------
def d_vigenere1(ciphertext, key):
    square = get_vigenereSquare()

    plaintext = ''
    for char in ciphertext:
        if char.lower() in square[0]:
            keyIndx = square[0].index(key)
            plainIndx = 0
            for i in range(26):
                if square[i][keyIndx] == char.lower():
                    plainIndx = i
                    break
            plainChar = square[0][plainIndx]
            key = plainChar
            plaintext += plainChar.upper() if char.isupper() else plainChar
        else:
            plaintext += char
    return plaintext

#-------------------------------------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (str): a phrase
# Return:       ciphertext (string)
# Description:  Decryption using Vigenere Cipher (Polyalphabetic Substitituion)
#               Non alpha characters --> no substitution
#               Algorithm preserves case of the characters
#---------------------------------------------------------------------------------------
def d_vigenere2(ciphertext, key):
    square = get_vigenereSquare()
    alph = square[0]
    plaintext = ''
    for a in ciphertext:
        i = 1
        for char in key:
            newTest = alph[alph.index(char.lower()):] + alph[:alph.index(char.lower())]
            for t in ciphertext:
                if alph.count(t) == 1 :
                    plaintext += alph[newTest.index(t)]
                    ciphertext = ciphertext[i:]
                    break
                elif alph.count(t.lower()) == 1:
                    plaintext += alph[newTest.index(t.lower())].upper()
                    ciphertext = ciphertext[i:]
                    break
                else:
                    plaintext += t
                    ciphertext = ciphertext[i:]
                    break
                i += 1      
    return plaintext


##### every second word is encrypted incorrectly but decrypted correctly I'M SO CONFUSED WHAT DID I DO


#-------------------------------------
#Q2: Vigenere Crytanalysis Utilities #
#-------------------------------------

#-----------------------------------------------------------------------------
# Parameters:   text (string)
#               size (int)
# Return:       list of strings
# Description:  Break a given string into strings of given size
#               Result is provided in a list
#------------------------------------------------------------------------------
def text_to_blocks(text,size):
    
    blocks = []

    #Blocks list gets every chunk shifted by block size in range of the text
    for i in range(0, len(text), size):
        blocks.append(text[i: i + size])
    
    return blocks

#-----------------------------------
# Parameters:   text (string)
# Return:       modifiedText (string)
# Description:  Removes all non-alpha characters from the given string
#               Returns a string of only alpha characters upper case
#-----------------------------------
def remove_nonalpha(text):
    #sub every non-alpha char for an empty string in text
    modifiedText = (re.sub("[^a-zA-Z]", "", text)).upper()
    return modifiedText

#-------------------------------------------------------------------------------------
# Parameters:   blocks: list of strings
# Return:       baskets: list of strings
# Description:  Assume all blocks have same size = n (other than last block)
#               Create n baskets
#               In basket[i] put character #i from each block
#---------------------------------------------------------------------------------------
def blocks_to_baskets(blocks):
    baskets = []
    setLen = len(blocks[0])

    
    for j in range(setLen): #for 0-2 (3 spots)
        baskets.append("")
        for i in blocks: #check every block
            if len(i) == setLen: #check that we aren't at the one shorter block at the end
                baskets[j] = baskets[j] + i[j]
            else:
                baskets[j] = baskets[j] + ""

            ##disregarding the last short block, need to redo code so this block is included
 
    
    
    return baskets

#----------------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       I (float): Index of Coincidence
# Description:  Computes and returns the index of coincidence 
#               for a given text
#----------------------------------------------------------------
def get_indexOfCoin(ciphertext):
    square = get_vigenereSquare()
    alph = square[0]
    
    cLen = float(len(ciphertext))
    aList = list(alph)

    I = 0
    for j in range(len(aList)) : 
      I += (ciphertext.count(alph[j].upper()) * (ciphertext.count(alph[j].upper()) - 1))
    
    I = I * (1/ (cLen * (cLen - 1)))
    return I


#----------------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       key length (int)
# Description:  Uses Friedman's test to compute key length
#               returns key length rounded to nearest integer
#---------------------------------------------------------------
def getKeyL_friedman(ciphertext):
    k = 0
    
    cLen = len(ciphertext)
    i = get_indexOfCoin(ciphertext)
    k = round(cLen * (0.027)/((cLen-1)*i + 0.0655 - 0.0385 * cLen))

    return k

#----------------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       key length (int)
# Description:  Uses the Ciphertext Shift method to compute key length
#               Attempts key lengths 1 to 20
#---------------------------------------------------------------
def getKeyL_shift(ciphertext):

    matches = 0
    maxMatches = 0
    test = 0
    k = -1
    cShifted = shift_string(ciphertext,1,'r') #shift once
    print(cShifted)
    for i in range(1,20):
        for x in range(len(ciphertext)):
            for j in ciphertext:
                if j == cShifted[test]:
                    matches += 1
                    
                cShifted = shift_string(cShifted,1,'r')
        if matches > maxMatches:
            maxMatches = matches
            k = i
        matches = 0
        
    return k


#---------------------------------
#   Q3:  Block Rotate Cipher     #
#---------------------------------
#-----------------------------------------------------------
# Parameters:   key (b,r)
# Return:       updatedKey (b,r)
# Description:  Assumes given key is in the format of (b(int),r(int))
#               Updates the key in three scenarios:
#               1- The key is too big (use modulo)
#               2- The key is negative
#               if an invalid key is given print error message and return (0,0)
#-----------------------------------------------------------
def adjustKey_blockRotate(key):
    updatedKey = ()
    if type(key) is not tuple:
        print("Error: invalid key")
        return (0,0)
    testB = key[0]
    testR = key[1]
    if type(testB) is not int or type(testR) is not int:
        print("Error: invalid key")
        return (0,0)
    if key[0] <= 0:
        print("Error: invalid key")
        return (0,0)
    if key[1] > key[0]: #if r > b
        updatedKey = (key[0], key[1] % key[0])
    if key[1] < 0:
        updatedKey = (key[0], key[1] + key[0])
 
    return updatedKey

#-----------------------------------
# Parameters:   text (string)
# Return:       nonalphaList (2D List)
# Description:  Analyzes a given string
#               Returns a list of non-alpha characters along with their positions
#               Format: [[char1, pos1],[char2,post2],...]
#               Example: get_nonalpha('I have 3 cents.') -->
#                   [[' ', 1], [' ', 6], ['3', 7], [' ', 8], ['.', 14]]
#-----------------------------------
def get_nonalpha(text):
    nonalphaList = []

    indx = 0
    for i in range(len(text)):
      
        if not text[i].isalpha():  
            nonalphaList.append([text[indx],i])
        indx += 1
    
    return nonalphaList

#-----------------------------------
# Parameters:   text (str)
#               2D list: [[char1,pos1], [char2,pos2],...]
# Return:       modifiedText (string)
# Description:  inserts a list of nonalpha characters in the positions
#-----------------------------------
def insert_nonalpha(text, nonAlpha):
    modifiedText = ""
    textList = []
    
    for i in text:
        textList.append(i) #list of chrs in text

    for j in range(len(nonAlpha)):
        indx = int(nonAlpha[j][1])
        if nonAlpha[j][1] >= len(textList):
            textList.append(nonAlpha[j][0])
        else:
            textList[indx] = nonAlpha[j][0]

    for k in textList:
        modifiedText += str(k)
    
    return modifiedText

#-----------------------------------------------------------
# Parameters:   plaintext (string)
#               key (b,r): (int,int)
# Return:       ciphertext (string)
# Description:  break plaintext into blocks of size b
#               rotate each block r times to the left
#-----------------------------------------------------------
def e_blockRotate(plaintext,key):
    ciphertext = ""
    pNew = text_to_blocks(plaintext,key[0])
    #pNew is list of blocks

    for i in pNew:
        i = shift_string(i,key[1],"l")
        ciphertext += i

                        
    return ciphertext

#-----------------------------------------------------------
# Parameters:   ciphertext (string)
#               key (b,r): (int,int)
# Return:       plaintext (string)
# Description:  Decryption using Block Rotate Cipher
#-----------------------------------------------------------
def d_blockRotate(ciphertext,key):
    plaintext = ""
    pNew = text_to_blocks(ciphertext,key[0])
    for i in pNew:
        i = shift_string(i,key[1],"r")
        plaintext += i
    
    return plaintext

#-----------------------------------------------------------
# Parameters:   ciphertext (string)
#               b1 (int): starting block size
#               b2 (int): end block size
# Return:       plaintext,key
# Description:  Cryptanalysis of Block Rotate Cipher
#               Returns plaintext and key (r,b)
#               Attempts block sizes from b1 to b2 (inclusive)
#               Prints number of attempts
#-----------------------------------------------------------
def cryptanalysis_blockRotate(ciphertext,b1,b2):
    for i in range(b1, b2):
        plaintext = ""
    return plaintext,key

#---------------------------------
#       Q4: Cipher Detector     #
#---------------------------------
#-----------------------------------------------------------
# Parameters:   ciphertext (string)
# Return:       cipherType (string)
# Description:  Detects the type of a given ciphertext
#               Categories: "Atbash Cipher, Spartan Scytale Cipher,
#                   Polybius Square Cipher, Shfit Cipher, Vigenere Cipher
#                   All other ciphers are classified as Unknown. 
#               If the given ciphertext is empty return 'Empty Ciphertext'
#-----------------------------------------------------------
def get_cipherType(ciphertext):
    if ciphertext == "":
        return ""
    else:
        return ciphertext

        
    return cipherType

#-------------------------------------
#  Q5: Wheastone Playfair Cipher     #
#-------------------------------------
#-----------------------------------------------------------
# Parameters:   plaintext (string)
# Return:       modifiedPlain (string)
# Description:  Modify a plaintext through the following criteria
#               1- All non-alpha characters are removed
#               2- Every 'W' is translsated into 'VV' double V
#               3- Convert every double character ## to #X
#               4- if the length of text is odd, add X
#               5- Output is formatted as pairs, separated by space
#                   all upper case
#-----------------------------------------------------------
def formatInput_playfair(plaintext):
    modText = []
    modifiedPlain = ""
    modifiedText = (re.sub("[^a-zA-Z]", "", plaintext)).upper()
    
    for i in modifiedText:
        modText.append(i) #get list of upepr alpha letters
        
    for j in range(len(modText)):
        if modText[j] == "W":
            modText[j] = "VV"

        if j+1 != len(modText):
            if modText[j] == modText[j+1]:
                modText[j+1] = "X"

    if len(modText)%2 != 0:
        modText.append("X")

    count = 0
    for k in range(0, len(modText), 2):
            modifiedPlain += modText[0+k]
            modifiedPlain += modText[1+k]
            modifiedPlain += " "
 
    return modifiedPlain

#-------------------------------------------------------------------------------------
# Parameters:   plaintext(string)
#               key: playfair Square (2D List)
# Return:       ciphertext (string)
# Description:  Encryption using Wheatstone Playfair Cipher
#---------------------------------------------------------------------------------------
def e_playfair(plaintext, key):
    square = get_playfairSquare()
    
    return ciphertext

#-------------------------------------------------------------------------------------
# Parameters:   plaintext(string)
#               key: playfair Square (2D List)
# Return:       ciphertext (string)
# Description:  Decryption using Wheatstone Playfair Cipher
#-------------------------------------------------------------------------------
def d_playfair(ciphertext, key):
    # your code here
    return plaintext
