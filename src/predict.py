#!/usr/bin/env python3
"""Predicts TokenCases and prints predictions to a file--i.e. args.predictions_sinkpath."""

import argparse
import json
import os
import subprocess

import case
import features


def _extract_test_feats(test_sourcepath): 
    
    with open(test_sourcepath, 'r') as source, open('test_feats.txt', 'w') as sink: 
        toks = []
        folded_tok_sents = []
        for line in source: 
            tok_sent = line.split()
            folded_toks = []
            for tok in tok_sent: 
                folded_tok = tok.casefold()
                toks.append(folded_tok)
                folded_toks.append(folded_tok)
            folded_tok_sents.append(folded_toks)  
        for folded_tok_sent in folded_tok_sents: 
            tfs = features.extract_features(folded_tok_sent)
            vectorless_tfs = []
            for tf in tfs: 
                tf = '\t'.join(tf)
                vectorless_tfs.append(tf)
            for tfs in vectorless_tfs: 
                 print(tfs, file=sink)
            print(file=sink)

def _predict(test_sourcepath, model_sourcepath, predictions_sinkpath): 

    with open(test_sourcepath, 'r') as source, open ('mc_dict.json', 'r') as source2, subprocess.Popen(["crfsuite", "tag", "-m", model_sourcepath, "test_feats.txt"], stdout=subprocess.PIPE, text=True) as proc:
        mc_dict = json.load(source2)
        folded_toks = []
        no_of_sents = 0
        for line in source: 
            tok_sent = line.split()
            for index, tok in enumerate(tok_sent): 
                folded_tok = tok.casefold()
                folded_toks.append(folded_tok)
                if index == len(tok_sent)-1: 
                    folded_toks.append('\n')
                    no_of_sents += 1

        # applies the tags to casefolded tokens in 'test'
        cased_toks = []
        for tag, (index, folded_tok) in zip(proc.stdout, enumerate(folded_toks)):
            if folded_tok==f'\n':
                cased_toks.append(folded_tok)
            elif tag == case.TokenCase.MIXED: 
                print(tag)
                cased_toks.append(mc_dict.get(folded_tok))
            elif folded_tok in mc_dict.keys(): 
                cased_toks.append(mc_dict.get(folded_tok))
            else: 
                tag = tag.rstrip()
                cased_tok = case.apply_tc(folded_tok, case.TokenCase[tag])
                cased_toks.append(cased_tok)

        return cased_toks



def main(args): 

    os.chdir('..')
    os.chdir('data')

    # extracts freatures from test_sourcepath and prints to a file titled, 'test_feats.txt', which will be used for predicting after which it will be deleted
    _extract_test_feats(args.test_sourcepath)

    # calls crfsuite tag and prints cased tokens to predictions sinkpath 
    cased_toks = _predict(args.test_sourcepath, args.model_sourcepath, args.predictions_sinkpath)
    with open('recased_test.txt', 'w') as sink:     
        sents = ' '.join(cased_toks)
        print(sents, file=sink)
    with open('recased_test.txt', 'r') as source, open(args.predictions_sinkpath, 'w') as sink:
        for line in source: 
            line = line.rstrip().lstrip()
            print(line, file=sink)
        print(file=sink)

    # removes file with bad formatting
    os.remove('recased_test.txt')
    os.remove('test_feats.txt')

if __name__=='__main__': 
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('test_sourcepath', help = 'path to test')
    parser.add_argument('model_sourcepath', help = 'path to model')
    parser.add_argument('predictions_sinkpath', help = 'path to predictions')
    args = parser.parse_args()
    main(args)




            
        
    
    
     
 



