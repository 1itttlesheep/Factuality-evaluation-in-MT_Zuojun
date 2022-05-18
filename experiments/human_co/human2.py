import enum
from metric1 import nli_score



def get_nli_score(language):
    refs = {}
    refs[language+'-en'] = []

    with open('wmt18/references/newstest2018-'+ language + 'en-ref.en', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            refs[language+'-en'].append(l.strip())
            
    

    lines = [line.rstrip('\n') for line in open('wmt18/DA-syslevel.csv', 'r', encoding='utf-8')]
    lines.pop(0)
    manual = {}
    for l in lines:
        l = l.replace("nmt-smt-hybrid","nmt-smt-hybr")
        c = l.split()
        
        lp, score, system = c[0], c[1], c[2]   

        if lp not in manual:
            manual[lp] = {}
        if system not in manual[lp]:
            manual[lp][system] = {}
            
        manual[lp][system] = float(score)
    ns = []

    re = []     
    for lp in manual.keys():
        if lp == language+'-en':
            for sys in manual[lp].keys():
                path = 'wmt18/system-outputs/'+lp+'/newstest2018.'+sys+'.'+lp
                try:
                    lines = [line.rstrip('\n') for line in open(path, 'r', encoding='utf-8')]
                except:
                    print('file not found')
                    
                p1 = []
                p2 = []    
                for i,l in enumerate(lines):
                    if len(p1) > 100:
                        break
                    hyp = l
                    ref = refs[lp][i]
                    p1.append(ref)
                    p2.append(hyp)
                    
                ns= nli_score(p1, p2)
        
                for i, p in enumerate(ns):
                    #score = p[0]-p[1]-2*p[2]
                    re.append((p[0][0],p[0][1],p[0][2],p[1][0],p[1][1],p[1][2],lp,sys,p1[i],p2[i]))
                    #rs.append(score)


    with open('metricre/w18/da/result'+language+'.txt', 'w', encoding='utf-8') as f:
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
            f.write('\n')

if __name__ == '__main__':
    get_nli_score('ru')
                
            
