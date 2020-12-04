#!/usr/bin/bash


if [ -e "../Data/glove.6B.300d.txt" ]
then
    echo "File is already downloaded"
    
else
    echo "Downloading word embeddings from Stanford U"
    wget http://nlp.stanford.edu/data/glove.6B.zip -O ../Data/glove.6B.zip
    sleep 2
    echo "Unarchiving word embeddings"
    unzip ../Data/glove.6B.zip -d ../Data
    sleep 2
    echo "Done downloading and unarchiving"
fi

echo "Done."
echo "Thank you."
echo "Bye."

