#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# importing packages
import requests
from bs4 import BeautifulSoup


# helper function
def get_default_headers():
    
    return {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'accept-language': 'en-US,en;q=0.9'
    }


# function that scrapes proportions of star ratings, number of ratings and title of product from Amazon website
def retrieve_star_ratings_from_Amazon(url, headers=None):

    # Use default headers if none are provided
    if headers is None:
        headers = get_default_headers()

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page with status code: {response.status_code}")
        return None, None, None

    soup = BeautifulSoup(response.text, 'lxml')

    title_element = soup.select_one('#productTitle')
    title = title_element.text.strip() if title_element else None
    if not title:
        print("Failed to find the title element.")
        
    no_of_ratings_element = soup.select_one('#acrCustomerReviewText')
    no_of_ratings = int(no_of_ratings_element.text.replace(' ratings', '').replace(',', '').strip()) if no_of_ratings_element else None
    if not no_of_ratings:
        print("Failed to find the number of ratings element.")

    star_reviews_hist = soup.select_one('#cm_cr_dp_d_rating_histogram')
    if star_reviews_hist:
        a_tags = star_reviews_hist.find_all('a')
        star_reviews_list = [a.get('aria-label') for a in a_tags if a.get('aria-label')]
    else:
        print("Failed to find the rating histogram section.")
        star_reviews_list = None

    return star_reviews_list, no_of_ratings, title

# Output
# star_reviews_list, no_of_ratings, title = retrieve_star_ratings_from_Amazon(url = 'https://www.amazon.co.uk/Fellowship-Ring-Lord-Rings-Book/dp/B098T7Y764/ref=sr_1_1?crid=27UDEHA2GEFQR&dib=eyJ2IjoiMSJ9.WrTkzOAV8F3J01PaazC2z3cY5ECpjRJyl6JBTCAsfZHFLK7DeUNN2QDX8rAd2erItL5NP11EdA4Nj_AUJf_1JeEvC_4EpmQZSWA3Tx3rg_JhZyWn02OvAnlh51PblfrLRziPBN3mYoE5C80waot6MZamzlqTxuDMJEtYtQmsYTfKeHJWStZV1kfzcffcg2NChVM_NwS0X6jG0WMct6EHBAiUC8jK-Ulc1YgX0VL1cpA.Eqfpx8QinoKBjaqZNH-4uBYb7yH47oJIN3_cEMgmpaY&dib_tag=se&keywords=lord+of+the+rings&qid=1725456922&sprefix=lord+of+the+rings%2Caps%2C108&sr=8-1')

