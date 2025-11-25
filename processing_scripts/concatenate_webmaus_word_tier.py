# Input: a textgrid with 1 tier named ORT-MAU, word level segmented
# output: the textgrid with an additional tier named sent containing the sentence

# sentence = concatenation of words (joined with a space ) with a full stop appended at the end

# ------------------------------------------------------------
import os
import tgt


# 0. loop through all textgrids in a folder
tgt_dir = "/home/hiovain/speech-smj-private/speech-smj-minicorpus/tjaktjalasta"
file_list = os.listdir(tgt_dir)

for tg in file_list:
# for each path stored in the filelist; set the variable tg to the current path
#    print(tg)
    if not tg.endswith(".TextGrid"):
        continue
    # 1. load the textgrid

    the_tgt = tgt.io.read_textgrid(os.path.join(tgt_dir, tg), encoding="utf-8")
    # print the textgrid that is going to be modified

# 2. load the words <=> How to get the tier "ORT-MAU"
    tier_words = the_tgt.get_tier_by_name("ORT-MAU")

# 3. generate the sentence tier content (list of intervals)
#  What is an interval, (start, end, text)
#    start = start of the FIRST word
#    end = end of the LAST word
#    text = concatenation of all words between the first and the last

# Boundary value in ms (parameter!)
    sentence_separator_threshold = 0.6
    previous_end = -sentence_separator_threshold + 10
    list_sent_words = []
    list_sentences = []
    start_sent = 0


# for all the intervals:
    for word_inter in tier_words.intervals:
    # IS the word opening interval
        if (word_inter.start_time - previous_end) > sentence_separator_threshold:
        # Generate the sentence interval
            sent_text = " ".join(list_sent_words) + "."
            sent = tgt.Interval(start_sent, previous_end, sent_text)
            list_sentences.append(sent)
        # Save the start
            start_sent = word_inter.start_time
        # Reinitialize the list
            list_sent_words = [word_inter.text]
        # Or not...
        else:
            list_sent_words.append(word_inter.text)

        # Save the soon to become the previous end
        previous_end = word_inter.end_time

    # Generate last sentence interval
    if list_sent_words:
        sent_text = " ".join(list_sent_words) + "."
        sent = tgt.Interval(start_sent, tier_words.intervals[-1].end_time, sent_text)
        list_sentences.append(sent)

    # 4. creating the new tier
    # print(list_sentences)
    sent_tier = tgt.IntervalTier(tier_words.start_time, tier_words.end_time, "Sent2", list_sentences)
    the_tgt.add_tier(sent_tier)

    # 5. saving the textgrid
    tgt.io.write_to_file(the_tgt, os.path.join(tgt_dir, tg), format="long", encoding="utf-8")
