#!/usr/bin/env python3
'''Computes token accuracy.'''


import argparse
import os


def main(args): 

    os.chdir('..')
    os.chdir('data')

    with open(args.gold_sourcepath, 'r') as gold, open(args.pred_sourcepath, 'r') as pred: 
        
        CORRECT = 0 
        INCORRECT = 0 
        all_pred_tokens = []
        all_gold_tokens = []
        
        for (gold_line, pred_line) in zip(gold, pred):
            gold_tokens = gold_line.split()
            pred_tokens = pred_line.split()
            assert len(gold_tokens) == len(pred_tokens)
            for (gold_token, pred_token) in zip(gold_tokens, pred_tokens):
                all_pred_tokens.append(pred_token)
                all_gold_tokens.append(gold_token)
        
        assert len(all_pred_tokens) == len(all_gold_tokens)
        TOTAL = len(all_pred_tokens)
        for gold_token, pred_token in zip(all_gold_tokens, all_pred_tokens): 
            if gold_token == pred_token: 
                CORRECT += 1 
            else: 
                print(gold_token, pred_token)
                INCORRECT += 1
                
    print(f'TOTAL: {TOTAL}')
    print(f'CORRECT: {CORRECT}')
    print(f'INCORRECT: {INCORRECT}')
    print(f'ACCURACY: {CORRECT/TOTAL:.4f}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('gold_sourcepath', help='sourcepath to gold data')
    parser.add_argument('pred_sourcepath', help= 'sourcpath to case-restored, predicted data')
    main(parser.parse_args())

