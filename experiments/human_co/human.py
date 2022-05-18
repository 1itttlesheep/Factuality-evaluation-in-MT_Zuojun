import enum
from metric1 import nli_score




refs = {}
refs['cs-en'] = {}
refs['de-en'] = {}
refs['ru-en'] = {}
refs['tr-en'] = {}
refs['zh-en'] = {}

with open('wmt17/txt/references/newstest2017-csen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['cs-en'][str(i)] = l.strip()
        
with open('wmt17/txt/references/newstest2017-deen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['de-en'][str(i)] = l.strip()
        
with open('wmt17/txt/references/newstest2017-ruen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['ru-en'][str(i)] = l.strip()
       
with open('wmt17/txt/references/newstest2017-tren-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['tr-en'][str(i)] = l.strip()

with open('wmt17/txt/references/newstest2017-zhen-ref.en', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        refs['zh-en'][str(i)] = l.strip()

lines = [line.rstrip('\n') for line in open('wmt17/DA-seglevel.csv', 'r', encoding='utf-8')]
lines.pop(0)
manual = {}
for l in lines:
    l = l.replace("nmt-smt-hybrid","nmt-smt-hybr")
    c = l.split()
    
    lp, data, system, sid, score = c[0], c[1], c[2], c[3], c[4]    
    c = system.split("+")
    system = c[0]

    if lp not in manual:
        manual[lp] = {}
    if system not in manual[lp]:
        manual[lp][system] = {}
        
    manual[lp][system][sid] = float(score)
hs = []
ns = []
p1 = []
p2 = []
for lp in manual.keys():
    if lp == 'de-en':
        for sys in manual[lp].keys():
            path = 'wmt17/txt/system-outputs/newstest2017/'+lp+'/newstest2017.'+sys+'.'+lp
            try:
                lines = [line.rstrip('\n') for line in open(path, 'r', encoding='utf-8')]
            except:
                print('file not found')
            for sid in manual[lp][sys].keys():
                # if len(p1) > 10:
                #     break
                hyp = lines[int(sid)-1]
                ref = refs[lp][str(int(sid)-1)]
                p1.append(ref)
                p2.append(hyp)
                hs.append(manual[lp][sys][sid])
                
                
    
print(len(p1))     
ns= nli_score(p1, p2)  
#rs = []
re = []         
for i, p in enumerate(ns):
    #score = p[0]-p[1]-2*p[2]
    re.append((p[0][0],p[0][1],p[0][2], p[1][0],p[1][1],p[1][2], hs[i], p1[i], p2[i]))
    #rs.append(score)


with open('metricre/w17/resultde.txt', 'w', encoding='utf-8') as f:
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
        f.write('\n')


                
            
