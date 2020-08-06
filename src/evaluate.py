#!/usr/bin/env python3
'''Computes token accuracy and prints errors.'''


import argparse
import os


def main(args): 
        
    with open(args.gold_sourcepath, 'r') as gold_file, open(args.pred_sourcepath, 'r') as pred_file:

        # computes overall token accuracy and baseline accuracy; baseline accuracy computes the number of correctly cased tokens in a casefolded data set.
        incorrect = 0
        correct = 0 
        baseline_correct = 0
        total = 0
        for (gold_tokens, pred_tokens) in zip(gold_file, pred_file):
            for (gold_token, pred_token) in zip(gold_tokens.split(), pred_tokens.split()):
                total += 1
                if gold_token == pred_token:
                    correct += 1
                else:
                    print(gold_token, pred_token)
                    incorrect += 1
                if gold_token == gold_token.casefold(): 
                    baseline_correct += 1 

        baseline_accuracy = baseline_correct / total
        token_accuracy = correct / total

        print('======================================')
        print(f'CORRECT: {correct:.4f}')
        print(f'INCORRECT: {incorrect:.4f}')
        print(f'TOTAL: {total: .4f}')
        print(f'BASELINE ACCURACY: {baseline_accuracy: .4f}')
        print(f'TOKEN ACCURACY: {token_accuracy: .4f}')
        print('======================================')
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('gold_sourcepath', help='sourcepath to gold data')
    parser.add_argument('pred_sourcepath', help= 'sourcepath to case-restored, predicted data')
    main(parser.parse_args())

