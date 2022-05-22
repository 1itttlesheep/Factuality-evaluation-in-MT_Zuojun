def comp(h1,h2):
    # greater1 = 0
    # greater2 = 0
    # for i1 in h1.keys():
    #     if i1 in h2.keys():
    #         s1 = h1[i1]
    #         s2 = h2[i1]
    #         score1 = float(s1[0])
    #         score2 = float(s2[0])
    #         if score1 > score2:
    #             greater1 += 1
    #         elif score1 < score2:
    #             greater2 += 1
    #         else:
    #             print(s1)

    # print(greater1/(greater1+greater2))

    # greater1 = 0
    # greater2 = 0
    # for i1 in h1.keys():
    #     if i1 in h2.keys():
    #         s1 = h1[i1]
    #         s2 = h2[i1]
    #         score1 = -float(s1[1])
    #         score2 = -float(s2[1])
    #         if score1 > score2:
    #             greater1 += 1
    #         elif score1 < score2:
    #             greater2 += 1
    #         else:
    #             print(s1)

    # print(greater1/(greater1+greater2))

    # greater1 = 0
    # greater2 = 0
    # for i1 in h1.keys():
    #     if i1 in h2.keys():
    #         s1 = h1[i1]
    #         s2 = h2[i1]
    #         score1 = -float(s1[2])
    #         score2 = -float(s2[2])
    #         if score1 > score2:
    #             greater1 += 1
    #         elif score1 < score2:
    #             greater2 += 1
    #         else:
    #             print(s1)

    # print(greater1/(greater1+greater2))

    greater1 = 0
    greater2 = 0
    for i1 in h1.keys():
        if i1 in h2.keys():
            s1 = h1[i1]
            s2 = h2[i1]
            score1 = float(s1[0])-float(s1[2])
            score2 = float(s2[0])-float(s2[2])
            if score1 > score2:
                greater1 += 1
            elif score1 < score2:
                greater2 += 1
            else:
                print(s1)

    print(greater1/(greater1+greater2))

    # greater1 = 0
    # greater2 = 0
    # for i1 in h1.keys():
    #     if i1 in h2.keys():
    #         s1 = h1[i1]
    #         s2 = h2[i1]
    #         score1 = float(s1[0])-float(s1[1])
    #         score2 = float(s2[0])-float(s2[1])
    #         if score1 > score2:
    #             greater1 += 1
    #         elif score1 < score2:
    #             greater2 += 1
    #         else:
    #             print(s1)

    # print(greater1/(greater1+greater2))
    
    # greater1 = 0
    # greater2 = 0
    # for i1 in h1.keys():
    #     if i1 in h2.keys():
    #         s1 = h1[i1]
    #         s2 = h2[i1]
    #         score1 = float(s1[0])-float(s1[1])-2*float(s1[2])
    #         score2 = float(s2[0])-float(s2[1])-2*float(s2[2])
    #         if score1 > score2:
    #             greater1 += 1
    #         elif score1 < score2:
    #             greater2 += 1
    #         else:
    #             print(s1)

    # print(greater1/(greater1+greater2))

def comb_comp(h1,h2,hm):
    greater1 = 0
    greater2 = 0
    for i in h1.keys():
            s1 = h1[i]
            s2 = h2[i]
            sm = hm[i]
            score1 = (float(s1[0])-float(s1[1]) + sm[0]) / 2
            score2 = (float(s2[0])-float(s2[1]) + sm[1]) / 2
            
            if score1 > score2:
                greater1 += 1
            elif score1 < score2:
                greater2 += 1
            else:
                print(s1)

    print(greater1/(greater1+greater2))



    
    

