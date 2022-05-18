from scipy.stats import pearsonr
import statistics

def pearson_and_spearman(preds, labels):
    pearson_corr = pearsonr(preds, labels)[0]
    return "pearson: " + str(pearson_corr)

lines = [line.rstrip('\n') for line in open('wmt18/DA-syslevel.csv', 'r', encoding='utf-8')]
lines.pop(0)
manual = {}
for l in lines:
    l = l.replace("nmt-smt-hybrid","nmt-smt-hybr")
    c = l.split()
    
    lp, score, system = c[0], c[1], c[2]   

    if lp == "ru-en":
        manual[system] = float(score)

output = {}
with open('metricre/w18/da/resultru.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        line = l.split('\t')
        lp = line[6]
        sys = line[7]
        score = (float(line[0])-float(line[1])) if float(line[1]) < float(line[4]) else (float(line[3])-float(line[4]))
        if sys not in output:
            output[sys] = []
        
        output[sys].append(score)
     
hs = []
rs = []        
for sys in output:
    hs.append(manual[sys])
    rs.append(statistics.mean(output[sys])) 
    

print(pearson_and_spearman(hs, rs))

# with open('metricre/w18/da/resultde.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     for l in lines:
#         line = l.split('\t')
#         score = 1*0.5*(float(line[0])+float(line[3]))-1*0.5*(float(line[1])+float(line[4]))-1*0.5*(float(line[2])+float(line[5]))
#         hs.append(float(line[6]))
#         rs.append(score)

# print(pearson_and_spearman(hs, rs))