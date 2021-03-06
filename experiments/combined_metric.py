from metric_eval import get_data, comp
from NLI_comp import read_result, pick_enc, final_res

def normalization(list):
    res = []
    for i in range(len(list)):
        norm = (list[i]-min(list))/max(list)-min(list)
        res.append(norm)
        
    return res

def bart_nli(phenomenon, dataset, model, direction1, direction2):
    from bart_score import BARTScorer
    
    bart_scorer = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')
    
    _, ref, _, hyp1, hyp2, hyp3, hyp4 = get_data(phenomenon, dataset)
    
    metric_score1 = []
    metric_score2 = []
    if phenomenon == 'drop' or phenomenon == 'vb':
        metric_score1 = bart_scorer.score(ref, hyp1, batch_size=4)
        metric_score2 = bart_scorer.score(ref, hyp3, batch_size=4)
    elif phenomenon == 'jj':
        metric_score1 = bart_scorer.score(ref, hyp1, batch_size=4)
        metric_score2 = bart_scorer.score(ref, hyp4, batch_size=4)
    else:
        metric_score1 = bart_scorer.score(ref, hyp1, batch_size=4)
        metric_score2 = bart_scorer.score(ref, hyp2, batch_size=4)
        
    metric_score1 = normalization(metric_score1)
    metric_score2 = normalization(metric_score2)
    
    nli_score1, nli_score2 = read_result(phenomenon, model, dataset)
    
    
    
    for enc1, enc2 in zip(nli_score1, nli_score2):
            e1 = enc1[0]
            n1 = enc1[1]
            c1 = enc1[2]
            e2 = enc1[3]
            n2 = enc1[4]
            c2 = enc1[5]
            
            e, n, c = pick_enc(e1,n1,c1,e2,n2,c2,direction1)
            s1 = final_res(e, n, c, direction2)
            
            e1 = enc2[0]
            n1 = enc2[1]
            c1 = enc2[2]
            e2 = enc2[3]
            n2 = enc2[4]
            c2 = enc2[5]
            
            e, n, c = pick_enc(e1,n1,c1,e2,n2,c2,direction1)
            s2 = final_res(e, n, c, direction2)
    
    s1 , s2 = normalization(s1), normalization(s2)
    
    score1 = []
    score2 = []
    for m, n in zip(metric_score1, s1):
        score1.append(m+n)
        
    for m, n in zip(metric_score2, s2):
        score2.append(m+n)
        
    
    accuracy = comp(score1, score2)
    print('bartscore + nli: %f' % (accuracy))

def bert_nli(phenomenon, dataset, model, direction1, direction2):
    from bertscore import be_score
    
    _, ref, _, hyp1, hyp2, hyp3, hyp4 = get_data(phenomenon, dataset)
    
    metric_score1 = []
    metric_score2 = []
    if phenomenon == 'drop' or phenomenon == 'vb':
        (metric_score1, _, _), _ = be_score(hyp1, ref, lang="en", return_hash=True)  
        (metric_score2, _, _), _ = be_score(hyp3, ref, lang="en", return_hash=True)  
    elif phenomenon == 'jj':
        (metric_score1, _, _), _ = be_score(hyp1, ref, lang="en", return_hash=True)  
        (metric_score2, _, _), _ = be_score(hyp4, ref, lang="en", return_hash=True)  
    else:
        (metric_score1, _, _), _ = be_score(hyp1, ref, lang="en", return_hash=True)  
        (metric_score2, _, _), _ = be_score(hyp2, ref, lang="en", return_hash=True)  
        
    metric_score1 = normalization(metric_score1)
    metric_score2 = normalization(metric_score2)
    
    nli_score1, nli_score2 = read_result(phenomenon, model, dataset)
    
    
    
    for enc1, enc2 in zip(nli_score1, nli_score2):
            e1 = enc1[0]
            n1 = enc1[1]
            c1 = enc1[2]
            e2 = enc1[3]
            n2 = enc1[4]
            c2 = enc1[5]
            
            e, n, c = pick_enc(e1,n1,c1,e2,n2,c2,direction1)
            s1 = final_res(e, n, c, direction2)
            
            e1 = enc2[0]
            n1 = enc2[1]
            c1 = enc2[2]
            e2 = enc2[3]
            n2 = enc2[4]
            c2 = enc2[5]
            
            e, n, c = pick_enc(e1,n1,c1,e2,n2,c2,direction1)
            s2 = final_res(e, n, c, direction2)
    
    s1 , s2 = normalization(s1), normalization(s2)
    
    score1 = []
    score2 = []
    for m, n in zip(metric_score1, s1):
        score1.append(m+n)
        
    for m, n in zip(metric_score2, s2):
        score2.append(m+n)
        
    
    accuracy = comp(score1, score2)
    print('bertscore + nli: %f' % (accuracy))
    
def mover_nli(phenomenon, dataset, model, direction1, direction2):
    from moverscore import word_mover_score 
    from collections import defaultdict
    idf_dict_hyp = defaultdict(lambda: 1.)
    idf_dict_ref = defaultdict(lambda: 1.)
    
    _, ref, _, hyp1, hyp2, hyp3, hyp4 = get_data(phenomenon, dataset)
    
    metric_score1 = []
    metric_score2 = []
    if phenomenon == 'drop' or phenomenon == 'vb':
        metric_score1 = word_mover_score(ref, hyp1, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
        metric_score2 = word_mover_score(ref, hyp3, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
    elif phenomenon == 'jj':
        metric_score1 = word_mover_score(ref, hyp1, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
        metric_score2 = word_mover_score(ref, hyp4, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
    else:
        metric_score1 = word_mover_score(ref, hyp1, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
        metric_score2 = word_mover_score(ref, hyp2, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
            
    metric_score1 = normalization(metric_score1)
    metric_score2 = normalization(metric_score2)
    
    nli_score1, nli_score2 = read_result(phenomenon, model, dataset)
    
    
    
    for enc1, enc2 in zip(nli_score1, nli_score2):
            e1 = enc1[0]
            n1 = enc1[1]
            c1 = enc1[2]
            e2 = enc1[3]
            n2 = enc1[4]
            c2 = enc1[5]
            
            e, n, c = pick_enc(e1,n1,c1,e2,n2,c2,direction1)
            s1 = final_res(e, n, c, direction2)
            
            e1 = enc2[0]
            n1 = enc2[1]
            c1 = enc2[2]
            e2 = enc2[3]
            n2 = enc2[4]
            c2 = enc2[5]
            
            e, n, c = pick_enc(e1,n1,c1,e2,n2,c2,direction1)
            s2 = final_res(e, n, c, direction2)
    
    s1 , s2 = normalization(s1), normalization(s2)
    
    score1 = []
    score2 = []
    for m, n in zip(metric_score1, s1):
        score1.append(m+n)
        
    for m, n in zip(metric_score2, s2):
        score2.append(m+n)
        
    
    accuracy = comp(score1, score2)
    print('moverscore + nli: %f' % (accuracy))

if __name__ == '__main__':
    phenomenon = 'add'
    dataset = 'wmt'
    model = 1
    direction1 = 5
    direction2 = 5
    
    bart_nli(phenomenon, dataset, model, direction1, direction2)
    bert_nli(phenomenon, dataset, model, direction1, direction2)
    mover_nli(phenomenon, dataset, model, direction1, direction2)
    