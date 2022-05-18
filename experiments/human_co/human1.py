import enum
from metric1 import nli_score
from bart_score import BARTScorer
bart_scorer = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')



refs = {}
refs['cs-en'] = {}
refs['de-en'] = {}
refs['ru-en'] = {}
refs['fi-en'] = {}
refs['gu-en'] = {}
refs['lt-en'] = {}
refs['zh-en'] = {}

with open('wmt19/references/newstest2019-csen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['cs-en'][str(i)] = l.strip()
        
with open('wmt19/references/newstest2019-deen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['de-en'][str(i)] = l.strip()
        
with open('wmt19/references/newstest2019-ruen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['ru-en'][str(i)] = l.strip()

with open('wmt19/references/newstest2019-lten-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['lt-en'][str(i)] = l.strip()

with open('wmt19/references/newstest2019-guen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['gu-en'][str(i)] = l.strip()

with open('wmt19/references/newstest2019-fien-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['fi-en'][str(i)] = l.strip()

with open('wmt19/references/newstest2019-zhen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['zh-en'][str(i)] = l.strip()
        


lines = [line.rstrip('\n') for line in open('WMT19/RR-seglevel.csv')]
lines.pop(0)

manual = {}

for l in lines:
    l = l.replace("nmt-smt-hybrid","nmt-smt-hybr")
    c = l.split()

    if len(c) != 5:
        print ("error in manual evaluation file")
        exit(1)

    lp = c[0]
    data = c[1]
    sid = c[2] 
    better = c[3]
    worse = c[4]
    if lp not in manual:
        manual[lp] = {}
    if sid not in manual[lp]:
        manual[lp][sid] = {}
    if better not in manual[lp][sid]:
        manual[lp][sid][better] = {}
    if worse not in manual[lp][sid][better]:
        manual[lp][sid][better][worse] = 1
        

rs = []
hypbs = []
hypws = []
scores = []
for lp in manual.keys():
    if lp == 'lt-en':
        for sid in manual[lp].keys():
            ref = refs[lp][str(int(sid)-1)]
            if len(ref) > 30:
                pairs = []
                for better in manual[lp][sid].keys():
                    pathb = 'wmt19/system-outputs/'+lp+'/newstest2019.'+better+'.'+lp
                    try:
                        linesb = [line.rstrip('\n') for line in open(pathb, 'r', encoding='utf-8')]
                        for worse in manual[lp][sid][better].keys():
                            if len(rs) > 559:
                                break
                            pathw = 'wmt19/system-outputs/'+lp+'/newstest2019.'+worse+'.'+lp
                            try:
                                linesw = [line.rstrip('\n') for line in open(pathw, 'r', encoding='utf-8')]
                                hypb = linesb[int(sid)-1]
                                hypw = linesw[int(sid)-1]
                                if (hypb, hypw) not in pairs:
                                    rs.append(ref)
                                    score1 = bart_scorer.score([ref], [hypb], batch_size=4)[0]
                                    score2 = bart_scorer.score([ref], [hypw], batch_size=4)[0]
                                    hypbs.append(hypb)
                                    hypws.append(hypw)
                                    scores.append((score1, score2))
                                    pairs.append((hypb, hypw))
                                
                            except:
                                print(pathw)
                        
                            
                        
                    except:
                        print(pathb)
                    
           
    
print(len(rs))     
bs= nli_score(rs, hypbs)  
ws= nli_score(rs, hypws)  
re = []         
for i, b in enumerate(bs):
    #score = p[0]-p[1]-2*p[2]
    w = ws[i]
    re.append((b[0][0],b[0][1],b[0][2],b[1][0],b[1][1],b[1][2],w[0][0],w[0][1],w[0][2],w[1][0],w[1][1],w[1][2],rs[i], hypbs[i], hypws[i], scores[i][0], scores[i][1]))
    #rs.append(score)


with open('metricre/w19/rr/resultlt.txt', 'w', encoding='utf-8') as f:
    for p in re:
        f.write(str(p[0]))
        f.write('\t')
        f.write(str(p[1]))
        f.write('\t')
        f.write(str(p[2]))
        f.write('\t')
        f.write(str(p[3]))
        f.write('\t')
        f.write(str(p[4]))
        f.write('\t')
        f.write(str(p[5]))
        f.write('\t')
        f.write(str(p[6]))
        f.write('\t')
        f.write(str(p[7]))
        f.write('\t')
        f.write(str(p[8]))
        f.write('\t')
        f.write(str(p[9]))
        f.write('\t')
        f.write(str(p[10]))
        f.write('\t')
        f.write(str(p[11]))
        f.write('\t')
        f.write(str(p[12]))
        f.write('\t')
        f.write(str(p[13]))
        f.write('\t')
        f.write(str(p[14]))
        f.write('\t')
        f.write(str(p[15]))
        f.write('\t')
        f.write(str(p[16]))
        f.write('\n')


                
            
