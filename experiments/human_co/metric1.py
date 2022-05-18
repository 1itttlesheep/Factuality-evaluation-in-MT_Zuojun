from transformers import AutoTokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def nli_score(premises, hypothesiss):
    max_length = 256
    hg_model_hub_name = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/xlnet-large-cased-snli_mnli_fever_anli_R1_R2_R3-nli"
    #hg_model_hub_name = 'prajjwal1/bert-medium-mnli'
    #hg_model_hub_name = 'microsoft/deberta-large-mnli'

    tokenizer = AutoTokenizer.from_pretrained(hg_model_hub_name)
    model = AutoModelForSequenceClassification.from_pretrained(hg_model_hub_name)
    
    res = []
    i = 0
    for premise, hypothesis in zip(premises, hypothesiss):
        i = i+1
        print(i)
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
        
        if hg_model_hub_name == "microsoft/deberta-large-mnli":
            e = predicted_probability[2]
            n = predicted_probability[1]
            c = predicted_probability[0]
            e1 = predicted_probability_conv[2]
            n1 = predicted_probability_conv[1]
            c1 = predicted_probability_conv[0]
        else:
            e = predicted_probability[0]
            n = predicted_probability[1]
            c = predicted_probability[2]
            e1 = predicted_probability_conv[0]
            n1 = predicted_probability_conv[1]
            c1 = predicted_probability_conv[2]
        
        # e = 0
        # n = 0
        # c = 0
        
        # if predicted_probability[0] >= 0.1 or predicted_probability_conv[0] >= 0.1:
        #     if predicted_probability[2] >= 0.1 or predicted_probability_conv[2] >= 0.1:
        #         if predicted_probability[2] >= predicted_probability_conv[2]:
        #             e = predicted_probability[0]
        #             n = predicted_probability[1]
        #             c = predicted_probability[2]
        #         else:
        #             e = predicted_probability_conv[0]
        #             n = predicted_probability_conv[1]
        #             c = predicted_probability_conv[2]
        #     else:    
        #         if predicted_probability[0] < predicted_probability_conv[0]:
        #             e = predicted_probability[0]
        #             n = predicted_probability[1]
        #             c = predicted_probability[2]
        #         else:
        #             e = predicted_probability_conv[0]
        #             n = predicted_probability_conv[1]
        #             c = predicted_probability_conv[2]
        # else:
        #     if predicted_probability[2] >= predicted_probability_conv[2]:
        #         e = predicted_probability[0]
        #         n = predicted_probability[1]
        #         c = predicted_probability[2]
        #     else:
        #         e = predicted_probability_conv[0]
        #         n = predicted_probability_conv[1]
        #         c = predicted_probability_conv[2]
                
        res.append(([e,n,c], [e1,n1,c1]))
        
    return res
        
        

def build_list(filename):
    datalist = []
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            i = l[0].strip()
            r = l[1].strip()
            hyp1 = l[4].strip()
            hyp2 = l[5].strip()
            datalist.append((i, r, hyp1, hyp2))
        return datalist


def result_print(test, pathh1, path2):
    h1 = []
    h2 = []
    r = []
    for tuple in test:
        if len(r) > 199:
            break
        i = tuple[0].strip()
        
        r.append(tuple[1].strip())
        
        h1.append(tuple[2].strip())
        h2.append(tuple[3].strip())
    print(len(r))
    score1 = nli_score(r, h1)
    score2 = nli_score(r, h2)
        
        
    
    with open(pathh1, 'w', encoding='utf-8') as f:
        for i, s in enumerate(score1):
            f.write(str(i))
            f.write('\t')
            f.write(str(s[0][0]))
            f.write('\t')
            f.write(str(s[0][1]))
            f.write('\t')
            f.write(str(s[0][2]))
            f.write('\t')
            f.write(str(s[1][0]))
            f.write('\t')
            f.write(str(s[1][1]))
            f.write('\t')
            f.write(str(s[1][2]))
            f.write('\n')
    
    with open(path2, 'w', encoding='utf-8') as f:
        for i, s in enumerate(score2):
            f.write(str(i))
            f.write('\t')
            f.write(str(s[0][0]))
            f.write('\t')
            f.write(str(s[0][1]))
            f.write('\t')
            f.write(str(s[0][2]))
            f.write('\t')
            f.write(str(s[1][0]))
            f.write('\t')
            f.write(str(s[1][1]))
            f.write('\t')
            f.write(str(s[1][2]))
            f.write('\n')
    
    
        
        
if __name__ == '__main__':
    #result_print(build_list('output1/name.txt'),'output1/result1/nameh1r.txt','output1/result1/namer.txt')
    #result_print(build_list('output1/num.txt'),'output1/result1/numh1r.txt','output1/result1/numr.txt')
    #result_print(build_list('output1/word.txt'),'output1/result1/nnh1r.txt','output1/result1/nnr.txt')
    #result_print(build_list('output1/neg.txt'),'output1/result1/negr.txt','output1/result1/negh1r.txt')
    #result_print(build_list('output1/pron.txt'),'output1/result1/pronh1r.txt','output1/result1/pronr.txt')
    #result_print(build_list('add/newaddnon.txt'),'output1/result1/add1h1r.txt','output1/result1/add1r.txt')
    #result_print(build_list('output1/ad.txt'),'output1/result1/addh1r.txt','output1/result1/dropr.txt')
    result_print(build_list('output1/word.txt'),'output1/result2/vbr.txt','output1/result2/jjr.txt')