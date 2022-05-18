from scipy.stats import pearsonr
#from bart_score import BARTScorer
#bart_scorer = BARTScorer(device='cuda:0', checkpoint='facebook/bart-large-cnn')


hs = []
rs = []
with open('metricre/w16/rr/result2de.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    conc = 0
    disc = 0
    for l in lines:
        line = l.split('\t')
        score1 = (float(line[0])-1*float(line[1])-0*float(line[2])) if float(line[1]) < float(line[4]) else (float(line[3])-1*float(line[4])-0*float(line[5]))
        score2 = (float(line[6])-1*float(line[7])-0*float(line[8])) if float(line[7]) < float(line[10]) else (float(line[9])-1*float(line[10])-0*float(line[11]))
        
        if score1 > score2:
            conc = conc + 1
        else:
            disc = disc + 1

conc = float(conc)
disc = float(disc)
result = (conc-disc)/(conc+disc)

print(result)


hs = []
rs = []
with open('metricre/w16/rr/result2de.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    conc = 0
    disc = 0
    for l in lines:
        line = l.split('\t')
        score1 = (float(line[0])-1*float(line[1])-2*float(line[2])) if float(line[1]) < float(line[4]) else (float(line[3])-1*float(line[4])-2*float(line[5]))
        score2 = (float(line[6])-1*float(line[7])-2*float(line[8])) if float(line[7]) < float(line[10]) else (float(line[9])-1*float(line[10])-2*float(line[11]))
        
        if score1 > score2:
            conc = conc + 1
        else:
            disc = disc + 1

conc = float(conc)
disc = float(disc)
result = (conc-disc)/(conc+disc)

print(result)

hs = []
rs = []
with open('metricre/w16/rr/result2de.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    conc = 0
    disc = 0
    for l in lines:
        line = l.split('\t')
        score1 = (float(line[0])-0*float(line[1])-0*float(line[2])) if float(line[1]) < float(line[4]) else (float(line[3])-0*float(line[4])-0*float(line[5]))
        score2 = (float(line[6])-0*float(line[7])-0*float(line[8])) if float(line[7]) < float(line[10]) else (float(line[9])-0*float(line[10])-0*float(line[11]))
        
        if score1 > score2:
            conc = conc + 1
        else:
            disc = disc + 1

conc = float(conc)
disc = float(disc)
result = (conc-disc)/(conc+disc)

print(result)


# hs = []
# rs = []
# with open('metricre/w19/rr/resultgu.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     conc = 0
#     disc = 0
#     for l in lines:
#         line = l.split('\t')
#         score1 = (float(line[0])-1*float(line[1])-0*float(line[2])) if float(line[1]) > float(line[4]) else (float(line[3])-1*float(line[4])-0*float(line[5]))
#         score2 = (float(line[6])-1*float(line[7])-0*float(line[8])) if float(line[7]) > float(line[10]) else (float(line[9])-1*float(line[10])-0*float(line[11]))
        
#         if score1 > score2:
#             conc = conc + 1
#         else:
#             disc = disc + 1

# conc = float(conc)
# disc = float(disc)
# result = (conc-disc)/(conc+disc)

# print(result)

# hs = []
# rs = []
# with open('metricre/w19/rr/resultgu.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     conc = 0
#     disc = 0
#     for l in lines:
#         line = l.split('\t')
#         e1 = max(float(line[0]),float(line[3]))
#         n1 = max(float(line[1]),float(line[4]))
#         c1 = max(float(line[2]),float(line[5]))
#         e2 = max(float(line[6]),float(line[9]))
#         n2 = max(float(line[7]),float(line[10]))
#         c2 = max(float(line[8]),float(line[11]))
#         score1 = e1-n1
#         score2 = e2-n2
        
#         if score1 > score2:
#             conc = conc + 1
#         else:
#             disc = disc + 1

# conc = float(conc)
# disc = float(disc)
# result = (conc-disc)/(conc+disc)

# print(result)

# hs = []
# rs = []
# with open('metricre/w19/rr/resultgu.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     conc = 0
#     disc = 0
#     for l in lines:
#         line = l.split('\t')
#         e1 = min(float(line[0]),float(line[3]))
#         n1 = min(float(line[1]),float(line[4]))
#         c1 = min(float(line[2]),float(line[5]))
#         e2 = min(float(line[6]),float(line[9]))
#         n2 = min(float(line[7]),float(line[10]))
#         c2 = min(float(line[8]),float(line[11]))
#         score1 = e1-n1
#         score2 = e2-n2
        
#         if score1 > score2:
#             conc = conc + 1
#         else:
#             disc = disc + 1

# conc = float(conc)
# disc = float(disc)
# result = (conc-disc)/(conc+disc)

# print(result)

# hs = []
# rs = []
# with open('metricre/w19/rr/resultgu.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     conc = 0
#     disc = 0
#     for l in lines:
#         line = l.split('\t')
#         score1 = float(line[0])-1*float(line[1])-0*float(line[2])
#         score2 = float(line[6])-1*float(line[7])-0*float(line[8])
        
#         if score1 > score2:
#             conc = conc + 1
#         else:
#             disc = disc + 1

# conc = float(conc)
# disc = float(disc)
# result = (conc-disc)/(conc+disc)

# print(result)

# hs = []
# rs = []
# with open('metricre/w19/rr/resultgu.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     conc = 0
#     disc = 0
#     for l in lines:
#         line = l.split('\t')
#         score1 = float(line[3])-1*float(line[4])-0*float(line[5])
#         score2 = float(line[9])-1*float(line[10])-0*float(line[11])
        
#         if score1 > score2:
#             conc = conc + 1
#         else:
#             disc = disc + 1

# conc = float(conc)
# disc = float(disc)
# result = (conc-disc)/(conc+disc)

# print(result)

# hs = []
# rs = []
# with open('metricre/w19/rr/resultgu.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     conc = 0
#     disc = 0
#     for l in lines:
#         line = l.split('\t')
#         score1 = 1*0.5*(float(line[0])+float(line[3]))-1*0.5*(float(line[1])+float(line[4]))-0*0.5*(float(line[2])+float(line[5]))
#         score2 = 1*0.5*(float(line[6])+float(line[9]))-1*0.5*(float(line[7])+float(line[10]))-0*0.5*(float(line[8])+float(line[11]))
       
#         if score1 > score2:
#             conc = conc + 1
#         else:
#             disc = disc + 1

# conc = float(conc)
# disc = float(disc)
# result = (conc-disc)/(conc+disc)

# print(result)


