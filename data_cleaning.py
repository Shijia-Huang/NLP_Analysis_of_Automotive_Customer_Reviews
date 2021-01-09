import pandas as pd
import numpy as np 
import stanza


url="https://www.dropbox.com/s/gb3i3deyb7swvvx/df_test_conf_lv.csv?dl=1"
sample = pd.read_csv(url)

sample['sent_text'] = sample['sent_text'].apply(lambda x: str(x))
sample['Entities'] = 'NoValue'

sample.to_csv("entire_data_cleaned.csv")

