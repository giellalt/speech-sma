def read_table(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def filter_and_find_longest_transcript(table_data, threshold=4):
    filtered_rows = []
    longest_transcript_length = 0
    longest_transcript = ""

    for row in table_data:
        columns = row.split('|')
        if len(columns) == 4:  # Ensure there are exactly 4 columns in the row
            filename, _, transcript, _ = columns
            transcript_length = len(transcript.strip())
            if transcript_length < threshold:
                filtered_rows.append((filename, transcript, transcript_length))
            if transcript_length > longest_transcript_length:
                longest_transcript_length = transcript_length
                longest_transcript = transcript

    return filtered_rows, longest_transcript, longest_transcript_length

def print_sorted_transcripts(filtered_rows, longest_transcript, longest_transcript_length):
    print("Transcripts shorter than 4 characters (Filename | Transcript):")
    for filename, transcript, length in filtered_rows:
        print(f"{filename} | {transcript} (Length: {length})")

    print("Longest transcript:")
    print(f"Transcript: {longest_transcript}")
    print(f"Length: {longest_transcript_length}")

if __name__ == "__main__":
    file_path = "/home/hiovain/DeepLearningExamples/PyTorch/SpeechSynthesis/FastPitch/filelists/SME-MEGA-TTS_filtered_filelist_pitch.txt"
    table_data = read_table(file_path)
    filtered_rows, longest_transcript, longest_transcript_length = filter_and_find_longest_transcript(table_data)
    filtered_rows.sort(key=lambda x: x[2])  # Sort rows based on the transcript length
    print_sorted_transcripts(filtered_rows, longest_transcript, longest_transcript_length)




