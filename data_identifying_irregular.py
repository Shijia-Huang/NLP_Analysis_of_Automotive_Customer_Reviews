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

length = len(detected_list)
print('detected list length:', length)

url = "https://www.dropbox.com/s/sxf35ebm71n3ho7/car%20model%20identifier.csv?dl=1"
match = pd.read_csv(url)
match.head()

# unique model names:
match_unique_models = []
match_models = match['model_fromsales']
[match_unique_models.append(x) for x in match_models if x not in match_unique_models]

#irregular model names:
match_irregular1 = match.loc[(match['model_fromsales'].str.contains(' '))].reset_index()
match_irregular2 = match.loc[(match['model_fromsales'].str.contains('/'))].reset_index()
match_irregular3 = match.loc[(match['model_fromsales'].str.contains('-'))].reset_index()

#############  SPACE  #############
detected_entities = []
brand = []
model = []
brand_IDs = []
model_IDs = []
year_IDs = []
ybm_IDs = []
yb_IDs = []
org_IDs = []
for i in range(len(detected_list)):
    for entity in detected_list.loc[i, 'Entities']:
        detected = entity.upper()
        texts = detected_list.loc[i, 'sent_text'].upper()
        for j in range(len(match_irregular1)):
            brand = match_irregular1.loc[j, 'brand']
            model = match_irregular1.loc[j, 'model_fromsales']
            brand_id = match_irregular1.loc[j, 'brand_id']
            model_id = match_irregular1.loc[j, 'model_id']
            year = str(match_irregular1.loc[j, 'year'])

            if (' ' in model) and (detected == model.split(' ', 1)[0] or detected == model.split(' ', 1)[1]
                                   or detected == model.replace(' ', '-')
                                   or detected == model.replace(' ','_')
                                   or detected == model.replace(' ', '')):
                model_ID = model_id

                if (' ' not in brand) and ('-' not in brand) and brand in texts:
                    brand_ID = brand_id
                elif (' ' in brand) and ((brand.split(' ', 1)[0] in texts)
                                         or (brand.split(' ', 1)[1] in texts)
                                         or (brand.replace(' ', '-') in texts)):
                    brand_ID = brand_id
                elif ('-' in brand) and ((brand.split('-', 1)[0] in texts)
                                         or (brand.split('-', 1)[1] in texts)
                                         or (brand.replace('-', ' ') in texts)):
                    brand_ID = brand_id
                else:
                    brand_ID = ""

                if brand_ID == brand_id:
                    if year in texts:
                        year_ID = year
                        yb_ID = match_irregular1.loc[j, 'yb_id']
                    else:
                        year_ID = ""
                        yb_ID = ""
                    if model_ID == model_id and brand_ID == brand_id and year_ID == year:
                        ybm_ID = match_irregular1.loc[j, 'ybm_id']
                    else:
                        ybm_ID = ""
                        
                    org_IDs.append(detected_list.loc[i, 'org_id'])
                    detected_entities.append(detected)
                    brand_IDs.append(brand_ID)
                    model_IDs.append(model_ID)
                    year_IDs.append(year_ID)
                    yb_IDs.append(yb_ID)
                    ybm_IDs.append(ybm_ID)

identified1 = pd.DataFrame({'detected_entity': detected_entities,
                            'year': year_IDs,
                            'model_id': model_IDs,
                            'brand_id': brand_IDs,
                            'yb_id': yb_IDs,
                            'ybm_id': ybm_IDs,
                            'org_id': org_IDs})

identified1_2 = identified1.sort_values(by=['brand_id', 'model_id', 'year', 'yb_id', 'ybm_id', 'org_id'])
identified1_3 = identified1_2.drop_duplicates(subset=['org_id', 'brand_id', 'model_id', 'year'], keep='last')

# below are for identification (without duplicates)
# identified1_2.to_csv("full_data_identified_irregular_SPACE_Mention_inprogress.csv")
# identified1_3 = identified1_2.drop_duplicates(subset=['brand_id','model_id','year'], keep='last')

identified1_3 = identified1_3.reset_index()
del (identified1_3['index'])
identified1_3 = identified1_3[['detected_entity', 'year', 'model_id', 'brand_id', 'yb_id', 'ybm_id', 'org_id']]
identified1_3.to_csv("entire_data_irregular_SPACE_Mentioned.csv")

print("identified ", len(identified1_3), "irregular SPACE models already")




#############  DASH  #############
detected_entities = []
brand = []
model = []
brand_IDs = []
model_IDs = []
year_IDs = []
ybm_IDs = []
yb_IDs = []
org_IDs = []
for i in range(len(detected_list)):
    for entity in detected_list.loc[i, 'Entities']:
        detected = entity.upper()
        texts = detected_list.loc[i, 'sent_text'].upper()
        for j in range(len(match_irregular3)):
            brand = match_irregular3.loc[j, 'brand']
            model = match_irregular3.loc[j, 'model_fromsales']
            brand_id = match_irregular3.loc[j, 'brand_id']
            model_id = match_irregular3.loc[j, 'model_id']
            year = str(match_irregular3.loc[j, 'year'])

            if ('-' in model) and (detected == model.split('-', 1)[0] or detected == model.split('-', 1)[1]
                                   or detected == model.replace('-', ' ')
                                   or detected == model.replace('-','_')
                                   or detected == model.replace('_', '')):
                model_ID = model_id

                if (' ' not in brand) and ('-' not in brand) and brand in texts:
                    brand_ID = brand_id
                elif (' ' in brand) and ((brand.split(' ', 1)[0] in texts)
                                         or (brand.split(' ', 1)[1] in texts)
                                         or (brand.replace(' ', '-') in texts)):
                    brand_ID = brand_id
                elif ('-' in brand) and ((brand.split('-', 1)[0] in texts)
                                         or (brand.split('-', 1)[1] in texts)
                                         or (brand.replace('-', ' ') in texts)):
                    brand_ID = brand_id
                else:
                    brand_ID = ""

                if brand_ID == brand_id:
                    if year in texts:
                        year_ID = year
                        yb_ID = match_irregular3.loc[j, 'yb_id']
                    else:
                        year_ID = ""
                        yb_ID = ""
                    if brand_ID == brand_id and model_ID == model_id and year_ID == year:
                        ybm_ID = match_irregular3.loc[j, 'ybm_id']
                    else:
                        ybm_ID = ""

                    org_IDs.append(detected_list.loc[i, 'org_id'])
                    detected_entities.append(detected)
                    brand_IDs.append(brand_ID)
                    model_IDs.append(model_ID)
                    year_IDs.append(year_ID)
                    yb_IDs.append(yb_ID)
                    ybm_IDs.append(ybm_ID)

