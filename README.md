# speech-sma
South Sámi speech technology work

## sma-TTS
* Official software available at [Borealium.org](https://borealium.org/en/resource/voice-sma-female/)
* Via Divvun API [Divvun API](https://api-giellalt.uit.no/#tts)
# smj TTS project technical documentation
This file reports the technical implementation of the speech-sma project.
### General
* [SCRIPTS] that are referred to, are going to be documented in detail in the script files
    * Almost all scripts mentioned here are written in python. Make sure to (pip) install python packages like: [sox](https://pypi.org/project/sox/), [tgt tools](https://textgridtools.readthedocs.io/en/stable/)
* Paper: Hiovain-Asikainen, K. & Kjærstad, B. T. & Kappfjell M. L. & Moshagen, N. S. (2025, accepted). The world’s first South Sámi TTS – a revitalisation effort of an endangered
language by reviving a legacy voice. Accepted for IWCLUL 2025, Joensuu, Finland.

### Corpus building
#### Text Corpus
* Anna Jacobsen’s broadcasts that already existed in written form, as they were later published in the anthology series Don jih daan bijre I–III (Jacobsen, 1997, 1998, 2000).
* Her biblical recordings were aligned with the South Sámi translation she produced together with Bierna Leine Bientie (Jacobsen and Bientie, 1993), which was scanned and OCR-processed for the project.
* Additional usable material came from her language-learning book Goltelidh jih soptsestidh (Jacobsen, 1993) and its accompanying audio cassettes.
* Manual transcription work for parts that didn't have existing texts. Done by the Divvun group at UiT in collaboration with the Sámi Archives and the National Archives of Norway.
#### Speech corpus
* Existing recordings of Anna Jacobsen. 
* The archival recordings of Anna Jacobsen were sourced from the Norwegian national broadcaster NRK and several audiobooks, and were digitally restored, enhanced, and transcribed by the Divvun group at UiT in collaboration with the Sámi Archives and the National Archives of Norway. Recorded between 1989 and 1993, the material spans multiple genres, including news and documentary broadcasts, biblical readings, fairy tales, and spontaneous autobiographical storytelling.
* During transcription, segments with very poor audio quality or containing speakers other than Anna Jacobsen were excluded from the final TTS corpus.
#### Text processing
* Most importantly checking existing texts that they match the audio tapes accurately + manual transcription.
* Done by 3 people, native and non-native language experts. 
* Processing roughly ten hours of audio resulted in about one hundred hours of transcription, equivalent to 2.5–3 weeks of full-time work for one person.
#### Audio processing
* Name files: wavs and txts identically
    * Also: split very long files to 2-3 parts to make the automatic pre-processing easier
* First cleaning of the audio: cut long pauses, noise, anything not suitable for synthesis
* Filters to long audio files (before splitting, see folder 'audio_processing')
    * Resemble-enhance pipeline, [resemble-enhance](https://github.com/resemble-ai/resemble-enhance)
    * Level normalization (make all sound files in the corpus to be at the same volume level)- [sox](https://pypi.org/project/sox/) & [STL](https://github.com/openitu/STL)
        * copy the [SCRIPT: norm_file_noconv.sh] to the folder where you have your target files, open a Terminal and cd to that folder with the script and the target files. Make a separate /output subfolder
        * remember to export path before running the command: export PATH=$PATH:/home/user/STL/bin 
        * run this command (example; fill with your own folder paths): ls -1 /home/user/sma/aj/*.wav | xargs -P 8 -I {} bash norm_file_noconv.sh {} /home/user/sma/aj/output

#### Splitting the data to sentences
* Generally, all TTS frameworks require the training data to be in certain form. This is sentence-long .wav and .txt pairs. The files should not vary too much in length.
* Make sure .wav and .txt long file pairs are identically named
* Run [WebMAUS pipeline without ASR](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/Pipeline), choose (G2P ⇒ MAUS ⇒ Subtitle) TextGrid output. This pipeline retains original text formatting, commas etc.
    * Audio files over 200 MB/30mins in size should be split in smaller chunks first or the aligner won't work
    * TIP for long files: [use Pipeline without ASR](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/Pipeline) with G2P -> Chunker -> MAUS options
    *  No Sámi model -> FINNISH model works for Sámi but note that numbers etc. are normalized in Finnish if any so make sure numbers are normalized BEFORE "MAUSING"!
    * WebMAUS automatically outputs a Praat .TextGrid annotation file with 4 annotation layers and boundaries on phoneme and word levels/tiers
* Next, the word boundary tier is converted to SENTENCE level based on silence duration between the sentences. It might require some fine-tuning of the duration variable to find a suitable treshold to each speaker [SCRIPT: scripts/concatenate_webmaus_word_tier.py].
    * The resulting sentence tier is manually checked and fixed in Praat
![](https://hackmd.io/_uploads/SyBSzIVvh.png)

* Run splitter script (Python) -- the [SCRIPT: split_sound_by_labeled_intervals_from_tgs_in_a_folder.py] saves each labeled interval (defined in the script) into indexed short .wav and .txt files into a folder
* Gather the .wav filenames and transcripts from corresponding txt files to a table [SCRIPT: scripts/extract_filenames.py]. Fill in the paths carefully!
* Check the table manually that everything is correct and that there are no unnecessary characters

### TTS frameworks

#### Fastpitch setup and training
* [Fastpitch on GitHub](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch)
    * Reference: [Adrian Łańcucki, 2021](https://arxiv.org/abs/2006.06873)
* Define symbol set of the language carefully [SCRIPT, for example: /home/user/DeepLearningExamples/PyTorch/SpeechSynthesis/FastPitch/common/text/symbols.py]
    * This is EXTREMELY important to get right! If the symbol list is not correct, the training will not work correctly. It's better to include "too many" symbols than too few.
* Fastpitch pre-processing [SCRIPT: scripts/prepare_dataset.sh]
    * define data table/filelist
    * extract mel spectrograms and pitch for each file, remember to CONVERT audio files to 22 KhZ (downsample)
    * add pitch file paths to the data table [SCRIPT: save_pitch_filenames.py]
        * Then: add speaker numbers!
    * using the *shuf* command, shuffle the table
    * make a test/validation set: ~100 sentences from the corpus are left out from training
    * If you face an error like: "Loss is NaN", run SCRIPT: check_pitch_1.py acapela_f_new/pitch to see if there are pitch files without any pitch analyzed (due to creaking voice, for example)
* Training
    * training [SCRIPT], parametres
    * training on cluster [SCRIPT]
    * training script with debug plotting: draw a spectrogram plot of each epoch [SCRIPT]
    * running inference [SCRIPTS]
        * VOCODERS!!! HifiGAN, NeMo UnivNet, hiftnet?
            * UnivNet generally performs better: it is easier to generalize to unseen speakers; no audible vocoder noise. Installation: pip install nemo_toolkit[tts]
            * Reference: Jang, W., Lim, D., Yoon, J., Kim, B., & Kim, J. (2021). Univnet: A neural vocoder with multi-resolution spectrogram discriminators for high-fidelity waveform generation. arXiv preprint arXiv:2106.07889.
            * Usage in the inference script:
...
from nemo.collections.tts.models import UnivNetModel
...
self.vocoder = UnivNetModel.from_pretrained(model_name="tts_en_libritts_univnet")
...
### Exporting TorchScript for C++ integration
* Command: <python export_torchscript.py --generator-name FastPitch --generator-checkpoint /output_sme_af/FastPitch_checkpoint_1000.pt --output /output_sme_af/torchscript_sme_f.pt --amp>
### User interface for TTS
* Huggingface multi-sami demo [Huggingface](https://huggingface.co/spaces/divvun-tts/multi-sami), includes multiple Sámi languages. 
### Publications & presentations
* Publication event 30.10.2024 in Hattfjelldal, Anna Jacobsen's 100th birthday
* Trondheim AI i Norden, 7.11.2024 (?)
* IWCLUL 2025, Joensuu, Finland
### Publishing the materials and models
* Where to publish/store data and models?
* Restrictions for specific use cases, such as commercial, academic etc...?
### To do...
* More voices and dialects.
* Integration to ANKI flashcard application for language learning?

### Bibliography & other useful links
* https://tts.readthedocs.io/en/latest/what_makes_a_good_dataset.html
* LRSpeech: Extremely Low-Resource Speech Synthesis and
Recognition https://arxiv.org/abs/2008.03687
* coqui-ai TTS: https://github.com/coqui-ai/TTS
* What makes a good TTS dataset: <https://docs.coqui.ai/en/latest/what_makes_a_good_dataset.html>
