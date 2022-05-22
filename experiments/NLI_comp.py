
import numpy as np


def read_result(phenomenon, model, dataset):
    h1 = []
    with open('nli_result/NLI'+ str(model) + '/' + dataset + '/' + phenomenon + 'h1r.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:  
            d = line.split('\t')
            e1 = float(d[1].strip())
            n1 = float(d[2].strip())
            c1 = float(d[3].strip())
            e2 = float(d[4].strip())
            n2 = float(d[5].strip())
            c2 = float(d[6].strip())
            h1.append((e1,n1,c1,e2,n2,c2))
            
    h2 = []
    with open('nli_result/NLI'+ str(model) + '/' + dataset + '/' + phenomenon + 'r.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:  
            d = line.split('\t')
            e1 = float(d[1].strip())
            n1 = float(d[2].strip())
            c1 = float(d[3].strip())
            e2 = float(d[4].strip())
            n2 = float(d[5].strip())
            c2 = float(d[6].strip())
            h2.append((e1,n1,c1,e2,n2,c2))
    
    return h1, h2

def formulas_all(model, dataset):
    formulas = []
    formulas.append(read_result('add', model, dataset))
    formulas.append(read_result('drop', model, dataset))
    formulas.append(read_result('neg', model, dataset))
    formulas.append(read_result('nn', model, dataset))
    formulas.append(read_result('vb', model, dataset))
    formulas.append(read_result('jj', model, dataset))
    formulas.append(read_result('num', model, dataset))
    formulas.append(read_result('pron', model, dataset))
    formulas.append(read_result('name', model, dataset))
    return formulas

def pick_enc(e1,n1,c1,e2,n2,c2,num):
    e, n, c = 0, 0, 0
    if num == 1:
        if e1 < e2:
            e, n, c = e1, n1, c1
        else:
            e, n, c = e2, n2, c2
    elif num == 2:
        if e1 > e2:
            e, n, c = e1, n1, c1
        else:
            e, n, c = e2, n2, c2
    elif num == 3:
        e, n, c = max(e1,e2), max(n1,n2), max(c1,c2)
    elif num == 4:
        e, n, c = min(e1,e2), min(n1,n2), min(c1,c2)
    elif num == 5:
        e, n, c = e1, n1, c1
    elif num == 6:
        e, n, c = e2, n2, c2
    elif num == 7:
        e, n, c = (e1+e2)/2, (n1+n2)/2, (c1+c2)/2
    else:
        print('d1 wrong')
        
    return e, n, c
    
def final_res(e, n, c,num):
    if num == 1:
        return e
    elif num == 2:
        return -n
    elif num == 3:
        return -c
    elif num == 4:
        return e-c
    elif num == 5:
        return e-n
    elif num == 6:
        return e-n-2*c
    else:
        print('d2 wrong')

def formula_result(model, dataset, direction1, direction2):
    formulas_results = formulas_all(model, dataset)
    scores = []
    for phe in formulas_results:
        
        g1 = 0
        g2 = 0
        for enc1, enc2 in zip(phe[0], phe[1]):
            e1 = enc1[0]
            n1 = enc1[1]
            c1 = enc1[2]
            e2 = enc1[3]
            n2 = enc1[4]
            c2 = enc1[5]
            
            e, n, c = pick_enc(e1,n1,c1,e2,n2,c2,direction1)
            s1 = final_res(e, n, c, direction2)
            
            e1 = enc2[0]
            n1 = enc2[1]
            c1 = enc2[2]
            e2 = enc2[3]
            n2 = enc2[4]
            c2 = enc2[5]
            
            e, n, c = pick_enc(e1,n1,c1,e2,n2,c2,direction1)
            s2 = final_res(e, n, c, direction2)
            
            if s1 > s2:
                g1 += 1
            elif s1 < s2:
                g2 += 1
                
        scores.append(g1/(g1+g2))
        
    scores = np.array(scores)
    mean = np.mean(scores)
    return mean
        
if __name__ == '__main__':
    for i in range(1,7):
        print("----------")
        for j in range(1,8):
            wmt = formula_result(1,'wmt',j,i)
            paws1 = formula_result(1,'paws1',j,i)
            paws2 = formula_result(1,'paws2',j,i)
            print((wmt+paws1+paws2)/3)
            

            
