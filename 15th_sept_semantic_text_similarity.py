# -*- coding: utf-8 -*-
"""15th Sept Semantic_text_Similarity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bR3DR5DJnq9WrxEVFlZ-6gHyfJBS2ppv
"""

with open('requirements.txt', 'w') as writefile:
    writefile.write("datasets")
    writefile.write("sentence_transformers")
    writefile.write("pandas")
    writefile.write("numpy")
    writefile.write("tqdm")
    writefile.write("sklearn")
    writefile.write("pickle")
    writefile.write("streamlit")
    writefile.write("pyngrok")

"""# Installations

# Libraries
"""

#loading training set
import pandas as pd
import numpy as np
from tqdm import tqdm
tqdm.pandas()
from datasets import load_dataset


# Load the English STSB dataset
stsb_dataset = load_dataset('stsb_multi_mt', 'en')
stsb_train = pd.DataFrame(stsb_dataset['train'])
stsb_test = pd.DataFrame(stsb_dataset['test'])

# Check loaded data
print(stsb_train.shape, stsb_test.shape)
stsb_test.head()

"""## Creating helper functions
* The first function is to pre-process texts by lemmatizing, lowercasing, and removing numbers and stop words.
* The second function takes in two columns of text embeddings and returns the row-wise cosine similarity between the two columns.
"""

from sklearn.metrics.pairwise import cosine_similarity
import spacy
nlp = spacy.load("en_core_web_sm")

def text_processing(sentence):
    """
    Lemmatize, lowercase, remove numbers and stop words
    
    Args:
      sentence: The sentence we want to process.
    
    Returns:
      A list of processed words
    """
    sentence = [token.lemma_.lower()
                for token in nlp(sentence) 
                if token.is_alpha and not token.is_stop]
    
    return sentence


def cos_sim(sentence1_emb, sentence2_emb):
    """
    Cosine similarity between two columns of sentence embeddings
    
    Args:
      sentence1_emb: sentence1 embedding column
      sentence2_emb: sentence2 embedding column
    
    Returns:
      The row-wise cosine similarity between the two columns.
      For instance is sentence1_emb=[a,b,c] and sentence2_emb=[x,y,z]
      Then the result is [cosine_similarity(a,x), cosine_similarity(b,y), cosine_similarity(c,z)]
    """
    cos_sim = cosine_similarity(sentence1_emb, sentence2_emb)
    return np.diag(cos_sim)

"""# Data Setup"""

data = (pd.read_csv("/content/SBERT_data.csv")).drop(['Unnamed: 0'], axis = 1)

prompt = input("Enter prompt: ")
data['prompt']= prompt
data.rename(columns = {'target_text':'sentence2', 'prompt':'sentence1'}, inplace = True)
data['sentence2'] = data['sentence2'].astype('str')
data['sentence1']  = data['sentence1'].astype('str')

data.head()

"""# Loop"""

from sentence_transformers import CrossEncoder
XpathFinder = CrossEncoder("cross-encoder/stsb-roberta-base")
sentence_pairs = []
for sentence1, sentence2 in zip(data['sentence1'],data['sentence2']):
  sentence_pairs.append([sentence1, sentence2])

data['SBERT CrossEncoder_Score'] = XpathFinder.predict(sentence_pairs, show_progress_bar = True)

#@title Sort 
data.sort_values(by=['SBERT CrossEncoder_Score'], ascending=False)

"""### Download"""

import pickle

filename = 'XpathFinder1.sav'
pickle.dump(XpathFinder, open(filename, 'wb'))

"""# App"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import io
# import netrc
# import pickle
# import sys
# import pandas as pd
# import numpy as np
# import streamlit as st
# # let's import sentence transformer
# import sentence_transformers
# import torch
# #######################################
# 
# st.markdown(
#     f"""
# <style>
#     .reportview-container .main .block-container{{
#         max-width: 90%;
#         padding-top: 5rem;
#         padding-right: 5rem;
#         padding-left: 5rem;
#         padding-bottom: 5rem;
#     }}
#     img{{
#     	max-width:40%;
#     	margin-bottom:40px;
#     }}
# </style>
# """,
#     unsafe_allow_html=True,
# )
# 
# # # let's load the saved model
# loaded_model = pickle.load(open('XpathFinder1.sav', 'rb'))
# #loaded_model = pickle.load('XpathFinder1.sav', map_location='cpu')
# 
# 
# #class CPU_Unpickler(pickle.Unpickler):
# #    def find_class(self, module, name):
# #        if module == 'torch.storage' and name == '_load_from_bytes':
# #            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
# #        else:
# #            return super().find_class(module, name)
# #
# 
# #loaded_model = CPU_Unpickler(open('XpathFinder1.sav', 'rb')).load()
# 
# 
# # Containers
# header_container = st.container()
# mod_container = st.container()
# 
# # Header
# with header_container:
# 
#     # different levels of text you can include in your app
#     st.title("Xpath Finder App")
# 
# 
# # model container
# with mod_container:
#     # collecting input from user
#     prompt = st.text_input("Enter your description below ...")
# 
#     # Loading e data
#     data = (pd.read_csv("/content/SBERT_data.csv")).drop(['Unnamed: 0'], axis = 1)
# 
#     data['prompt']= prompt
#     data.rename(columns = {'target_text':'sentence2', 'prompt':'sentence1'}, inplace = True)
#     data['sentence2'] = data['sentence2'].astype('str')
#     data['sentence1']  = data['sentence1'].astype('str')
# 
#     # let's pass the input to the loaded_model with torch compiled with cuda
#     if prompt:
#         # let's get the result
#         simscore = XpathFinder.predict([prompt])
#         from sentence_transformers import CrossEncoder
#         XpathFinder = CrossEncoder("cross-encoder/stsb-roberta-base")
#         sentence_pairs = []
#         for sentence1, sentence2 in zip(data['sentence1'],data['sentence2']):
#           sentence_pairs.append([sentence1, sentence2])
#         
#         # sorting the df to get highest scoring xpath_container
#         data['SBERT CrossEncoder_Score'] = XpathFinder.predict(sentence_pairs)
#         most_acc = data.head(5)
#         # predictions
#         st.write("Highest Similarity score: ", simscore)
#         st.text("Is this one of these the Xpath you're looking for?")
#         st.write(st.write(most_acc["input_text"])) 
#

# from pyngrok import ngrok

# ngrok.set_auth_token("29Mzs7BHkeeRGNZM41x0Rn4Xilq_7TYKeCLdR34nSS2qBCTzo")

# !nohup streamlit run app.py --server.port 80 &
# url = ngrok.connect(port = '80')
# print(url)
