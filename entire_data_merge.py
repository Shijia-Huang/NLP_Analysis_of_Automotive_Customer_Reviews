import pandas as pd
import numpy as np

# The file generated from entire_data_identifying
sample1 = pd.read_csv('entire_data_mentioned_regular.csv', header=0, usecols = ['detected_entity','year','model_id','brand_id','yb_id','ybm_id','org_id'] )

# Below are the files generated from entire_data_identifying_irregular. I have three files here because I split the
# code into three parts and deal with one irregular type at a time. To reproduce the result, you could run the
# entire_data_identifying_irregular code at once and write the result to a single file "entire_data_mentioned_irregular.csv"
sample2 = pd.read_csv('entire_data_mentioned_irregular_SPACE.csv', header=0, usecols = ['detected_entity','year','model_id','brand_id','yb_id','ybm_id','org_id']  )
sample3 = pd.read_csv('entire_data_mentioned_irregular_SLASH.csv', header=0, usecols = ['detected_entity','year','model_id','brand_id','yb_id','ybm_id','org_id']  )
sample4 = pd.read_csv('entire_data_mentioned_irregular_DASH.csv', header=0, usecols = ['detected_entity','year','model_id','brand_id','yb_id','ybm_id','org_id']  )

print(len(sample1))
print(len(sample2))
print(len(sample3))
print(len(sample4))

identified = sample1.append(sample2)
identified = identified.append(sample3)
identified = identified.append(sample4)


# replace 'NA' with 0 so that we can sort values with 0 being the smallest.
identified_2 = identified.replace(np.nan,0)
identified_2 = identified_2.drop_duplicates(subset = ['org_id','year','model_id','brand_id'])
identified_2 = identified_2.sort_values(by = ['org_id','year','model_id','brand_id'])
print("after merge: identified_2 has", len(identified_2), "lines")

# Below are for mentioned car brands/models
identified_3 = identified_2.drop_duplicates(subset=['org_id', 'brand_id', 'model_id'], keep='last')
identified_3 = identified_3.drop_duplicates(subset=['org_id', 'brand_id', 'year'], keep='last')

# Below are for identified car brands/models without duplicates
# identified_3 = identified_2.drop_duplicates(subset=['brand_id', 'model_id','year'], keep='last')
# identified_3 = identified_3.drop_duplicates(subset=['brand_id', 'model_id'], keep='last')
# identified_3 = identified_3.drop_duplicates(subset=['brand_id', 'year'], keep='last')

print("after drop duplicates of (brand, model) and (brand, year): identified3 has ", len(identified_3), 'lines')


identified_3 = identified_3.sort_values(by = ['org_id','detected_entity','year','model_id','brand_id','yb_id','ybm_id'])
identified_3 = identified_3.reset_index()
del (identified_3['index'])
identified_3 = identified_3[['detected_entity', 'year','model_id','brand_id','yb_id','ybm_id', 'org_id']]

# convert 0 back to 'NA'
identified_3['year'] = identified_3['year'].astype(int)
identified_3['model_id'] = identified_3['model_id'].astype(int)
identified_3['brand_id'] = identified_3['brand_id'].astype(int)
identified_3['yb_id'] = identified_3['yb_id'].astype(int)
identified_3['ybm_id'] = identified_3['ybm_id'].astype(int)
identified_3 = identified_3.replace(0,'')

identified_3.to_csv("entire_data_IDENTIFIed.csv")

print("In total there are ", len(identified_3), "distinct brand/models mentioned in the entire dataset.")