identified3 = pd.DataFrame({'detected_entity': detected_entities,
                            'year': year_IDs,
                            'model_id': model_IDs,
                            'brand_id': brand_IDs,
                            'yb_id': yb_IDs,
                            'ybm_id': ybm_IDs,
                            'org_id': org_IDs})

identified3_2 = identified3.sort_values(by=['brand_id', 'model_id', 'year', 'yb_id', 'ybm_id', 'org_id'])

identified3_3 = identified3_2.drop_duplicates(subset=['org_id', 'brand_id', 'model_id', 'year'], keep='last')

# below are for identifications
# identified1_2.to_csv("full_data_identified_irregular_SPACE_Mention_inprogress.csv")
# identified1_3 = identified1_2.drop_duplicates(subset=['brand_id','model_id','year'], keep='last')

identified3_3 = identified3_3.reset_index()
del (identified3_3['index'])
identified3_3 = identified3_3[['detected_entity', 'year', 'model_id', 'brand_id', 'yb_id', 'ybm_id', 'org_id']]
identified3_3.to_csv("entire_data_irregular_DASH_Mentioned.csv")

print("identified ", len(identified3_3), "irregular DASH models already")




############# SLASH #############
detected_entities = []
brand = []
model = []
brand_IDs = []
model_IDs = []
year_IDs = []
ybm_IDs = []
yb_IDs = []
org_IDs = []
for i in range(len(detected_list)):
    for entity in detected_list.loc[i, 'Entities']:
        detected = entity.upper()
        texts = detected_list.loc[i, 'sent_text'].upper()
        for j in range(len(match_irregular2)):
            brand = match_irregular2.loc[j, 'brand']
            model = match_irregular2.loc[j, 'model_fromsales']
            brand_id = match_irregular2.loc[j, 'brand_id']
            model_id = match_irregular2.loc[j, 'model_id']
            year = str(match_irregular2.loc[j, 'year'])

            first = model.split('/', 1)[0]
            later = re.split('(\d+)', model)[0] + model.split('/', 1)[1]

            if ('/' in model) and (detected == first or detected == later):
                model_ID = model_id

                if model in match_unique_models:
                    brand_ID = brand_id
                elif (' ' not in brand) and ('-' not in brand) and brand in texts:
                    brand_ID = brand_id
                elif (' ' in brand) and ((brand.split(' ', 1)[0] in texts)
                                         or (brand.split(' ', 1)[1] in texts)
                                         or (brand.replace(' ', '-') in texts)):
                    brand_ID = brand_id
                elif ('-' in brand) and ((brand.split('-', 1)[0] in texts)
                                         or (brand.split('-', 1)[1] in texts)
                                         or (brand.replace('-', ' ') in texts)):
                    brand_ID = brand_id
                else:
                    brand_ID = ""

                if brand_ID == brand_id:
                    if year in texts:
                        year_ID = year
                        yb_ID = match_irregular2.loc[j, 'yb_id'] 
                    else:
                        year_ID = ""
                        yb_ID = ""

                    if model_ID == model_id and brand_ID == brand_id and year_ID == year:
                        ybm_ID = match_irregular2.loc[j, 'ybm_id']
                    else:
                        ybm_ID = ""

                    org_IDs.append(detected_list.loc[i, 'org_id'])
                    detected_entities.append(detected)
                    brand_IDs.append(brand_ID)
                    model_IDs.append(model_ID)
                    year_IDs.append(year_ID)
                    yb_IDs.append(yb_ID)
                    ybm_IDs.append(ybm_ID)

identified2 = pd.DataFrame({'detected_entity': detected_entities,
                            'year': year_IDs,
                            'model_id': model_IDs,
                            'brand_id': brand_IDs,
                            'yb_id': yb_IDs,
                            'ybm_id': ybm_IDs,
                            'org_id': org_IDs})

identified2_2 = identified2.sort_values(by=['brand_id', 'model_id', 'year', 'yb_id', 'ybm_id', 'org_id'])

identified2_3 = identified2_2.drop_duplicates(subset=['org_id', 'brand_id', 'model_id', 'year'], keep='last')

# below are for identifications
# identified1_2.to_csv("full_data_identified_irregular_SPACE_Mention_inprogress.csv")
# identified1_3 = identified1_2.drop_duplicates(subset=['brand_id','model_id','year'], keep='last')

identified2_3 = identified2_3.reset_index()
del (identified2_3['index'])
identified2_3 = identified2_3[['detected_entity', 'year', 'model_id', 'brand_id', 'yb_id', 'ybm_id', 'org_id']]
identified2_3.to_csv("entire_data_irregular_SLASH_Mentioned.csv")

print("identified ", len(identified2_3), "irregular SlASH models already")

