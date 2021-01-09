import nltk
import pandas as pd
import numpy as np
import re

sample = pd.read_csv('full_data_tagged...csv', header=0)
sample['Entities'] = sample['Entities'].replace(np.nan, '')
print('file length:', len(sample))

def convert(string):
    string = re.sub(", ", " ", string)
    if len(string) != 0:
        li = string.split(" ")
    else:
        li = []
    return li


# convert 'Entities' from a string to a list containing entities as elements.
sample['Entities'] = sample['Entities'].apply(lambda x: convert(x))

detected_list = sample[sample['Entities'].astype(bool)][['org_id', 'sent_idx', 'sent_text', 'Entities']]
detected_list = detected_list.reset_index()
del (detected_list['index'])

print('detected list length:',len(detected_list))

url = "https://www.dropbox.com/s/sxf35ebm71n3ho7/car%20model%20identifier.csv?dl=1"
match = pd.read_csv(url)
match.head()

# unique model names:
match_unique_models = []
match_models = match['model_fromsales']
[match_unique_models.append(x) for x in match_models if x not in match_unique_models]

length = len(detected_list)
detected_entities = []
brand_IDs = []
model_IDs = []
year_IDs = []
ybm_IDs = []
yb_IDs = []
org_IDs = []

for i in range(len(detected_list)):
    for entity in detected_list.loc[i, 'Entities']:
        detected = entity.upper()
        texts = detected_list.loc[i, 'sent_text']
        for j in range(len(match)):
            brand = match.loc[j, 'brand']
            model = match.loc[j, 'model_fromsales']
            brand_id = match.loc[j, 'brand_id']
            model_id = match.loc[j, 'model_id']
            year = str(match.loc[j, 'year'])

            if (' ' not in brand) and ('-' not in brand) and (detected == brand):
                brand_ID = brand_id  #
                if (' ' not in model) and ('/' not in model) and ('-' not in model) and model in texts.upper():
                    model_ID = model_id  #
                elif (' ' in model) and (
                        model.split(' ', 1)[0] in texts.upper() or model.split(' ', 1)[1] in texts.upper()):
                    model_ID = model_id
                elif ('/' in model) and (
                        model.split('/', 1)[0] in texts.upper() or model.split('/', 1)[1] in texts.upper()):
                    model_ID = model_id
                elif ('-' in model) and (
                        model.split('-', 1)[0] in texts.upper() or model.split('-', 1)[1] in texts.upper()):
                    model_ID = model_id
                else:
                    model_ID = ""

                if year in texts:
                    year_ID = year
                    yb_ID = match.loc[j, 'yb_id']
                else:
                    year_ID = ""
                    yb_ID = ""
                if (model_ID == model_id and year_ID == year):
                    ybm_ID = match.loc[j, 'ybm_id']
                else:
                    ybm_ID = ""

                org_IDs.append(detected_list.loc[i, 'org_id'])
                detected_entities.append(detected)
                brand_IDs.append(brand_ID)
                model_IDs.append(model_ID)
                year_IDs.append(year_ID)
                yb_IDs.append(yb_ID)
                ybm_IDs.append(ybm_ID)


            # ____________Check irregular brand names_____________
            # since there are two irregular brand names: Land Rover and Mercedece-Benz,
            # we can identify them by checking if there is a space or a "-" in a brand name here

            elif (' ' in brand) and ((detected == brand.split(' ', 1)[0]) or (detected == brand.split(' ', 1)[1]) or (
                    detected == brand.replace(' ', '-'))):
                brand_ID = brand_id
                if ' ' not in model and model in texts.upper():
                    model_ID = model_id
                elif (' ' in model) and (
                        model.split(' ', 1)[0] in texts.upper() or model.split(' ', 1)[1] in texts.upper()):
                    model_ID = model_id
                else:
                    model_ID = ""

                if year in texts:
                    year_ID = year
                    yb_ID = match.loc[j, 'yb_id']
                else:
                    year_ID = ""
                    yb_ID = ""
                if (model_ID == model_id and year_ID == year):
                    ybm_ID = match.loc[j, 'ybm_id']
                else:
                    ybm_ID = ""

                org_IDs.append(detected_list.loc[i, 'org_id'])
                detected_entities.append(detected)
                brand_IDs.append(brand_ID)
                model_IDs.append(model_ID)
                year_IDs.append(year_ID)
                yb_IDs.append(yb_ID)
                ybm_IDs.append(ybm_ID)

            elif ('-' in brand) and ((detected == brand.split('-', 1)[0]) or (detected == brand.split('-', 1)[1]) or (
                    detected == brand.replace('-', ' '))):
                brand_ID = brand_id
                if ' ' not in model and model in texts.upper():
                    model_ID = model_id
                elif (' ' in model) and (
                        (model.split(' ', 1)[0] in texts.upper()) or (model.split(' ', 1)[1] in texts.upper())):
                    model_ID = model_id
                else:
                    model_ID = ""

                if year in texts:
                    year_ID = year
                    yb_ID = match.loc[j, 'yb_id']
                else:
                    year_ID = ""
                    yb_ID = ""
                if (model_ID == model_id and year_ID == year):
                    ybm_ID = match.loc[j, 'ybm_id']
                else:
                    ybm_ID = ""

                org_IDs.append(detected_list.loc[i, 'org_id'])
                detected_entities.append(detected)
                brand_IDs.append(brand_ID)
                model_IDs.append(model_ID)
                year_IDs.append(year_ID)
                yb_IDs.append(yb_ID)
                ybm_IDs.append(ybm_ID)

                # ____________Check irregular brand names finished_____________
            elif (detected == model):
                model_ID = model_id
                # only record this detection if the model name is unique 
                if model in match_unique_models:
                    brand_ID = brand_id
                    if year in texts:
                        year_ID = year
                    else:
                        year_ID = ''
                    if (brand_ID == brand_ID and model_ID == model_id and year_ID == year):
                        ybm_ID = match.loc[j, 'ybm_id']
                    else:
                        ybm_ID = ''
                    if (brand_ID == brand_id and year_ID == year):
                        yb_ID = match.loc[j, 'yb_id']
                    else:
                        yb_ID = ''

                    org_IDs.append(detected_list.loc[i, 'org_id'])
                    detected_entities.append(detected)
                    brand_IDs.append(brand_ID)
                    model_IDs.append(model_ID)
                    year_IDs.append(year_ID)
                    ybm_IDs.append(ybm_ID)
                    yb_IDs.append(yb_ID)

identified = pd.DataFrame({'detected_entity': detected_entities,
                           'year': year_IDs,
                           'model_id': model_IDs,
                           'brand_id': brand_IDs,
                           'yb_id': yb_IDs,
                           'ybm_id': ybm_IDs,
                           'org_id': org_IDs})
print(len(identified))

identified_2 = identified.sort_values(by=['brand_id', 'model_id', 'year', 'yb_id', 'ybm_id', 'org_id'])
identified_3 = identified_2.drop_duplicates(subset=['org_id', 'brand_id', 'model_id', 'year'], keep='last')

identified_3 = identified_3.reset_index()
del (identified_3['index'])
identified_3 = identified_3[['detected_entity', 'year', 'model_id', 'brand_id', 'yb_id', 'ybm_id', 'org_id']]
identified_3.to_csv("entire_data_Mentioned.csv")

print("identified ", len(identified_3), "brand/models already")
