from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-de")

model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-de")

tokenizer_b = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")

model_b = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")

ref = []
with open('news-commentary-v15.de-en.tsv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        sen = l.split('\t')
        s = sen[0].strip()
        r = sen[1].strip()
        ref.append((i, s, r))

hyp = []
for p in ref:
    i = p[0]
    s = p[1]
    r = p[2]
    batch_b = tokenizer_b([s], return_tensors="pt")
    generated_ids_b = model_b.generate(**batch_b)
    d_r = tokenizer_b.batch_decode(generated_ids_b, skip_special_tokens=True)[0]
    hyp.append((i, s, r, d_r))
    print(len(hyp))
    if len(hyp) == 2000:
        break

with open('desr.txt', 'w', encoding='utf-8') as f:
    for h in hyp:
        f.write(str(h[0]))
        f.write('\t')
        f.write(str(h[1]))
        f.write('\t')
        f.write(str(h[2]))
        f.write('\t')
        f.write(str(h[3]))
        f.write('\n')
