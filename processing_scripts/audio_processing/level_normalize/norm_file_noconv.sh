#!/bin/bash

# Ensure we have the utils
type -P "sox" &> /dev/null  || (>&2 echo "sox not in path"; exit -1)
type -P "sv56demo" &> /dev/null  || (>&2 echo "sv56demo not in path"; exit -1)

# Define some constants
DEFAULT_LEVEL=26

# Parse the arguments
if [[ $# -ne 2 ]]
then
    >&2 echo "Command line requires 2 arguments: <input_wav> <output_dir>"
    exit -1
fi

input_file=$1
output_dir=$2

# Ensure the output directory is valid
input_par_dir=$(dirname $input_file)
if [[ "$input_par_dir" == "$output_dir" ]]
then
    >&2 echo "Cannot normalize in the parent directory of the input file"
    exit -1
fi

# Define some temporary variables
SAMPLERATE=$(sox --i -r "$input_file")
BASENAME=$(basename "$input_file")
RAW_ORIG="$output_dir/${BASENAME}.raw"
RAW_NORM="$output_dir/${BASENAME}.raw_norm"
OUTPUT_FILE="$output_dir/${BASENAME}.wav"

# Convert to raw, normalize and back to output wav
echo "Normalizing $input_file"
sox "$input_file" "$RAW_ORIG"
sv56demo -q -sf ${SAMPLERATE} -lev -${DEFAULT_LEVEL} "${RAW_ORIG}" "${RAW_NORM}" >> log_sv56 2>> log_sv56
sox -t raw -b 16 -e signed -c 1 -r ${SAMPLERATE} "${RAW_NORM}" "$OUTPUT_FILE"

# Some cleaning
rm "${RAW_NORM}" "${RAW_ORIG}"
