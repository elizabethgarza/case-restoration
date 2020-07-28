#!/usr/bin/env python3
"""Splits data into 'train', 'dev' and 'test'."""


import argparse
from nltk import TreebankWordTokenizer
import os
import random
from typing import List, Tuple
from tqdm import tqdm
import subprocess


def _tok_and_norm(corpus_path: str) -> List: 

    """
    Tokenizes and normalizes each line in the corpus, rejoins and then appends those lines to a larger list, titled 'tok_sents'.
    """

    tok_sents = []
    with open(corpus_path, 'r') as source: 
        for line in tqdm(source): 
            # normalize quotation marks/apostrophes for tokenization
            norm_toks = (line.replace("”", '"').replace("“", '"')
                        .replace("’", "'").replace("‘", "'").replace("amp;", ""))
            # tokenizes each sentence and appends that tok_sent to the list tok_sents
            tok_sent = TreebankWordTokenizer().tokenize(norm_toks)
            tok_sents.append(tok_sent)
            
    return tok_sents

def _shuffle_and_split(tok_sents: list) -> Tuple[List, List, List]: 

    """
    Shuffles a list of tokenized_sentences and splits the lists into 'train', 'test', and 'dev'.
    """

    # shuffles the tokenized_sentences in 'tok_sents'
    random.shuffle(tok_sents)
    

    # computes the lengths of 'train' and 'dev'/'test'
    train_len = round(len(tok_sents)*.8)
    dev_and_test_len = round(len(tok_sents)*.2)

    # splits 'tok_sents' into 'train', 'dev', and 'test'
    train = tok_sents[:train_len]
    dev_and_test = tok_sents[train_len:]
    dev_len = round(len(dev_and_test)/2)
    dev = dev_and_test[:dev_len]
    test = dev_and_test[dev_len:]

    return train, dev, test

def _print(output_filepath: str, tok_sents: List) -> None: 

    """
    Rejoins tok_sents and prints to 'data'.
    """

    with open(output_filepath, 'w') as sink: 
        for sent in tok_sents: 
            print(' '.join(sent), file=sink)
        print(file=sink)

def main(args) -> None:

    # switches directories from 'src' to 'data' so 'train', 'dev', and 'test' will print to 'data'.
    os.chdir('..')
    os.chdir('data')

    # Tokenizes and normalizes each line in the corpus, rejoins and then appends those lines to a larger list, titled 'tok_sents'.
    # Shuffles a list of tokenized_sentences and splits the list into 'train', 'test', and 'dev'.
    with open(str(args.corpus_filepath), 'r'): 
        tok_sents = _tok_and_norm(str(args.corpus_filepath)) 
        train, dev, test = _shuffle_and_split(tok_sents)

    # Prints split up data set to 'data'.
    _print(args.train_filepath, train)
    _print(args.dev_filepath, dev)
    _print(args.test_filepath, test)
      

if __name__=="__main__": 
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('corpus_filepath', help='input filepath to corpus')
    parser.add_argument('train_filepath', help='output filepath to `train`')
    parser.add_argument('dev_filepath', help='output filepath to `dev`')
    parser.add_argument('test_filepath', help='output filepath to `test`')
    args = parser.parse_args()
    main(args)


