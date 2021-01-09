import pandas as pd
import numpy as np
import stanza

sample = pd.read_csv('full_data_cleaned_NoValue.csv')
print('import file ...... done')
nlp = stanza.Pipeline('en', processors={'ner': 'conll03'})

length = len(sample)
j = sample.Entities.eq('NoValue').idxmax()
print('processed ', j - 1, " lines, now starting from ", j, "th line")

count_Entities = 0
while j < length - 400:
    for i, sentence in enumerate(sample['sent_text'][j:j + 400]):
        sample['Entities'][i + j] = ''
        doc = nlp(sentence)
        for X in doc.entities:
            if X.type != 'O':
                count_Entities += 1
                sample['Entities'][i + j] += (X.text + ", ")
    sample.to_csv("full_data_tagged_inprogress.csv")
    j += 400

if j >= length - 400:
    for i, sentence in enumerate(sample['sent_text'][j:length]):
        sample['Entities'][i + j] = ''
        doc = nlp(sentence)
        for X in doc.entities:
            if X.type != 'O':
                count_Entities += 1
                sample['Entities'][i + j] += (X.text + ", ")
sample.to_csv("entire_data_tagged.csv")

print("counted Entities:", count_Entities)
