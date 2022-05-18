import enum
from metric1 import nli_score
from bart_score import BARTScorer
bart_scorer = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')

def human_cor(lg,nli):

    refs = {}
    refs[lg+'-en'] = {}


    with open('w16/references/newstest2016-'+lg+'en-ref.en', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            refs[lg+'-en'][str(i)] = l.strip()
            

            


    lines_in = [line.rstrip('\n') for line in open('w16/wmt16-master/data/wmt16.'+lg+'-eng.csv')]
    lines.pop(0)
    lines = []
    for line in lines_in:
        if line:
            lines.append(line)

    manual = {}

    for l in lines:
        c = l.split(',')
        if len(c) != 10:
            print ("error in manual evaluation file")
            exit(1)

        srclang = c[0]
        trglang = c[1]
        lp = srclang+'-'+trglang
        sid = c[2] 
        rank1 = c[6]
        rank2 = c[8]
        if rank1 < rank2:
            better = c[5]
            worse = c[7]
        elif rank1 > rank2:
            better = c[7]
            worse = c[5]
        else:
            continue
            
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
        if lp == lg+'-en':
            for sid in manual[lp].keys():
                ref = refs[lp][str(int(sid)-1)]
                if len(ref) > 30:
                    pairs = []
                    for better in manual[lp][sid].keys():
                        pathb = 'w16/system-outputs/newstest2016/'+lp+'/'+better
                        try:
                            linesb = [line.rstrip('\n') for line in open(pathb, 'r', encoding='utf-8')]
                            for worse in manual[lp][sid][better].keys():
                                if len(rs) > 559:
                                    break
                                pathw = 'w16/system-outputs/newstest2016/'+lp+'/'+worse
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


    with open('metricre/w16/rr/result'+nli+lg+'.txt', 'w', encoding='utf-8') as f:
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


human_cor('cs','2')
                
            
