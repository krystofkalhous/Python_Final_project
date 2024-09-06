#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# displaying the reviews which are evaluated as best/worst by both models

def text(model, df_sentiment):
    """
    Prints the best and worst reviews according to the positive sentiment scores of a given model, 
    and optionally the review with the highest overall sentiment for the VADER model.

    Parameters:
    model (str): The prefix of the column names in the DataFrame `df_sentiment` that contains 
                 sentiment scores. For example, if `model` is "model1", the DataFrame should 
                 contain a column named "model1positive".

    Returns:
    None: The function prints the best and worst reviews based on the highest and lowest positive 
          sentiment scores. If the model is "V", it additionally prints the review with the highest 
          overall sentiment based on the "Vcompound" column.
    """
    best = df_sentiment.loc[df_sentiment[f'{model}positive'].idxmax(), "body"]
    worst = df_sentiment.loc[df_sentiment[f'{model}positive'].idxmin(), "body"]
    print(f"The best review according to model {model}: \n {best} \n")
    print(f"The worst review according to model {model}: \n {worst} \n")

    if model == "V":
        highestsentiment = df_sentiment.loc[df_sentiment["Vcompound"].idxmax(), "body"]
        print(f"The review with the highest sentiment according to VADER model: \n {highestsentiment} \n")
        

