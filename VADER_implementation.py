#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


# In[13]:


# Download the VADER lexicon
nltk.download('vader_lexicon')


# In[14]:


# VADER model

def Vader_analyze_df(df):

    sia = SentimentIntensityAnalyzer()

    # predicting the sentiment for each review of the dataset
    vader = {}
    position = 0
    for review in df["body"]:
        vader[position] = {
            "Vnegative": sia.polarity_scores(review)["neg"],
            "Vneutral": sia.polarity_scores(review)["neu"],
            "Vpositive": sia.polarity_scores(review)["pos"],
            "Vcompound": sia.polarity_scores(review)["compound"]
        }
        position += 1

    # putting the results into an initial dataframe
    df_v = pd.DataFrame(vader).T
    df_v = pd.concat([df, df_v], axis = 1)
    return df_v

