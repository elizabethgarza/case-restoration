#!/usr/bin/env python3
"""Trains TokenCase tagger."""


import argparse
import collections
import json
import os
import subprocess
from typing import List 

import case 
import features

os.chdir('..')
os.chdir('data')

def _extract_train(train_sourcepath):

    with open(train_sourcepath, 'r') as source, open('train_feats.txt', 'w') as sink: 
        mc_dict = {}
        pattern_counts = collections.defaultdict(collections.Counter)
        tok_sents = []
        folded_tok_sents = []
        for line in source: 
            tok_sent = line.split()
            toks = []
            folded_toks = []
            for tok in tok_sent: 
                folded_tok = tok.casefold()
                folded_toks.append(folded_tok)
                toks.append(tok)
            folded_tok_sents.append(folded_toks)
            tok_sents.append(toks)   
        for tok_sent, folded_tok_sent in zip(tok_sents, folded_tok_sents):
            sfs = features.extract_features(folded_tok_sent)
            tc_and_sfs = []
            for tok, feat in zip(tok_sent, sfs): 
                tc = case.get_tc(tok)[0].name
                pattern = case.get_tc(tok)[1]
                if pattern: 
                    pattern_counts[tok.casefold()][tok] += 1
                tc_and_feats = [tc] + feat
                tc_and_sfs.append(tc_and_feats)
            for tc_and_sf in tc_and_sfs: 
                print('\t'.join(tc_and_sf), file=sink)
            print(file=sink)
            for folded_tok, pattern_count in pattern_counts.items(): # e.g.-- `former Counter({'former': 169, 'Former': 24})`
                tok, count = pattern_count.most_common(1)[0]
                if count > 2: 
                    mc_dict[folded_tok] = tok
        mc_dict = json.dumps(mc_dict)
        with open('mc_dict.json', 'w') as sink: 
            sink.write(mc_dict) 

def _extract_dev(dev_sourcepath): 
    
    with open(dev_sourcepath, 'r') as source, open('dev_feats.txt', 'w') as sink:
        tok_sents = []
        folded_tok_sents = []
        for line in source: 
            tok_sent = line.split()
            toks = []
            folded_toks = []
            for tok in tok_sent: 
                folded_tok = tok.casefold()
                folded_toks.append(folded_tok)
                toks.append(tok)
            folded_tok_sents.append(folded_toks)
            tok_sents.append(toks)   
        for tok_sent, folded_tok_sent in zip(tok_sents, folded_tok_sents):
            sfs = features.extract_features(folded_tok_sent)
            tc_and_sfs = []
            for tok, feat in zip(tok_sent, sfs): 
                tc = case.get_tc(tok)[0].name
                tc_and_feats = [tc] + feat
                tc_and_sfs.append(tc_and_feats)
            for tc_and_sf in tc_and_sfs: 
                print('\t'.join(tc_and_sf), file=sink)
            print(file=sink)

def main(args): 

    os.chdir('..')
    os.chdir('data')

    #preprocesses train and prints it to a file titled 'train_feats.txt'. 
    _extract_train(args.train_sourcepath)

    # preprocesses dev and prints it to a file titled 'dev_feats.txt'
    _extract_dev(args.dev_sourcepath)

    # creates a list of the parameters of 'crflearn'
    parms = [
        "-p",
        "feature.possible_states=1",
        "-p",
        "feature.possible_transitions=1",
    ]

    # creates a list of the arguments in the 'crflearn' call
    args = [ 
        "-m",
        args.model_sinkpath,
        "-e2",
        "train_feats.txt",
        "dev_feats.txt"
    ]

    # creates the model 
    subprocess.check_call(["crfsuite", "learn"] + parms + args)  

    # removes the two files with the preprocessed data
    os.remove('train_feats.txt')
    os.remove('dev_feats.txt')
    
if __name__=='__main__': 
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('train_sourcepath', help = 'path to train')
    parser.add_argument('dev_sourcepath', help = 'path to dev')
    parser.add_argument('model_sinkpath', help = 'path to model')
    args = parser.parse_args()
    main(args)

    
            

            


                    



