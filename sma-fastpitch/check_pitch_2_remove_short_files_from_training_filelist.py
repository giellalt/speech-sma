import sys, glob, os
import torch
import numpy as np

pitchfiles = sorted(glob.glob(sys.argv[1]+"/*.pt"))

# Open the output file
with open('short_files.txt', 'w') as outfile:
    for fname in pitchfiles:
        pitch = torch.load(fname)
        pitch = pitch.cpu().numpy().flatten()
        if len(pitch[pitch>0]) == 0:
            froot = os.path.basename(fname)[:-3]
            print(froot)
            if len(pitch) < 100:
                # Write the file name to the output file
                outfile.write(froot + '\n')
                continue
            os.system("play -q "+"SME-MEGA-TTS/"+froot+".wav")

# Read the list of short files
with open('/home/hiovain/DeepLearningExamples/PyTorch/SpeechSynthesis/FastPitch/short_files.txt', 'r') as f:
    short_files = f.read().splitlines()

# Read the other file list
with open('/home/hiovain/DeepLearningExamples/PyTorch/SpeechSynthesis/FastPitch/filelists/SAMI_MEGA_TTS_FILELIST.txt', 'r') as f:
    other_files = f.read().splitlines()

# Write the files that are not in the list of short files to a new list
with open('/home/hiovain/DeepLearningExamples/PyTorch/SpeechSynthesis/FastPitch/filelists/SME-MEGA-TTS_filtered_file_list.txt', 'w') as f:
    for file in other_files:
        # Check if the line contains any of the short file names
        if not any(short_file in file for short_file in short_files):
            f.write(file + '\n')