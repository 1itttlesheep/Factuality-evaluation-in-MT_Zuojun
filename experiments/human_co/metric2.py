from transformers import AutoTokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def nli_score(premise, hypothesis):
    tokenized_input_seq_pair = tokenizer.encode_plus(premise, hypothesis,
                                                    max_length=max_length,
                                                    return_token_type_ids=True, truncation=True)

    input_ids = torch.Tensor(tokenized_input_seq_pair['input_ids']).long().unsqueeze(0)
    # remember bart doesn't have 'token_type_ids', remove the line below if you are using bart.
    token_type_ids = torch.Tensor(tokenized_input_seq_pair['token_type_ids']).long().unsqueeze(0)
    attention_mask = torch.Tensor(tokenized_input_seq_pair['attention_mask']).long().unsqueeze(0)

    outputs = model(input_ids,
                    attention_mask=attention_mask,
                    token_type_ids=token_type_ids,
                    labels=None)
    # Note:
    # "id2label": {
    #     "0": "entailment",
    #     "1": "neutral",
    #     "2": "contradiction"
    # },

    predicted_probability = torch.softmax(outputs[0], dim=1)[0].tolist()  # batch_size only one
    
    tokenized_input_seq_pair_conv = tokenizer.encode_plus(hypothesis,premise,
                                                    max_length=max_length,
                                                    return_token_type_ids=True, truncation=True)

    input_ids_conv = torch.Tensor(tokenized_input_seq_pair_conv['input_ids']).long().unsqueeze(0)
    # remember bart doesn't have 'token_type_ids', remove the line below if you are using bart.
    token_type_ids_conv = torch.Tensor(tokenized_input_seq_pair_conv['token_type_ids']).long().unsqueeze(0)
    attention_mask_conv = torch.Tensor(tokenized_input_seq_pair_conv['attention_mask']).long().unsqueeze(0)

    outputs_conv = model(input_ids_conv,
                    attention_mask=attention_mask_conv,
                    token_type_ids=token_type_ids_conv,
                    labels=None)
    

    predicted_probability_conv = torch.softmax(outputs_conv[0], dim=1)[0].tolist()  # batch_size only one
    
    # if hg_model_hub_name == "microsoft/deberta-large-mnli":
    #     e = predicted_probability[2]
    #     c = predicted_probability[0]
    #     e1 = predicted_probability_conv[2]
    #     c1 = predicted_probability_conv[0]
    #     predicted_probability[0] = e
    #     predicted_probability[2] = c
    #     predicted_probability_conv[0] = e1
    #     predicted_probability_conv[2] = c1
    # else:
    #     e = 0
    #     n = 0
    #     c = 0
    
    if predicted_probability[0] >= 0.1 or predicted_probability_conv[0] >= 0.1:
        if predicted_probability[2] >= 0.1 or predicted_probability_conv[2] >= 0.1:
            if predicted_probability[2] >= predicted_probability_conv[2]:
                e = predicted_probability[0]
                n = predicted_probability[1]
                c = predicted_probability[2]
            else:
                e = predicted_probability_conv[0]
                n = predicted_probability_conv[1]
                c = predicted_probability_conv[2]
        else:    
            if predicted_probability[0] < predicted_probability_conv[0]:
                e = predicted_probability[0]
                n = predicted_probability[1]
                c = predicted_probability[2]
            else:
                e = predicted_probability_conv[0]
                n = predicted_probability_conv[1]
                c = predicted_probability_conv[2]
    else:
        if predicted_probability[2] >= predicted_probability_conv[2]:
            e = predicted_probability[0]
            n = predicted_probability[1]
            c = predicted_probability[2]
        else:
            e = predicted_probability_conv[0]
            n = predicted_probability_conv[1]
            c = predicted_probability_conv[2]
            
    
    
    return e, n, c
        
        

def build_list(filename):
    datalist = []
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            i = l[0].strip()
            r = l[2].strip()
            hyp1 = l[3].strip()
            hyp2 = l[4].strip()
            datalist.append((i, r, hyp1, hyp2))
        return datalist

def result_print(test, pathh1, path2):
    score1 = {}
    score2 = {}
    for tuple in test:
        i = tuple[0].strip()
        print(len(score1.keys()))
        
        r = tuple[1].strip()
        hyp1 = tuple[2].strip()
        if r == hyp1:
            continue
        hyp2 = tuple[3].strip()
        s1 = nli_score(r, hyp1)
        s2 = nli_score(r, hyp2)
        score1[i] = s1
        score2[i] = s2
        if len(score1.keys()) == 200:
            break
    
    with open(pathh1, 'w', encoding='utf-8') as f:
        for i, s in score1.items():
            f.write(i)
            f.write('\t')
            f.write(str(s[0]))
            f.write('\t')
            f.write(str(s[1]))
            f.write('\t')
            f.write(str(s[2]))
            f.write('\n')
    
    with open(path2, 'w', encoding='utf-8') as f:
        for i, s in score2.items():
            f.write(i)
            f.write('\t')
            f.write(str(s[0]))
            f.write('\t')
            f.write(str(s[1]))
            f.write('\t')
            f.write(str(s[2]))
            f.write('\n')
    
    
        
        
if __name__ == '__main__':
    
    max_length = 256
    #hg_model_hub_name = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/xlnet-large-cased-snli_mnli_fever_anli_R1_R2_R3-nli"
    #hg_model_hub_name = "prajjwal1/bert-medium-mnli"
    hg_model_hub_name = 'microsoft/deberta-large-mnli'

    tokenizer = AutoTokenizer.from_pretrained(hg_model_hub_name)
    model = AutoModelForSequenceClassification.from_pretrained(hg_model_hub_name)
        
    result_print(build_list('add/newadd_wmt.txt'),'add/result2/addwh1r.txt','add/result2/addwr.txt')