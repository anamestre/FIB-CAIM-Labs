#!/bin/sh

echo "Experimento jugando con los valores para mappers y reducers" > output_experiment2.txt
echo "20 clases, mappers: $1, reducers: $2" >> output_experiment2.txt

echo "MRK MEANS: " >> output_experiment2.txt
python MRKmeans.py --nmaps $1 --nreduces $2 >> output_experiment2.txt 
echo "PROCESS RESULTS: " >> output_experiment2.txt
python ProcessResults.py >> output_experiment2.txt
