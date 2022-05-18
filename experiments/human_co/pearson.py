from scipy.stats import pearsonr
from collections import defaultdict
#from bertscore import be_score
from moverscore import word_mover_score 
#from bart_score import BARTScorer
#bart_scorer = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')

def pearson_and_spearman(preds, labels):
    pearson_corr = pearsonr(preds, labels)[0]
    return "pearson: " + str(pearson_corr)

refs = []
sens = []
nli_scores = []
hs = []
rs = []
index= 0
with open('metricre/w17/result2cs.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        index += 1
        #print(index)
        e = min(float(line[0]), float(line[3]))
        n = min(float(line[1]), float(line[4]))
        score_nli = e-n
        score_nli = 1*0.5*(float(line[0])+float(line[3]))-1*0.5*(float(line[1])+float(line[4]))-0*0.5*(float(line[2])+float(line[5]))
        nli_scores.append(score_nli)
        #score = bart_scorer.score([line[7]], [line[8]], batch_size=4)[0] + score_nli
        
        refs.append(line[7])
        sens.append(line[8])
        
        #score = score_nli
        hs.append(float(line[6]))
        #rs.append(score[0])

idf_dict_hyp = defaultdict(lambda: 1.)
idf_dict_ref = defaultdict(lambda: 1.)
ms = word_mover_score(refs, sens, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
    

#(bs, _, _), _ = be_score(sens, refs, lang="en", return_hash=True)        
for m, n in zip(ms, nli_scores):
    rs.append(m+n)

print(pearson_and_spearman(hs, ms))
print(pearson_and_spearman(hs, rs))

