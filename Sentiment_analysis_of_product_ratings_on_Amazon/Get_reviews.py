#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Imports

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd


# In[ ]:


# downloading and saving the HTML content using Selenium

def download_html(driver, file_path):
    """
    Downloads the HTML content of the current page using a Selenium WebDriver and saves it to a specified file.

    Parameters:
    driver (selenium.webdriver): The Selenium WebDriver instance used to navigate and interact with the web page.
    file_path (str): The path (including the file name) where the HTML content should be saved.

    Returns:
    None: The function saves the HTML content of the current page to the specified file.
    """
    time.sleep(5)
     
    html_content = driver.page_source
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


# In[ ]:


# extracting reviews

def get_reviews(soup):
    """
    Extracts review details from a BeautifulSoup object representing a webpage containing reviews.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML of the webpage.

    Returns:
    list of dict: A list of dictionaries where each dictionary contains details of a review with 
                  keys "title", "body", "rating", and "date".

    Raises:
    SystemExit: If no reviews are found on the page, the function prints a message and exits the program.
    """
    reviews_list = []

    # finding the review elements
    reviews = soup.find_all('div', {'data-hook': 'review'})
    if not reviews:
        print("No reviews found on this page.")
        return reviews_list

    for review in reviews:
        try:
            # review title
            title_element = review.find('a', {'data-hook': 'review-title'})
            title = title_element.text.strip().split("\n")[-1] if title_element else 'No title'
            if title == 'No title':
                title_element = review.find('span', {'data-hook': 'review-title'})
                title = title_element.text.strip().split("\n")[-1] if title_element else 'No title'

            # review body
            body_element = review.find('span', {'data-hook': 'review-body'})
            body = body_element.text.strip() if body_element else 'No body'

            # review rating
            rating_element = review.find('i', {'data-hook': 'review-star-rating'})
            rating = rating_element.text.strip() if rating_element else 'No rating'
            if rating == 'No rating':
                rating_element = review.find('i', {'data-hook': 'cmps-review-star-rating'})
                rating = rating_element.text.strip() if rating_element else 'No rating'

            # review date
            date_element = review.find('span', {'data-hook': 'review-date'})
            date = date_element.text.strip() if date_element else 'No date'

            reviews_list.append({
                "title": title,
                "body": body,
                "rating": rating,
                "date": date
            })
        except AttributeError as e:
            print(f"Error parsing review: {e}")
    
    return reviews_list


# In[ ]:


# main function to scrape reviews, putting it into a data frame

def scrape(asin):
    """
    Extracts review details from a BeautifulSoup object representing a webpage containing reviews.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML of the webpage.

    Returns:
    list of dict: A list of dictionaries where each dictionary contains details of a review with 
                  keys "title", "body", "rating", and "date".

    Raises:
    SystemExit: If no reviews are found on the page, the function prints a message and exits the program.
    """
    html_file_path = 'amazon_reviews.html'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    driver = webdriver.Chrome(options=options)

    dataframe = pd.DataFrame(columns = ["title", "body", "rating", "date"])
    t = []
    b = []
    r = []
    d = []

    try:
        for page_number in range(1,11):
            url = f'https://www.amazon.co.uk/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(page_number)
            driver.get(url)
            download_html(driver, html_file_path)
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            reviews = get_reviews(soup)
            if not reviews and page_number == 1:  # if no reviews found on the first page => break the loop
                break
            for review in reviews:
                t.append(review["title"])
                b.append(review["body"])
                r.append(review["rating"])
                d.append(review["date"])
            

    finally:
        driver.quit()
    
    dataframe["title"] = t
    dataframe["body"] = b
    dataframe["rating"] = r
    dataframe["date"] = d

    return dataframe

