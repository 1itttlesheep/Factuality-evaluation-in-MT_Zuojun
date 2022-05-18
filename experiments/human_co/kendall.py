from collections import defaultdict
from bertscore import be_score
#from moverscore import word_mover_score 
#from bart_score import BARTScorer
#bart_scorer = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')


hs = []
rs = []
refs = []
sens1 = []
sens2 = []
nli_scores = []
with open('metricre/w19/rr/resultlt.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    # conc = 0
    # disc = 0
    for l in lines:
        line = l.split('\t')
        #score1 = (float(line[0])-0*float(line[1])-0*float(line[2])) if float(line[1]) < float(line[4]) else (float(line[3])-0*float(line[4])-0*float(line[5]))
        #score2 = (float(line[6])-0*float(line[7])-0*float(line[8])) if float(line[7]) < float(line[10]) else (float(line[9])-0*float(line[10])-0*float(line[11]))
        #score1 = 1*0.5*(float(line[0])+float(line[3]))-1*0.5*(float(line[1])+float(line[4]))-2*0.5*(float(line[2])+float(line[5]))
        #score2 = 1*0.5*(float(line[6])+float(line[9]))-1*0.5*(float(line[7])+float(line[10]))-2*0.5*(float(line[8])+float(line[11]))
        e1 = max(float(line[0]),float(line[3]))
        n1 = max(float(line[1]),float(line[4]))
        c1 = max(float(line[2]),float(line[5]))
        e2 = max(float(line[6]),float(line[9]))
        n2 = max(float(line[7]),float(line[10]))
        c2 = max(float(line[8]),float(line[11]))
        score1 = e1-n1
        score2 = e2-n2
        nli_scores.append((score1, score2))
        refs.append(line[12])
        sens1.append(line[13])
        sens2.append(line[14])
        #bart
        #score1 = float(line[15])#+ 1*score1
        #score2 = float(line[16])#+ 1*score2
        
        # if score1 > score2:
        #     conc = conc + 1
        # else:
        #     disc = disc + 1
        
nli_scores2 = []
with open('metricre/w19/rr/result2lt.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    # conc = 0
    # disc = 0
    for l in lines:
        line = l.split('\t')
        e1 = max(float(line[0]),float(line[3]))
        n1 = max(float(line[1]),float(line[4]))
        c1 = max(float(line[2]),float(line[5]))
        e2 = max(float(line[6]),float(line[9]))
        n2 = max(float(line[7]),float(line[10]))
        c2 = max(float(line[8]),float(line[11]))
        score1 = e1-n1
        score2 = e2-n2
        nli_scores2.append((score1, score2))

# idf_dict_hyp = defaultdict(lambda: 1.)
# idf_dict_ref = defaultdict(lambda: 1.)
# ms1 = word_mover_score(refs, sens1, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
# ms2 = word_mover_score(refs, sens2, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True, batch_size=64)
(ms1, _, _), _ = be_score(sens1, refs, lang="en", return_hash=True)  
(ms2, _, _), _ = be_score(sens2, refs, lang="en", return_hash=True)  
conc = 0
disc = 0

for i, n in enumerate(nli_scores):
    score1 = float(ms1[i])
    score2 = float(ms2[i])
    
    if score1 > score2:
        conc = conc + 1
    else:
        disc = disc + 1

conc = float(conc)
disc = float(disc)
result = (conc-disc)/(conc+disc)
print("origin")
print(result)

conc = 0
disc = 0
for i, n in enumerate(nli_scores):
    score1 = n[0] + float(ms1[i])
    score2 = n[1] + float(ms2[i])
    
    if score1 > score2:
        conc = conc + 1
    else:
        disc = disc + 1

conc = float(conc)
disc = float(disc)
result = (conc-disc)/(conc+disc)
print("combine1")
print(result)

conc = 0
disc = 0
for i, n in enumerate(nli_scores2):
    score1 = n[0] + float(ms1[i])
    score2 = n[1] + float(ms2[i])
    
    if score1 > score2:
        conc = conc + 1
    else:
        disc = disc + 1

conc = float(conc)
disc = float(disc)
result = (conc-disc)/(conc+disc)
print("combine2")
print(result)






