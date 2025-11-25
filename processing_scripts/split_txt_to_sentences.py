# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on Thu Mar 08 11:44:03 2021

@author: hiovain
"""

s_ind = 1

with open("smjtts11.txt") as f:
    text = f.read()
#    print(text)
    sentences1 = text.split('\n')
#    print(sentences1)
    
    text_per_lines = ""
    
    for s1 in sentences1:
        sentences2 = s1.split('. ')
        for s2 in sentences2:
            if len(s2) > 0:
                s_ind_str = '000' + str(s_ind)
                s_ind_str = s_ind_str[-3:]
                file_object = open("smjtts11_" + s_ind_str + ".txt","w")
                file_object.write(s2)
                file_object.close()
                s_ind += 1
                print(s2)
                text_per_lines = text_per_lines + s2 + ".\n"
                
with open("smjtts11_out.txt" ,"w") as f_out:
    f_out.write(text_per_lines)
    
#    text_per_lines = text_per_lines + s2 + END_UTT + "\n" 
#    END_UTT = "." 