def nli_result(p1,p2):
    h1 = {}
    with open(p1, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:  
            d = line.split('\t')
            i = float(d[0].strip())
            e1 = float(d[1].strip())
            n1 = float(d[2].strip())
            c1 = float(d[3].strip())
            e2 = float(d[4].strip())
            n2 = float(d[5].strip())
            c2 = float(d[6].strip())
            h1[i] = (e1,n1,c1) if e1 < e2 else (e2,n2,c2)
            #h1[i] = (max(e1,e2), max(n1,n2), max(c1,c2))
            
    h2 = {}
    with open(p2, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:  
            d = line.split('\t')
            i = float(d[0].strip())
            e1 = float(d[1].strip())
            n1 = float(d[2].strip())
            c1 = float(d[3].strip())
            e2 = float(d[4].strip())
            n2 = float(d[5].strip())
            c2 = float(d[6].strip())
            h2[i] = (e1,n1,c1) if e1 < e2 else (e2,n2,c2)
            #h2[i] = (max(e1,e2), max(n1,n2), max(c1,c2))

    comp(h1,h2)

def comb_result(p1,p2,pm):
    h1 = {}
    with open(p1, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):  
            d = line.split('\t')
            e1 = float(d[1].strip())
            n1 = float(d[2].strip())
            c1 = float(d[3].strip())
            e2 = float(d[4].strip())
            n2 = float(d[5].strip())
            c2 = float(d[6].strip())
            h1[i] = (e1,n1,c1)# if e1 > e2 else (e2,n2,c2)
            
    h2 = {}
    with open(p2, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            d = line.split('\t')
            e1 = float(d[1].strip())
            n1 = float(d[2].strip())
            c1 = float(d[3].strip())
            e2 = float(d[4].strip())
            n2 = float(d[5].strip())
            c2 = float(d[6].strip())
            h2[i] = (e1,n1,c1)# if e1 > e2 else (e2,n2,c2)
            
    hm = {}
    with open(pm, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            d = line.split('\t')
            s1 = float(d[1].strip())
            s2 = float(d[2].strip())
            hm[i] = (s1,s2)# if e1 > e2 else (e2,n2,c2)
    
    comb_comp(h1,h2,hm)


#print('add---------------')
nli_result('non/result1/add1h1r.txt','non/result1/add1r.txt')#, 'non/mover/addr.txt')
#print('drop---------------')
nli_result('non/result1/addh1r.txt','non/result1/dropr.txt')#, 'non/mover/dropr.txt')
#print('neg---------------')
nli_result('non/result1/negh1r.txt','non/result1/negr.txt')#, 'non/mover/addr.txt')
#print('nn---------------')
nli_result('non/result1/nnh1r.txt','non/result1/nnr.txt')#, 'non/mover/nnr.txt')
#print('vb---------------')
nli_result('non/result1/nnh1r.txt','non/result1/vbr.txt')#, 'non/mover/vbr.txt')
#print('jj---------------')
nli_result('non/result1/nnh1r.txt','non/result1/jjr.txt')#, 'non/mover/jjr.txt')
#print('num---------------')
nli_result('non/result1/numh1r.txt','non/result1/numr.txt')#, 'non/mover/numr.txt')
#print('pron---------------')
nli_result('non/result1/pronh1r.txt','non/result1/pronr.txt')#, 'non/mover/pronr.txt')
#print('name---------------')
nli_result('non/result1/nameh1r.txt','non/result1/namer.txt')#, 'non/mover/namer.txt')
    
# print('add---------------')
# nli_result('non/result1/add1h1r.txt','non/result1/add1r.txt')
# print('drop---------------')
# nli_result('non/result1/addh1r.txt','non/result1/dropr.txt')
# print('neg---------------')
# nli_result('non/result1/negh1r.txt','non/result1/negr.txt')
# print('nn---------------')
# nli_result('non/result1/nnh1r.txt','non/result1/nnr.txt')
# print('vb---------------')
# nli_result('non/result1/nnh1r.txt','non/result1/vbr.txt')
# print('jj---------------')
# nli_result('non/result1/nnh1r.txt','non/result1/jjr.txt')
# print('num---------------')
# nli_result('non/result1/numh1r.txt','non/result1/numr.txt')
# print('pron---------------')
# nli_result('non/result1/pronh1r.txt','non/result1/pronr.txt')
# print('name---------------')
# nli_result('non/result1/nameh1r.txt','non/result1/namer.txt')
