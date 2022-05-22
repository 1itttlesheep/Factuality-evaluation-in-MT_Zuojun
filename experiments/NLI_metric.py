from transformers import AutoTokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def nli_score(premises, hypothesiss, model):
    max_length = 256
    if model == 1:
        hg_model_hub_name = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    elif model == 2:
        hg_model_hub_name = 'microsoft/deberta-large-mnli'
    else:
        print("model number error")

    tokenizer = AutoTokenizer.from_pretrained(hg_model_hub_name)
    model = AutoModelForSequenceClassification.from_pretrained(hg_model_hub_name)
    
    res = []
    for premise, hypothesis in zip(premises, hypothesiss):
        
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
        
        
        res.append(([e,n,c], [e1,n1,c1]))
        
    return res
        
        

def NLI_score_write(phenomenon, model, dataset):
    datalist = []
    with open('../checklist_generate/adversarial test/wmt/'+ phenomenon +'.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            i = l[0].strip()
            if dataset == 'paws1' or dataset == 'paws2':
                if phenomenon == 'drop':
                    r = l[1].strip()
                    hyp1 = l[2].strip()
                    hyp2 = l[4].strip()
                elif phenomenon == 'vb':
                    r = l[1].strip()
                    hyp1 = l[2].strip()
                    hyp2 = l[4].strip()
                elif phenomenon == 'jj':
                    r = l[1].strip()
                    hyp1 = l[2].strip()
                    hyp2 = l[5].strip()
                else:
                    r = l[1].strip()
                    hyp1 = l[2].strip()
                    hyp2 = l[3].strip()
            elif dataset == 'wmt':
                if phenomenon == 'drop':
                    r = l[3].strip()
                    hyp1 = l[4].strip()
                    hyp2 = l[6].strip()
                elif phenomenon == 'vb':
                    r = l[3].strip()
                    hyp1 = l[4].strip()
                    hyp2 = l[6].strip()
                elif phenomenon == 'jj':
                    r = l[3].strip()
                    hyp1 = l[4].strip()
                    hyp2 = l[7].strip()
                else:
                    r = l[3].strip()
                    hyp1 = l[4].strip()
                    hyp2 = l[5].strip()
            
            datalist.append((i, r, hyp1, hyp2))
    
    result_print(datalist, phenomenon, model, dataset)
    
    


def result_print(test_data, phenomenon, model, dataset):

    h1 = []
    h2 = []
    r = []
    for tuple in test_data:
        if len(r) > 199:
            break
        i = tuple[0].strip()
        r.append(tuple[1].strip())
        h1.append(tuple[2].strip())
        h2.append(tuple[3].strip())
        
    
    score1 = nli_score(r, h1, model)
    score2 = nli_score(r, h2, model)
    
    with open('nli_result/NLI'+ str(model) + '/' + dataset + '/' + phenomenon + 'h1r.txt', 'w', encoding='utf-8') as f:
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
    
    with open('nli_result/NLI'+ str(model) + '/' + dataset + '/' + phenomenon + 'r.txt', 'w', encoding='utf-8') as f:
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
    
    
    # model = 1 or 2, dataset = 'wmt' or 'paws1' or 'paws2'
    # phenomenon = 'add', 'drop', 'neg', 'nn', 'vb', 'jj', 'num', 'pron', 'name'
    NLI_score_write(phenomenon = 'drop', model = 1, dataset = 'wmt')
    NLI_score_write(phenomenon = 'vb', model = 1, dataset = 'paws1')
    NLI_score_write(phenomenon = 'jj', model = 1, dataset = 'paws2')