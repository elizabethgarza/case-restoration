#!/usr/bin/env python3
'''Computes token accuracy and prints errors.'''


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
        all_folded_tokens = []
        for (gold_line, pred_line) in zip(gold, pred):
            gold_tokens = gold_line.split()
            pred_tokens = pred_line.split()
            assert len(gold_tokens) == len(pred_tokens)
            for (gold_token, pred_token) in zip(gold_tokens, pred_tokens):
                all_pred_tokens.append(pred_token)
                all_gold_tokens.append(gold_token)
                all_folded_tokens.append(gold_token.casefold())

        # computes TOKEN ACCURACY
        assert len(all_pred_tokens) == len(all_gold_tokens) == len(all_folded_tokens)
        TOTAL = len(all_pred_tokens)
        for gold_token, pred_token in zip(all_gold_tokens, all_pred_tokens): 
            if gold_token == pred_token: 
                CORRECT += 1 
            else: 
                print(gold_token, pred_token)
                INCORRECT += 1

        # computes BASELINE ACCURACY
        BASELINE_CORR = 0
        BASELINE_INCORR = 0 
        for gold_token, folded_token in zip(all_gold_tokens, all_folded_tokens): 
            if gold_token == folded_token: 
                BASELINE_CORR += 1
            else: 
                BASELINE_INCORR += 1
        assert (BASELINE_CORR + BASELINE_INCORR) == (len(all_pred_tokens))

        # computes PRECISION and RECALL
        FP = 0 # 'FP' stands for 'false positive', etc.
        FN = 0
        TP = 0 
        all_cased_tokens = set() # these sets are being created in order to carry out an assertion statement below 
        false_pos = set()
        false_neg = set()
        true_pos = set()
        for gold_token, pred_token in zip(all_gold_tokens, all_pred_tokens): 
            if gold_token == gold_token.casefold(): # e.g. 'and' == 'and' 
                if gold_token != pred_token: # e.g. 'and' != 'And'
                    all_cased_tokens.add(gold_token.casefold())
                    false_pos.add(pred_token.casefold()) 
                    FP += 1
                elif gold_token == pred_token: # e.g. 'and' == 'and' 
                    true_pos.add(gold_token.casefold()) 
                    all_cased_tokens.add(gold_token.casefold())
                    TP += 1
            elif gold_token != gold_token.casefold(): # e.g. 'Mr.' != 'mr.'; or 'UNICEF' != 'Unicef' (An 'UPPER' that is mistagged as a 'TITLE' will be counted as a false negative.)
                if gold_token != pred_token: # e.g. 'Mr.' != 'mr.'
                    all_cased_tokens.add(gold_token.casefold())
                    false_neg.add(pred_token.casefold())
                    FN += 1
                elif gold_token == pred_token: # e.g. 'Mr.' == 'Mr.'
                    true_pos.add(gold_token.casefold())
                    all_cased_tokens.add(gold_token.casefold())
                    TP += 1
        assert len(all_cased_tokens) == len(false_pos.union(false_neg, true_pos))
  

    print('============================================================================================================')   
    print('Number of correctly cased tokens if tokens in data were casefolded')
    print('============================================================================================================')    
    print(f'TOTAL: {TOTAL}')
    print(f'CORRECT: {BASELINE_CORR}')
    print(f'INCORRECT: {BASELINE_INCORR}')   
    print(f'BASELINE ACCURACY: {BASELINE_CORR/TOTAL:.4f}')
    print('============================================================================================================')  
    print('(Number of correctly cased tokens after case restoration) / (Number of cased tokens before case restoration)')
    print('============================================================================================================')   
    print(f'TOTAL: {BASELINE_INCORR}')
    print(f'CORRECT: {BASELINE_INCORR - INCORRECT}')
    print(f'INCORRECT: {INCORRECT}')
    print(f'CASED TOKEN ACCURACY: {1-INCORRECT / BASELINE_INCORR: .4f}')
    print('============================================================================================================')   
    print('Number of correctly cased tokens if tokens in data undergo case restoration.')   
    print('============================================================================================================')         
    print(f'TOTAL: {TOTAL}')
    print(f'CORRECT: {CORRECT}')
    print(f'INCORRECT: {INCORRECT}')
    print(f'PRECISION: {TP / (TP + FP):.4f}') 
    print(f'RECALL: {TP / (TP + FN): .4f}')
    print(f'TOKEN ACCURACY: {CORRECT/TOTAL:.4f}') 
    print('============================================================================================================')  
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('gold_sourcepath', help='sourcepath to gold data')
    parser.add_argument('pred_sourcepath', help= 'sourcpath to case-restored, predicted data')
    main(parser.parse_args())

