<h1 align="center">Market_Analysis_On_Customer_Reviews</h1>




## About 

The purpose of this project is to analyze how consumers perceive the quality of complex products for which they lack the expertise to accurately access. This stream of work sits at the intersection between operations management and marketing. The research will use aggregate customer review measures as a proxy for product quality to investigate how relative perceived quality amongst similar products influences market shares in a competitive market.
By understanding how consumers evaluate quality of complex, technology products, firms can design products that better communicate the benefits of a new technology and allocate their resources accordingly.

## Design
The code is to read through the dataset of car customer reviews, and filter out information such as possible car brand names, model names, and production year. We match the mentioned car models with a set of car brands/models, in order to generate a dataset of all the mentioned car brand names, model names, and year of production in the reviews. 

The dataset we can be downloaded from https://www.dropbox.com/s/gb3i3deyb7swvvx/df_test_conf_lv.csv?dl=1, each line contains the information of one review sentence. 

The code first use the python NLP package [stanza](https://stanfordnlp.github.io/stanza/) to perform a Named Entity Recognition on the entire dataset, and generate a list of detected possible car brand/model names for each review sentence.

We compare the detected possible car brand/model names with the car brand/model names in a reference set of car information. 

![results](images/reference_car_models.png)

Then we create a dataframe containing all the detected entities that can be matched with car brand/models in the reference set, which is all the mentioned car brand/models in the each review text. 


### Procedures

1. Load the dataframe of all review texts, and create an empty column named "Entities" for detected possible car brand/model names in later steps using [data_cleaning.py](https://github.com/ScarlettHuang1/Analysis_On_Customer_Reviews-/blob/main/data_cleaning.py), and save the new dataframe as "[entire_dataset_cleaned.csv](https://1drv.ms/u/s!AoWQe4vzVrOkgRnz6Ly9M6STheYh?e=U0M0Jt)".


2. Load the entire_data_cleaned file. Use the NLP package [stanza](https://stanfordnlp.github.io/stanza/) to read the reviews line by line and detect entities that are possibly car brand or model names using [data_tagging.py](https://github.com/ScarlettHuang1/Analysis_On_Customer_Reviews-/blob/main/data_tagging.py). Put the detected entities in each review sentence to the column "Entities" that we created in step 1. Because the dataset has more than 760,000 reivew sentences, we write back to the datafram every 400 lines to save the changes incase the task times out and ends before we process all the sentences. If the task times out before all sentences are tagged, we read the latest dataframe and the code restart process the reviews from the first sentence that has not been processed. Save the tagged data to "[entire_dataset_tagged.csv](https://1drv.ms/u/s!AoWQe4vzVrOkgQ91Ip0Egrjn_bmb?e=4BISrC)".

![results](images/tagged.png)

3. Based on the reference car information, check if each detected entity can be matched to any car brand/model names using [data_identifying_regular](https://github.com/ScarlettHuang1/Analysis_On_Customer_Reviews-/blob/main/data_identifying_regular.py) (for regular model names) and [data_identifying_irregular](https://github.com/ScarlettHuang1/Analysis_On_Customer_Reviews-/blob/main/data_identifying_irregular.py) (for irregular model names containing space, slash, or dash). If it could be matched, read the sentence that contains the entity, and check if there are more information in the sentence, such as the model names, or year of production. Merge the identified regular and irregular car brand/model names using [data_merging](https://github.com/ScarlettHuang1/Analysis_On_Customer_Reviews-/blob/main/data_merging.py), and save the information to a new datafram named "[entire_dataset_mentioned](https://1drv.ms/x/s!AoWQe4vzVrOkgRJVUHgfRaF6fCl5?e=QGqoez)".

![results](images/mentioned.png)


### Required Packages and Resources

The dataframe containing reviews and information: https://www.dropbox.com/s/gb3i3deyb7swvvx/df_test_conf_lv.csv?dl=1

Packages used: nltk, pandas, numpy, re, and [stanza](https://stanfordnlp.github.io/stanza/)  - We use the package with [4 named entity types](https://stanfordnlp.github.io/stanza/available_models.html) (language code = en, package = conll03), and supported types include PER (Person), LOC (Location), ORG (Organization) and MISC (Miscellaneous).

![results](images/4_class.png)

  
The results were generated with the help of [Vanderbilt ACCRE Cluster Virtual Machine](https://www.vanderbilt.edu/accre/documentation/python/#installing-additional-packages-with-virtual-environments). 

## Conclusion
Now we could use the result dataset to exam how many times a specific car model is mentioned. We will also determine how frequently two models are mentioned together. The lift between two brands/models may indicate their similarity or association as perceived by consumers.
