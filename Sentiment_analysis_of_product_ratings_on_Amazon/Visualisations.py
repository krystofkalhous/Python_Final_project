#!/usr/bin/env python
# coding: utf-8

# In[4]:


import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer, re, CountVectorizer
import pandas as pd
import warnings


# In[2]:


# VADER model output visualizations

def plot_VADER_output(df_v, df_sentiment):
    # barplot which shows the average predicted valence (compound score) by VADER model for each "star group"

    plt.figure(figsize = (10,4))
    ax = sns.barplot(df_v, x = "rating", y = "Vcompound")
    ax.set_title("compound score by amazon stars")
    ax.set_xlabel("stars rating")
    ax.set_ylabel("valence score")
    plt.show()

    # plot which shows the average predicted valence by VADER model for each "star group" (I assume this one fits better)

    meandf = df_sentiment.groupby("rating")["Vcompound"].mean().reset_index()
    meandf["rating"] = [str(priemer) for priemer in meandf["rating"]]
    plt.figure(figsize=(10,4))
    plt.stem(meandf['rating'], meandf['Vcompound'])
    plt.title('compound score by amazon stars')
    plt.show()


# In[6]:


# barplot which displays the average predicted (pos/neu/neg) valence by both models for each "star group"

def pnn_plots(model, df_sentiment):
    """
    Generates bar plots for positive, neutral, and negative sentiment scores based on a given model.

    Parameters:
    model (str): The prefix of the column names in the DataFrame `df_sentiment` that contains 
                 sentiment scores. For example, if `model` is "model1", the DataFrame should 
                 contain columns named "model1positive", "model1neutral", and "model1negative".

    Returns:
    None: The function creates and displays a figure with three bar plots. The plots show the 
          sentiment scores (positive, neutral, and negative) against the ratings.
    """
    fig, axs = plt.subplots(1,3, figsize = (15,4))
    sns.barplot(df_sentiment, x = "rating", y = f"{model}positive", ax = axs[0])
    sns.barplot(df_sentiment, x = "rating", y = f"{model}neutral", ax = axs[1])
    sns.barplot(df_sentiment, x = "rating", y = f"{model}negative", ax = axs[2])
    axs[0].set_title("positive")
    axs[1].set_title("neutral")
    axs[2].set_title("negative")
    


# In[5]:


def display_relationships(df_sentiment):

    # displaying the relationship between models' predicted sentiments

    # surpressing the layout warning as the layout of the graph looks alright
    warnings.filterwarnings("ignore", message="The figure layout has changed to tight")

    sns.pairplot(data = df_sentiment, vars= ['Vnegative', 'Vneutral', 'Vpositive'
                                       ,'Rnegative', 'Rneutral', 'Rpositive'],
                    hue = "rating",
                    palette="pastel")
    plt.show()


# In[7]:


def VADER_compound_sentiment_over_t(df_sentiment):

    # VADER compound sentiment shown over time

    plt.figure(figsize = (10,3))
    plt.rc('font', family='Courier', size=8)
    plt.scatter(x = df_sentiment["date"], y = df_sentiment["Vcompound"], color = "orange")
    plt.title("overall sentiment predicted by the VADER model throughout time")


# In[ ]:


def ROBERTA_negative_sentiment_over_t(df_sentiment):
    # roBERTa negative sentiment shown over time

    plt.figure(figsize=(10,3))
    plt.scatter(x = df_sentiment["date"], y = df_sentiment["Rnegative"], color = "red", alpha = 0.4)
    plt.title("negative sentiment predicted by the roberta model throught time")
    


# In[3]:


def word_cloud(df_sentiment):
    # word cloud displaying the most used words in all of the reviews

    reviews = "".join(i for i in df_sentiment["body"])
    cloud = WordCloud(stopwords = ENGLISH_STOP_WORDS, colormap="inferno_r").generate(reviews)
    plt.figure(figsize=(8,4))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    

