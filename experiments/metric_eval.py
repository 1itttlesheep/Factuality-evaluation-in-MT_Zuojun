from collections import defaultdict


def get_data(phenomenon, dataset):
    src = []
    ref = []
    d_r = []
    hyp1 = []
    hyp2 = []
    hyp3 = []
    hyp4 = []
    
    with open('../checklist_generate/adversarial test/'+dataset+'/'+phenomenon+'.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for l in lines:
                line = l.split('\t')
                if dataset == 'wmt':
                    src.append(line[1].strip())
                    ref.append(line[2].strip())
                    d_r.append(line[3].strip())
                    hyp1.append(line[4].strip())
                    hyp2.append(line[5].strip())
                    if len(line) == 7:
                        hyp3.append(line[6])
                    if len(line) == 8:
                        hyp4.append(line[7])
                if dataset == 'paws1'or dataset == 'paws2':
                    d_r.append(line[1].strip())
                    hyp1.append(line[2].strip())
                    hyp2.append(line[3].strip())
                    if len(line) == 5:
                        hyp3.append(line[4])
                    if len(line) == 6:
                        hyp4.append(line[5])
                        
    return src, ref, d_r, hyp1, hyp2, hyp3, hyp4

def comp(score1, score2):
    g1 = 0 
    g2 = 0
    for s1, s2 in zip(score1, score2):
        if s1 > s2:
            g1 += 1
        elif s1 < s2:
            g2 += 1
    
    return g1 / (g1 + g2)

def bart_eval(ref, hyp1, hyp2):
    from bart_score import BARTScorer
    
    bart_scorer = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')
    
    score1 = bart_scorer.score(ref, hyp1, batch_size=4)
    score2 = bart_scorer.score(ref, hyp2, batch_size=4)
    accuracy = comp(score1, score2)
    print('bartscore: %f' % (accuracy))
    
def bert_eval(ref, hyp1, hyp2):
    from bertscore import be_score
    
    (f1, _, _), _ = be_score(hyp1, ref, lang="en", return_hash=True)  
    (f2, _, _), _ = be_score(hyp2, ref, lang="en", return_hash=True)  
    accuracy = comp(f1, f2)
    print('bertscore: %f' % (accuracy))
    
def mover_eval(ref, hyp1, hyp2):
    from moverscore import word_mover_score 
    
    idf_dict_hyp = defaultdict(lambda: 1.)
    idf_dict_ref = defaultdict(lambda: 1.)
    score1 = word_mover_score(ref, hyp1, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
    score2 = word_mover_score(ref, hyp2, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
    accuracy = comp(score1, score2)
    print('moverscore: %f' % (accuracy))
    
def xmover_eval(src, ref, hyp2):
    from xmover_scorer import XMOVERScorer
    from mosestokenizer import MosesDetokenizer
    import numpy as np
    import torch
    scorer = XMOVERScorer('bert-base-multilingual-cased', 'gpt2', False)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    temp = np.load('mapping/layer-8/europarl-v7.%s-%s.2k.%s.BAM' % ('de', 'en', 8), allow_pickle=True)
    projection = torch.tensor(temp, dtype=torch.float).to(device)
    
    temp = np.load('mapping/layer-8/europarl-v7.%s-%s.2k.%s.GBDD' % ('de', 'en', 8), allow_pickle=True)
    bias = torch.tensor(temp, dtype=torch.float).to(device)
    
    with MosesDetokenizer('de') as detokenize:        
        source = [detokenize(s.split(' ')) for s in src]         
    with MosesDetokenizer('en') as detokenize:                
        references = [detokenize(s.split(' ')) for s in ref]        
        translations = [detokenize(s.split(' ')) for s in hyp2]
    
    x_hyp = scorer.compute_xmoverscore('CLP', projection, bias, source, translations, ngram=1, \
                                              layer=8, dropout_rate=0.3, bs=8)
    x_ref = scorer.compute_xmoverscore('CLP', projection, bias, source, references, ngram=1, \
                                              layer=8, dropout_rate=0.3, bs=8)
    
    accuracy = comp(x_ref, x_hyp)
    print('xmoverscore: %f' % (accuracy))
    
def bleurt_eval(ref, hyp1, hyp2):
    from bleurt import score
    checkpoint = "BLEURT-20-D12"
    scorer = score.BleurtScorer(checkpoint)
    score1 = scorer.score(references=ref, candidates=hyp1)
    score2 = scorer.score(references=ref, candidates=hyp2)
    accuracy = comp(score1, score2)
    print('bleurt: %f' % (accuracy))
    


if __name__ == '__main__': 
    
    # wmt test
    src, ref, d_r, hyp1, hyp2, hyp3, hyp4 = get_data('name', 'wmt')
    bart_eval(d_r, hyp1, hyp2)
    bleurt_eval(d_r, hyp1, hyp2)
    bert_eval(d_r, hyp1, hyp2)
    mover_eval(d_r, hyp1, hyp2)
    xmover_eval(src, ref, hyp2)
    
    # paws1 test
    src, ref, d_r, hyp1, hyp2, hyp3, hyp4 = get_data('name', 'paws1')
    bart_eval(d_r, hyp1, hyp2)
    bleurt_eval(d_r, hyp1, hyp2)
    bert_eval(d_r, hyp1, hyp2)
    mover_eval(d_r, hyp1, hyp2)
    
    # paws2 test
    src, ref, d_r, hyp1, hyp2, hyp3, hyp4 = get_data('name', 'paws2')
    bart_eval(d_r, hyp1, hyp2)
    bleurt_eval(d_r, hyp1, hyp2)
    bert_eval(d_r, hyp1, hyp2)
    mover_eval(d_r, hyp1, hyp2)
    

    
    