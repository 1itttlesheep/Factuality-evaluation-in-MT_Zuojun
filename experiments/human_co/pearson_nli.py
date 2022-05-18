from scipy.stats import pearsonr
#from bart_score import BARTScorer
#bart_scorer = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')

def pearson_and_spearman(preds, labels):
    pearson_corr = pearsonr(preds, labels)[0]
    return str(pearson_corr)

# hs = []
# rs = []
# index= 0
# with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     for l in lines:
#         line = l.split('\t')
#         index += 1
#         #print(index)
#         score_nli = (float(line[0])-1*float(line[1])-1*float(line[2])) if float(line[1]) < float(line[4]) else (float(line[3])-1*float(line[4])-2*float(line[5]))
#         #score = bart_scorer.score([line[7]], [line[8]], batch_size=4)[0] + score_nli
#         score = score_nli
#         hs.append(float(line[6]))
#         rs.append(score)
        

# print(pearson_and_spearman(hs, rs))

hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        score_nli = (float(line[0])-1*float(line[1])-0*float(line[2])) if float(line[1]) < float(line[4]) else (float(line[3])-1*float(line[4])-0*float(line[5]))
        
        score = score_nli
        hs.append(float(line[6]))
        rs.append(score)
        

print(pearson_and_spearman(hs, rs))

hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        score_nli = (float(line[0])-1*float(line[1])-0*float(line[2])) if float(line[1]) > float(line[4]) else (float(line[3])-1*float(line[4])-0*float(line[5]))
        
        score = score_nli
        hs.append(float(line[6]))
        rs.append(score)
        

print(pearson_and_spearman(hs, rs))

hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        e = max(float(line[0]), float(line[3]))
        n = max(float(line[1]), float(line[4]))
        score_nli = e-n
        
        score = score_nli
        hs.append(float(line[6]))
        rs.append(score)
        

print(pearson_and_spearman(hs, rs))

hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        e = min(float(line[0]), float(line[3]))
        n = min(float(line[1]), float(line[4]))
        score_nli = e-n
        score = score_nli
        hs.append(float(line[6]))
        rs.append(score)
        

print(pearson_and_spearman(hs, rs))


hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        score = float(line[0])-1*float(line[1])-0*float(line[2])
        hs.append(float(line[6]))
        rs.append(score)

print(pearson_and_spearman(hs, rs))

hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        score = float(line[3])-1*float(line[4])-0*float(line[4])
        hs.append(float(line[6]))
        rs.append(score)

print(pearson_and_spearman(hs, rs))

# hs = []
# rs = []
# with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     for l in lines:
#         line = l.split('\t')
#         score = 1*0.5*(float(line[0])+float(line[3]))-0*0.5*(float(line[1])+float(line[4]))-0*0.5*(float(line[2])+float(line[5]))
#         hs.append(float(line[6]))
#         rs.append(score)

# print(pearson_and_spearman(hs, rs))

hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        score = 1*0.5*(float(line[0])+float(line[3]))-1*0.5*(float(line[1])+float(line[4]))-0*0.5*(float(line[2])+float(line[5]))
        hs.append(float(line[6]))
        rs.append(score)

print(pearson_and_spearman(hs, rs))

# hs = []
# rs = []
# with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     for l in lines:
#         line = l.split('\t')
#         score = 1*0.5*(float(line[0])+float(line[3]))-1*0.5*(float(line[1])+float(line[4]))-2*0.5*(float(line[2])+float(line[5]))
#         hs.append(float(line[6]))
#         rs.append(score)

# print(pearson_and_spearman(hs, rs))

hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        score_nli = (float(line[0])-1*float(line[1])-2*float(line[2])) if float(line[1]) < float(line[4]) else (float(line[3])-1*float(line[4])-2*float(line[5]))
        
        score = score_nli
        hs.append(float(line[6]))
        rs.append(score)
        

print(pearson_and_spearman(hs, rs))

hs = []
rs = []
with open('metricre/w17/result2ru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        score_nli = (float(line[0])-1*float(line[1])-1*float(line[2])) if float(line[1]) < float(line[4]) else (float(line[3])-1*float(line[4])-1*float(line[5]))
        
        score = score_nli
        hs.append(float(line[6]))
        rs.append(score)
        

print(pearson_and_spearman(hs, rs))