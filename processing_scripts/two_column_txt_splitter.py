# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 13:44:03 2018

@author: hiovain
"""

#import sys
import os
import csv

s_ind = 0

with open('testi_taulukko_1.txt') as f:
    text = f.read()
#    print(text)
    sentences1 = text.split('\n')
#    print(sentences1)


#[square brackets: COLUMNS; SPLIT ROWS TWICE]
#(separate by tab: \t)
#1:-1: from second (ignore headers): to second last: ignore empty rows at the end)    
    for s1 in sentences1[1:-1]:
        sentences2 = s1.split('\t')
        filename=sentences2[0]
        content=sentences2[1]
        file_object = open("ee_" + filename + ".txt","w")
        file_object.write(content)
        file_object.close()
        
        
