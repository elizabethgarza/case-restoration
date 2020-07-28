"""
Extracts suffix and word context features.
"""


import typing


def suff_features(token: str) -> List: 
    
    if len(token)>3: 
        suff_features = [f"suf1={token[-1]}", 
                              f"suf2={token[-2]+token[-1]}", 
                              f"suf3={token[-3]+token[-2]+token[-1]}"] 
        return suff_features 
    
    if len(token)==3: 
        suff_features = [f"suf3={token[-3]+token[-2]+token[-1]}", f"suf2={token[-2]+token[-1]}"]
        return suff_features
    
    if len(token)==2: 
        suff_features = [f"suf1={token[-1]}"]
        return suff_features
    
        
    if len(token)==1: 
        suff_features = []
        return suff_features


def extract_features(tokenized_sent:  List) ->  List
    
    features = []
    
    for index, token in enumerate(tokenized_sent): 
        if index==0:
            features.append([f"t[0]={token}", 
                             "__BOS__"]+suff_features(token))
        if index==1:
            features.append([f"t[0]={token}", 
                             f"t[-1]={tokenized_sent[index-1]}", 
                             f"t[+1]={tokenized_sent[index+1]}", 
                             f"t[-1]={tokenized_sent[index-1]}^t[+1]={tokenized_sent[index+1]}"]+suff_features(token))
        if index>1 and index<(len(tokenized_sent)-3):
            if len(token)>3:
                features.append([f"t[0]={token}", 
                              f"t[-1]={tokenized_sent[index-1]}", 
                              f"t[+1]={tokenized_sent[index+1]}", 
                              f"t[-1]={tokenized_sent[index-1]}^t[+1]={tokenized_sent[index+1]}",
                              f"t[-2]={tokenized_sent[index-2]}", 
                              f"t[+2]={tokenized_sent[index+2]}"]+suff_features(token))
        if index == len(tokenized_sent)-3:
            if len(token)>3:
                features.append([f"t[0]={token}", 
                              f"t[-1]={tokenized_sent[index-1]}", 
                              f"t[+1]={tokenized_sent[index+1]}", 
                              f"t[-1]={tokenized_sent[index-1]}^t[+1]={tokenized_sent[index+1]}",
                              f"t[-2]={tokenized_sent[index-2]}"]  
                              +suff_features(token))
        if index == len(tokenized_sent)-2:
            if len(token)>3:
                features.append([f"t[0]={token}", 
                              f"t[-1]={tokenized_sent[index-1]}",
                              f"t[-2]={tokenized_sent[index-2]}"]+suff_features(token))
        if index == len(tokenized_sent)-1:
            features.append([f"t[0]={token}",
                                 "__EOS__", 
                                  f"t[-1]={tokenized_sent[index-1]}",
                                  f"t[-2]={tokenized_sent[index-2]}"]+suff_features(token))

    return features