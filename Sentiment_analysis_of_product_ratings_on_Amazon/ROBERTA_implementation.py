#!/usr/bin/env python
# coding: utf-8

# In[9]:


import warnings
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax
import pandas as pd


# In[10]:


def Roberta_initialize():
    # ROBERTA PRETRAINED MODEL (takes context into account)

    # surpressing specific FutureWarning from huggingface_hub
    warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub")

    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"

    # load tokenizer and model (sometimes crashed kernel so had to include try, except)
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)

        # check if GPU is available and use it, otherwise use CPU
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        print(f"Model and tokenizer loaded successfully on {device}!")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None
        
    return tokenizer, model, device


# In[11]:


def Roberta_analyze(df, tokenizer, model):

    # predicting the sentiment for each review of the dataset
    robertamodel = {}
    position = 0
    for review in df["body"]:
        try:
            encoded = tokenizer(review, return_tensors="pt")
            modelled = model(**encoded)
            roberta = modelled[0][0].detach().numpy()
            roberta = softmax(roberta)
            robertamodel[position] = {
                "Rnegative": roberta[0],
                "Rneutral": roberta[1],
                "Rpositive": roberta[2]
            }
            position += 1
        except RuntimeError:
            print(f"can't process the text in index {position}")
            position += 1

    # concatenating all dataframes together
    df_r = pd.DataFrame(robertamodel).T
    return df_r
    

