import random
import nltk
nltk.download('omw-1.4')
from checklist.perturb import Perturb
from num2words import num2words
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import spacy
nlp = spacy.load('en_core_web_sm')


def collect_words(type):
    """Get words from the word list.

    Used for mistranslation.

    Args:
        type: The type of the words (nn, vb, or jj)

    Returns:
        A random word list of the type.
    """
    
    with open('words/' + type + '.txt', 'r') as f:
        v = []
        lines = f.readlines()
        for l in lines:
            v.append(l.strip())
    return v

def mistranslation(ref_path, out_path):
    """Get mistranslation adversarial data.

    Args:
        ref_path: Path of the txt that contains at each line: index, src, ref, r
        out_path: Path for the returned txt that contains at each line: index, src, ref, r, hyp_para, hyp_adv(nn), hyp_adv(vb), hyp_adv(jj)
        
    Returns:
        none
    """    
    ref = []
    with open(ref_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            sen = l.split('\t')
            i = sen[0].strip()
            s = sen[1].strip()
            r = sen[2].strip()
            d_r = sen[3].strip()
            ref.append((i, s, r, d_r))

    # collect words to generate hyp_adv(vb)
    vbn = collect_words('vbn')
    vbd = collect_words('vbd')
    vbg = collect_words('vbg')
    vbz = collect_words('vbz')
    vb = collect_words('vb')
    # collect words to generate hyp_adv(nn)
    nn = collect_words('nn')
    # collect words to generate hyp_adv(jj)
    jj = collect_words('jj')

    def replace_word(ref):
        """generate mistranslation hyp_adv.

        Args:
            ref: A list of tuple: (index, src, ref, r)
            
        Returns:
            A list of tuple: (index, src, ref, r, hyp_adv(nn), hyp_adv(vb), hyp_adv(jj))
        """  
        out = []
        for p in ref:
            if len(out) == 2000:
                break
            i = p[0].strip()
            s = p[1]
            r = p[2]
            d_r = p[3]
            
            # 改这里就行
            pos = nltk.pos_tag(nltk.word_tokenize(d_r))
            #pos = nltk.pos_tag(nltk.word_tokenize(r))
            
            sen_nn = []
            sig_nn = 0
            for j in range(len(pos)):
                w, tag = pos[j]
                if sig_nn == 1:
                    sen_nn.append(w)
                    continue
                
                if tag == 'NN':
                    if w.islower():
                        rword = random.choice(nn)
                        sig_nn = 1
                        sen_nn.append(rword)
                else:
                    sen_nn.append(w)
                    
                    
            sen_vb = []   
            sig_vb = 0        
            for j in range(len(pos)):
                w, tag = pos[j]
                if sig_vb == 1:
                    sen_vb.append(w)
                    continue
                
                if w != 'been' and w != 'was' and w != 'were' and w != 'is' and w != 'are' and w != 'am' and w != 'be' and w != 'has' and w != 'have':
                    if tag == 'VBN':
                        if w.islower():
                            rword = random.choice(vbn)
                            sig_vb = 1
                            sen_vb.append(rword)
                    elif tag == 'VBG':
                        if w.islower():
                            rword = random.choice(vbg)
                            sig_vb = 1
                            sen_vb.append(rword)
                    elif tag == 'VBD':
                        if w.islower():
                            rword = random.choice(vbd)
                            sig_vb = 1
                            sen_vb.append(rword)
                    elif tag == 'VBZ':
                        if w.islower():
                            rword = random.choice(vbz)
                            sig_vb = 1
                            sen_vb.append(rword)
                    elif tag == 'VB':
                        if w.islower():
                            rword = random.choice(vb)
                            sig_vb = 1
                            sen_vb.append(rword)
                    else:
                        sen_vb.append(w)
            
            sen_jj = []
            sig_jj = 0
            for j in range(len(pos)):
                w, tag = pos[j]
                if sig_jj == 1:
                    sen_jj.append(w)
                    continue
                
                if tag == 'JJ':
                    if w.islower():
                        rword = random.choice(jj)
                        sig_jj = 1
                        sen_jj.append(rword)
                else:
                    sen_jj.append(w)
                
            
            if sig_nn == 1 and sig_vb == 1 and sig_jj == 1:
                h_nn = " ".join(x for x in sen_nn)
                h_vb = " ".join(x for x in sen_vb)
                h_jj = " ".join(x for x in sen_jj)
                out.append((i, s, r, d_r, h_nn, h_vb, h_jj))
                
        return out
            
    out = replace_word(ref) 
    with open(out_path, 'w', encoding='utf-8') as f:
        for h in out:  
            f.write(str(h[0]))
            f.write('\t')
            f.write(h[1])
            f.write('\t')
            f.write(h[2])
            f.write('\t')
            f.write(h[3])
            f.write('\t')
            f.write(h[4])
            f.write('\t')
            f.write(h[5])
            f.write('\t')
            f.write(h[5])
            f.write('\n')
    
    # get hyp_para        
    back_trans(out_path,out_path)
    
def pronoun(ref_path, out_path):
    """Get pronoun adversarial data.

    Args:
        ref_path: Path of the txt that contains at each line: index, src, ref, r
        out_path: Path for the returned txt that contains at each line: index, src, ref, r, hyp_para, hyp_adv
        
    Returns:
        none
    """  
    ref = []
    with open(ref_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            sen = l.split('\t')
            i = sen[0].strip()
            s = sen[1].strip()
            r = sen[2].strip()
            d_r = sen[3].strip()
            ref.append((i, s, r, d_r))
    
    def replace_word(ref):
        """generate mistranslation hyp_adv.

        Args:
            ref: A list of tuple: (index, src, ref, r)
            
        Returns:
            A list of tuple: (index, src, ref, r, hyp_adv)
        """   
        out = []
        for p in ref:
            if len(out) == 2000:
                break
            i = p[0]
            s = p[1]
            r = p[2]
            d_r = p[3]
            
            # select the sentence based on to generate hyp_adv
            pos = nltk.pos_tag(nltk.word_tokenize(d_r))        
            
            sig = 0
            sen = []
            for j in range(len(pos)):
                w, tag = pos[j]
                if sig == 1:
                    sen.append(w)
                    continue
                
                if tag == 'PRP' or tag == 'PRP$':
                    if w == 'he':
                        if w.islower():
                            rword = 'she'
                            sig = 1
                            sen.append(rword)
                    elif w == 'she':
                        if w.islower():
                            rword = 'he'
                            sig = 1
                            sen.append(rword)
                    elif w == 'we':
                        if w.islower():
                            rword = 'they'
                            sig = 1
                            sen.append(rword)
                    elif w == 'they':
                        if w.islower():
                            rword = 'we'
                            sig = 1
                            sen.append(rword)
                    elif w == 'his':
                        if w.islower():
                            rword = 'her'
                            sig = 1
                            sen.append(rword)
                    elif w == 'him':
                        if w.islower():
                            rword = 'her'
                            sig = 1
                            sen.append(rword)
                    elif w == 'us':
                        if w.islower():
                            rword = 'them'
                            sig = 1
                            sen.append(rword)
                    elif w == 'them':
                        if w.islower():
                            rword = 'us'   
                            sig = 1
                            sen.append(rword)   
                    elif w == 'our':
                        if w.islower():
                            rword = 'their'
                            sig = 1
                            sen.append(rword)
                    elif w == 'their':
                        if w.islower():
                            rword = 'our'
                            sig = 1
                            sen.append(rword)
                else:
                    sen.append(w)
                    
            
                    
            if sig == 1:
                print(sen)
                h_adv = " ".join(x for x in sen)
                out.append((i, s, r, d_r, h_adv))
                
        return out

                
    out = replace_word(ref) 
    with open(out_path, 'w', encoding='utf-8') as f:
        for h in out:  
            f.write(str(h[0]))
            f.write('\t')
            f.write(h[1])
            f.write('\t')
            f.write(h[2])
            f.write('\t')
            f.write(h[3])
            f.write('\t')
            f.write(h[4])
            f.write('\n')
    
    # get hyp_para
    back_trans(out_path, out_path)
    

def drop_phrases(sent):
    """drop a random phrase in the sentence
    
    Used to generate drop hyp_adv

    Args:
        sent: The reference sentence
        
    Returns:
        The adversarial sentence (hyp_adv) of the reference sentence
    """ 
    pos = nltk.pos_tag(nltk.word_tokenize(sent))
    sen = []
    l = len(pos)
    flag = 0
    le = round(l*0.2)
    x = random.randint(0,le-1)
    y = 0
    for i in range(l-1):
        w, p = pos[i]
        if x<=i and y < round(l*0.2): 
            y+=1
            flag = 1
            continue
        else:
            sen.append(w)
    sen.append(pos[l-1][0])
    if flag==1: 
        out = " ".join(w for w in sen)
    return out if flag  else sent

def add_object(sent):
    """add an object in the sentence
    
    Used to generate add hyp_adv
    
    Args:
        sent: The reference sentence
        
    Returns:
        The adversarial sentence (hyp_adv) of the reference sentence
    """
    # collect noun words
    nn = collect_words('nn')
    pos = nltk.pos_tag(nltk.word_tokenize(sent))
    sen = []
    l = len(pos)
    flag = 0
    flag1 = 0
    for i in range(l-1):
        w, p = pos[i]
        if flag == 0 and p in ['NN']: 
            a = random.choice(nn)
            # replace a noun word
            w = w + ' and ' + a
            flag = 1
            sen.append(w)
        elif flag1 == 0 and w == 'is': 
            w = 'are'
            flag1 = 1
            sen.append(w)
        elif flag1 == 0 and w == 'has': 
            w = 'have'
            flag1 = 1
            sen.append(w)
        else:
            sen.append(w)
    sen.append(pos[l-1][0])
    if flag==1: 
        out = " ".join(w for w in sen)
    return out if flag  else sent
              
def add_drop(ref_path, out_path):
    """Get add+drop adversarial data.

    Args:
        ref_path: Path of the txt that contains at each line: index, src, ref, r
        out_path: Path for the returned txt that contains at each line: index, src, ref, r, hyp_para, hyp_adv(add), hyp_adv(omi)
        
    Returns:
        none
    """  
    ref = []
    with open(ref_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            sen = l.split('\t')
            i = sen[0].strip()
            s = sen[1].strip()
            r = sen[2].strip()
            d_r = sen[3].strip()
            ref.append((i, s, r, d_r))

    hyp = []
    for p in ref:
        i = p[0]
        s = p[1]
        r = p[2]
        d_r = p[3]
        try:
            # modify the reference sentence
            ret1 = add_object(d_r)
            ret2 = drop_phrases(d_r)
        except:
            continue
        else:
            if ret1 != d_r and ret2 != d_r:
                hyp.append((i, s, r, d_r, ret1, ret2))
        
        if len(hyp) == 2000:
            break

    with open(out_path, 'w', encoding='utf-8') as f:
        for h in hyp:
            f.write(str(h[0]))
            f.write('\t')
            f.write(str(h[1]))
            f.write('\t')
            f.write(str(h[2]))
            f.write('\t')
            f.write(str(h[3]))
            f.write('\t')
            f.write(str(h[4]))
            f.write('\t')
            f.write(str(h[5]))
            f.write('\n')
    
    back_trans(out_path, out_path)
            
            
def name(ref_path, out_path):
    """Get name adversarial data.

    Args:
        ref_path: Path of the txt that contains at each line: index, src, ref, r
        out_path: Path for the returned txt that contains at each line: index, src, ref, r, hyp_para, hyp_adv
        
    Returns:
        none
    """ 
    ref = []
    with open(ref_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            sen = l.split('\t')
            i = sen[0].strip()
            s = sen[1].strip()
            r = sen[2].strip()
            d_r = sen[3].strip()
            ref.append((i, s, r, d_r))
    
    hyp = []
    
    
    for p in ref:
        j = p[0]
        s = p[1]
        r = p[2]
        d_r = p[3]
        doc = []
        
        
        # get name hyp_adv
        doc.append(nlp(d_r))
        ret1 = Perturb.perturb(doc, Perturb.change_names, keep_original=False)
        if ret1.data:
            hyp.append((j, s, r, d_r, (ret1.data)[0][0]))
        if len(hyp) == 2000:
            break
    
    with open(out_path, 'w', encoding='utf-8') as f:
        for h in hyp:
            f.write(str(h[0]))
            f.write('\t')
            f.write(str(h[1]))
            f.write('\t')
            f.write(str(h[2]))
            f.write('\t')
            f.write(str(h[3]))
            f.write('\t')
            f.write(str(h[4]))
            f.write('\n')
    
    # get hyp_para
    back_trans(out_path, out_path)
            
def negation(ref_path, out_path):
    """Get nagetion adversarial data.

    Args:
        ref_path: Path of the txt that contains at each line: index, src, ref, r
        out_path: Path for the returned txt that contains at each line: index, src, ref, r, hyp_para, hyp_adv
        
    Returns:
        none
    """ 
    ref = []
    with open(ref_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            sen = l.split('\t')
            i = sen[0].strip()
            s = sen[1].strip()
            r = sen[2].strip()
            d_r = sen[3].strip()
            ref.append((i, s, r, d_r))
    
    hyp = []
    
    for p in ref:
        j = p[0]
        s = p[1]
        r = p[2]
        d_r = p[3]
        doc = []
        doc.append(nlp(d_r))
        # get hyp_para
        ret1 = Perturb.perturb([r], Perturb.contractions, keep_original=False)
        # get hyp_ adv
        ret2 = Perturb.perturb(doc, Perturb.remove_negation, keep_original=False)
        if ret1.data and ret2.data:
            #print(len(hyp))
            hyp.append((j, s, r, d_r, (ret1.data)[0][0], (ret2.data)[0][0]))
        if len(hyp) == 200:
            break
    
    with open(out_path, 'w', encoding='utf-8') as f:
        for h in hyp:
            f.write(str(h[0]))
            f.write('\t')
            f.write(str(h[1]))
            f.write('\t')
            f.write(str(h[2]))
            f.write('\t')
            f.write(str(h[3]))
            f.write('\t')
            f.write(str(h[4]))
            f.write('\t')
            f.write(str(h[5]))
            f.write('\n')
     
def number2words(sent):
    """translate a digit number into word or replace it with another
    
    Used to generate number hyp_para and hyp_adv
    
    Args:
        sent: The reference sentence
        
    Returns:
        The paraphrase (hyp_para) and the adversarial sentence (hyp_adv) of the reference sentence
    """
    
    out = ''
    hyp2 = ''
    label = 0
    date = 0
    for i in sent.split(' '):
        # exclude date
        if i in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'November', 'October', 'December']:
            date = 1
        # exclude number for years
        if i.isdigit() and not label and len(i) < 4:
            # get hyp_para
            out = out + num2words(i) + ' '
            label = 1
            # get hyp_adv
            if int(i) < 10:
                newi = random.randint(0,10)
            elif int(i) < 100:
                newi = random.randint(0,100)
            elif int(i) < 1000:
                newi = random.randint(0,1000)
            hyp2 = hyp2 + str(newi) + ' '
        else:
            out = out + i + ' '
            hyp2 = hyp2 + i + ' '
        if date:
            out = sent
    return out.strip(), hyp2.strip()
            
def num(ref_path, out_path):
    """Get number adversarial data.

    Args:
        ref_path: Path of the txt that contains at each line: index, src, ref, r
        out_path: Path for the returned txt that contains at each line: index, src, ref, r, hyp_para, hyp_adv
        
    Returns:
        none
    """ 
    ref = []
    with open(ref_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            sen = l.split('\t')
            i = sen[0].strip()
            s = sen[1].strip()
            r = sen[2].strip()
            d_r = sen[3].strip()
            ref.append((i, s, r, d_r))
            
    hyp = []
    error = []
    for p in ref:
        i = p[0]
        s = p[1]
        r = p[2]
        d_r = p[3]
        # get hyp_para and hyp_adv
        hyp1, hyp2 = number2words(d_r)
            
        if hyp1 != d_r:
            #print(len(hyp))
            hyp.append((i, s, r, d_r, hyp1, hyp2))
        if hyp1 == r:
            error.append(i)
        
        if len(hyp) == 200:
            break


        
    with open(out_path, 'w', encoding='utf-8') as f:
        for h in hyp:
            f.write(str(h[0]))
            f.write('\t')
            f.write(str(h[1]))
            f.write('\t')
            f.write(str(h[2]))
            f.write('\t')
            f.write(str(h[3]))
            f.write('\t')
            f.write(str(h[4]))
            f.write('\t')
            f.write(str(h[5]))
            f.write('\n')
            
def back_trans(in_path, out_path):
    """Get back-translated sentences
    
    Used to get hyp_para.

    Args:
        in_path: Path of the txt that contains at each line: index, src, ref, r, hyp_adv (or more)
        out_path: Path for the returned txt that contains at each line: index, src, ref, r, hyp_para, hyp_adv
        
    Returns:
        none
    """ 

    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-de")

    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-de")

    tokenizer_b = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")

    model_b = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")

    ref = []
    with open(in_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            sens = []
            for s in l:
                sens.append(s)
                
            ref.append(sens)

    hyp = []
    for p in ref:
        i = p[0]
        r = p[3]
        batch = tokenizer([r], return_tensors="pt")
        generated_ids = model.generate(**batch)
        back = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        batch_b = tokenizer_b([back], return_tensors="pt")
        generated_ids_b = model_b.generate(**batch_b)
        hyp1 = tokenizer_b.batch_decode(generated_ids_b, skip_special_tokens=True)[0]
        
        if hyp1 != r and (len(hyp1) - len(r) <= 7) and (len(r) - len(hyp1) <= 10):
            #print(len(hyp))
            senspair = []
            for i in range(len(p)):
                if i == 4:
                    senspair.append(hyp1)
                    
                senspair.append(p[i])
                
            hyp.append(senspair)
            
        if len(hyp) == 200:
            break

    with open(out_path, 'w', encoding='utf-8') as f:
        for h in hyp:
            for i in range(len(h)):
                f.write(str(h[i]))
                if i == len(h) - 1:
                    f.write('\n')
                else:
                    f.write('\t')


if __name__ == '__main__': 
    # need to unpack zip
    add_drop('desr.txt', 'adversarial test/wmt/de/add_drop.txt')
    negation('desr.txt', 'adversarial test/wmt/de/negation.txt')
    mistranslation('desr.txt', 'adversarial test/wmt/de/word.txt')
    num('desr.txt', 'adversarial test/wmt/de/num.txt')
    pronoun('desr.txt', 'adversarial test/wmt/de/pron.txt')
    name('desr.txt', 'adversarial test/wmt/de/name.txt')
    