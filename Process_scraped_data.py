#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Imports
import pandas as pd
from langdetect import detect_langs
from googletrans import Translator


# In[ ]:


# Function that processes scraped data

def process_scraped_data(df):
    
    """
    Processes and cleans the scraped data in a pandas DataFrame.
    """
    
    df["rating"] = df["rating"].apply(lambda x: int(x.split(".")[0]))

    # extracting the date from the scraped date info and converting it into a datetime object

    df["date"] = df["date"].apply(lambda x: x.split("on")[-1])
    df["date"] = pd.to_datetime(df["date"])
    
    return df


# In[ ]:


# translating non-english reviews to english

def translation(df):
    """
    Translate non-English text reviews in a DataFrame to English using Google Translate.

    This function iterates through a DataFrame containing text reviews, detects the language of each review,
    and translates non-English reviews to English. The translated text replaces the original text in the DataFrame.

    Args:
    - df (DataFrame): A pandas DataFrame containing reviews to be translated. It should have a column named "body" containing text reviews.

    Returns:
    - DataFrame: The modified DataFrame with non-English reviews translated to English. The original "body" column is updated with the translations.

    Prints:
    - A message indicating if a review is empty or too short to process.
    - A message indicating any errors encountered during language detection or translation for specific reviews.

    Notes:
    - Reviews with fewer than 5 characters are considered too short and are not processed for language detection or translation.
    - Handles exceptions during language detection and translation by printing error messages and continuing with the next review.

    """
    translator = Translator()
    for i in range(len(df)):
        review = df.loc[i, "body"]
        if not review or len(review) < 5:  
            print(f"Review at index {i} is empty or too short.")
        
        try:
            lang = str(detect_langs(review)).split(':')[0][1:]
        except Exception as e:
            print(f"Error detecting language for review at index {i}: {e}")
        
        if lang != "en":
            try:
                translation = translator.translate(review, src=lang, dest="en").text
                df.loc[i, "body"] = translation
            except Exception as e:
                print(f"Error translating review at index {i}: {e}")
                
    return df
    

