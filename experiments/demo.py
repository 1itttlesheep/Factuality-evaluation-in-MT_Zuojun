import pandas as pd
from mosestokenizer import MosesDetokenizer
from scipy.stats import pearsonr   
def pearson(preds, labels):
    pearson_corr = pearsonr(preds, labels)[0]
    return '{0:.{1}f}'.format(pearson_corr, 3)

reference_list = dict({
        "de-en": 'testset_zh-en.tsv',
        })

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--model_name', type=str, default='bert-base-multilingual-cased')
parser.add_argument('--do_lower_case', type=bool, default=False)
parser.add_argument('--language_model', type=str, default='gpt2')
parser.add_argument('--alignment', type=str, default='CLP', help='CLP or UMD or None')    
parser.add_argument('--ngram', type=int, default=1)
parser.add_argument('--layer', type=int, default=8)
parser.add_argument('--batch_size', type=int, default=8)
parser.add_argument('--dropout_rate', type=float, default=0.3, help='Remove the percentage of noisy elements in Word-Mover-Distance')

import json
args = parser.parse_args()
params = vars(args)
print(json.dumps(params, indent = 2))

from scorer import XMOVERScorer
import numpy as np
import torch
scorer = XMOVERScorer(args.model_name, args.language_model, args.do_lower_case)

def metric_combination(a, b, alpha):
    return alpha[0]*np.array(a) + alpha[1]*np.array(b)

def get_data(path, src):
    data = {}
    s = []
    ref = []
    hyp = []
    with open("wmt/"+src+"/"+path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            line = l.split('\t')
            s.append(line[1].strip())
            ref.append(line[2].strip())
            hyp.append(line[5].strip())
        data['source'] = s
        data['reference'] = ref
        data['translation'] = hyp
    return data
            

import os
from tqdm import tqdm
scoreslist = []
for pair in tqdm(reference_list.items()):
    lp, path = pair
    path = "name.txt"
    src, tgt = lp.split('-')
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    temp = np.load('mapping/layer-8/europarl-v7.%s-%s.2k.%s.BAM' % (src, tgt, args.layer), allow_pickle=True)
    projection = torch.tensor(temp, dtype=torch.float).to(device)
    
    temp = np.load('mapping/layer-8/europarl-v7.%s-%s.2k.%s.GBDD' % (src, tgt, args.layer), allow_pickle=True)
    bias = torch.tensor(temp, dtype=torch.float).to(device)

    data = get_data(path, src)
    references = data['reference']
    translations = data['translation']
    source = data['source']
    with MosesDetokenizer(src) as detokenize:        
        source = [detokenize(s.split(' ')) for s in source]         
    with MosesDetokenizer(tgt) as detokenize:                
        references = [detokenize(s.split(' ')) for s in references]        
        translations = [detokenize(s.split(' ')) for s in translations]
    
    x_hyp = scorer.compute_xmoverscore(args.alignment, projection, bias, source, translations, ngram=args.ngram, \
                                              layer=args.layer, dropout_rate=args.dropout_rate, bs=args.batch_size)
    x_ref = scorer.compute_xmoverscore(args.alignment, projection, bias, source, references, ngram=args.ngram, \
                                              layer=args.layer, dropout_rate=args.dropout_rate, bs=args.batch_size)
    # lm_scores_hyp = scorer.compute_perplexity(translations, bs=1)
    # lm_scores_ref = scorer.compute_perplexity(references, bs=1)
    # scores_ref = metric_combination(x_ref, lm_scores_ref, [1, 0.1])
    # scores_hyp = metric_combination(x_hyp, lm_scores_hyp, [1, 0.1])
    for r,h in zip(x_ref, x_hyp):
        scoreslist.append((r,h))
    
    print(path)
        
rg = 0
hg = 0

with open('wmt/de/namer.txt', 'w', encoding='utf-8') as f:
    for i,p in enumerate(scoreslist):
        r = float(p[0])
        h = float(p[1])
        if r > h:
            rg += 1
        elif h > r:
            hg += 1
        else:
            print('same')
        
        f.write(str(i))
        f.write('\t')
        f.write(str(r))
        f.write('\t')
        f.write(str(h))
        f.write('\n')

print(rg,hg)
result = rg / (rg+hg)
print(result)
    
    
