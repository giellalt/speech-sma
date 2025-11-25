import os

def find_missing_files(file_list_path, directory, cleaned_file_list_path):
    with open(file_list_path, 'r') as file:
        lines = file.readlines()
    with open(cleaned_file_list_path, 'w') as file:
        for line in lines:
            filename = line.split("|")[0]
            if os.path.exists(os.path.join(directory, filename)):
                file.write(line)
            else:
                print(f"Missing file: {filename}")

# Usage
find_missing_files('/home/hiovain/DeepLearningExamples/PyTorch/SpeechSynthesis/FastPitch/filelists/britt-inger-karin-table.txt', '/home/hiovain/DeepLearningExamples/PyTorch/SpeechSynthesis/FastPitch/smj_female_splits/britt-inger-karin-norm', '/home/hiovain/DeepLearningExamples/PyTorch/SpeechSynthesis/FastPitch/filelists/britt-inger-karin-table-cleaned.txt')