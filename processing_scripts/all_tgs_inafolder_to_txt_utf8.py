#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:34:16 2021

@author: hiovain
"""

# Katri Hiovain-Asikainen (Divvun), August 2021
# Input: a textgrid with 1 tier named ORT-MAU
# output: utf-8 .txt file containing the text from selected TG tier, saved as corresponding to the .TextGrid

# ------------------------------------------------------------
import os
import tgt

# Fill in
output_dir = "/home/hiovain/Desktop/code_test/tgt_to_txt/txt"
os.makedirs(output_dir, exist_ok=True)

# 0.1 loop through all textgrids in a folder
tgt_dir = "/home/hiovain/Desktop/code_test/tgt_to_txt/tgts"
file_list = os.listdir(tgt_dir)

for tg in file_list:
# for each path stored in the filelist; set the variable tg to the current path
    if not tg.endswith(".TextGrid"):
        continue

    # 1. load the textgrid

    try:
        the_tgt = tgt.io.read_textgrid(os.path.join(tgt_dir, tg), encoding="utf-8")
    except UnicodeError:
        the_tgt = tgt.io.read_textgrid(os.path.join(tgt_dir, tg), encoding="utf-16")
        basename = os.path.basename(tg)
        
    # 2. load the sentence tier
    tier_sents = the_tgt.get_tier_by_name("Sent2")

    # create list of sentences (intervals) from sent_tier
    
    list_sentences = []
    start_sent = 0

    # for all the sentences:
    for id_sent, sent_inter in enumerate(tier_sents.intervals):
        # Building filenames
        basename_txt = basename.replace(".TextGrid", ".txt")
        text = sent_inter.text

        # Retrieve interval elements
        start_s = sent_inter.start_time
        end_s = sent_inter.end_time
#        text = sent_inter.text

        # Ignore empty intervals
#        if text == "":
#            continue

        tgt.write_to_file(the_tgt, os.path.join(output_dir, basename_txt), format="long", encoding="utf-8")

            # Extract the text
        with open(os.path.join(output_dir, basename_txt), "w") as f_out:
            f_out.write(text)
