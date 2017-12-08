#!/bin/sh

echo "ExtractData.py --index news --minfreq $1 --maxfreq $2 --numwords $3" > outputMRK.txt
python ExtractData.py --index news --minfreq $1 --maxfreq $2 --numwords $3
python GeneratePrototypes.py 
echo "MRK MEANS: " >> outputMRK.txt
python MRKmeans.py >> outputMRK.txt 
echo "PROCESS RESULTS: " >> outputMRK.txt
python ProcessResults.py >> outputMRK.txt
