Pre-processing of the smj training data:

0) Before doing anything else, normalize texts (numbers, abbreviations etc..) and edit the text so that it corresponds to everything the reader has read: add repetitions and hesitations to the text! OR cut them if possible.

1) Force-align with accurate texts.

2) Make sure the .wav files are 16bit and 48 kHz. Denoise with Audacity or Praat if needed.

3) Split the .txt files to individual sentences. (Python script: split_txt_to_sentences.py or the .praat script which does everything). Check that the TextGrids dont have "" characters in them.
The double quotations can be replaces with single ones.

4) Split the .wav files to corresponding sentence snippets. Force-aligning beforehand helps tremendously to find the relevant splits. Splitting can be done e.g. with Praat script (save_intervals_to_wavs_and_TGs_index).

5) Make sure the .wav & .txt pairs are identically named and the naming conventions are corresponding: e.g. smjtts11_001.wav <-> smjtts11_001.txt <-> smjtts11_001.TextGrid

6) Convert texts / make another versions of the .txt files with IPA (or SAMPA?) characters MAKE SURE the .txt files are in UTF-8. If not, they need to be converted!!

See: https://www.fon.hum.uva.nl/praat/manual/Unicode.html
go to Text writing preferences... in the Preferences submenu of the Praat menu, and there set the output encoding to UTF-8. Praat will from then on save your text files in the UTF-8 format

7) Collect a list of ALL filenames and corresponding sentences in the data to a one single big table (Praat script helps).

OR on shell:

LIST OF ALL FILES IN A FOLDER TO A .txt FILE

cd to directory 

ls $search_path > list.txt


### OTHER SHELL COMMANDS ###

CONVERSION UTF-16 to UTF-8:

#find . -type f -exec bash -c 'iconv -f utf-16 -t utf-8 "{}" > "{}"' \;

CHECK .WAV INFO (Bit rate, bit depth...):

mediainfo cmu_us_arctic_slt_b0539.wav

(mediainfo package has to be installed)

CHECK .TXT ENCODING:

file myfile.txt check encoding
