def comp(h1,h2):
    greater1 = 0
    greater2 = 0
    for i1 in h1.keys():
        if i1 in h2.keys():
            s1 = h1[i1]
            s2 = h2[i1]
            score1 = float(s1[0])-float(s1[1])-2*float(s1[2])
            score2 = float(s2[0])-float(s2[1])-2*float(s2[2])
            if score1 > score2:
                greater1 += 1
            elif score1 < score2:
                greater2 += 1
            else:
                print(s1)


    print(greater1/(greater1+greater2))
    
def start(p1,p2):   
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
            h1[i] = (e1,n1,c1) if e1 > e2 else (e2,n2,c2)
            #h1[i] = (e1,n1,c1) if e1 < e2 else (e2,n2,c2)
            
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
            h2[i] = (e1,n1,c1) if e1 > e2 else (e2,n2,c2)
            #h2[i] = (e1,n1,c1) if e1 < e2 else (e2,n2,c2)

    comp(h1,h2)     

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

    comp(h1,h2)    

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
            h1[i] = (max(e1,e2), max(n1,n2), max(c1,c2))
            
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
            h2[i] = (max(e1,e2), max(n1,n2), max(c1,c2))

    comp(h1,h2)  

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
            h1[i] = (min(e1,e2), min(n1,n2), min(c1,c2))
            
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
            h2[i] = (min(e1,e2), min(n1,n2), min(c1,c2))

    comp(h1,h2)

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
            h1[i] = (e1,n1,c1)
            
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
            h2[i] = (e1,n1,c1)

    comp(h1,h2)

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
            h1[i] = (e2,n2,c2)
            
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
            h2[i] = (e2,n2,c2)

    comp(h1,h2)

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
            h1[i] = ((e1+e2)/2,(n1+n2)/2,(c1+c2)/2)
            
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
            h2[i] = ((e1+e2)/2,(n1+n2)/2,(c1+c2)/2)

    comp(h1,h2)

print('add---------------')
start('non/result1/add1h1r.txt','non/result1/add1r.txt')
print('drop---------------')
start('non/result1/addh1r.txt','non/result1/dropr.txt')
print('neg---------------')
start('non/result1/negh1r.txt','non/result1/negr.txt')
print('nn---------------')
start('non/result1/nnh1r.txt','non/result1/nnr.txt')
print('vb---------------')
start('non/result1/nnh1r.txt','non/result1/vbr.txt')
print('jj---------------')
start('non/result1/nnh1r.txt','non/result1/jjr.txt')
print('num---------------')
start('non/result1/numh1r.txt','non/result1/numr.txt')
print('pron---------------')
start('non/result1/pronh1r.txt','non/result1/pronr.txt')
print('name---------------')
start('non/result1/nameh1r.txt','non/result1/namer.txt')


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

# greater1 = 0
# greater2 = 0
# for i1 in h1.keys():
#     if i1 in h2.keys():
#         s1 = h1[i1]
#         s2 = h2[i1]
#         score1 = float(s1[0])-float(s1[2])
#         score2 = float(s2[0])-float(s2[2])
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
#         score1 = float(s1[0])-float(s1[1])
#         score2 = float(s2[0])-float(s2[1])
#         if score1 > score2:
#             greater1 += 1
#         elif score1 < score2:
#             greater2 += 1
#         else:
#             print(s1)

# print(greater1/(greater1+greater2))


