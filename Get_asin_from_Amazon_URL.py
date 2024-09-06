#!/usr/bin/env python
# coding: utf-8

# In[39]:


def get_asin(url):
    """Get asin from Amazon product URL"""
    
    if not isinstance(url, str):
        raise ValueError("Input URL must be a string. For example: 'https://www.amazon.co.uk/dp/B08N5WRWNW'")
        
    l = url.split('/')
    
    asin = None
    prev_element = ''
    
    for element in l:
        if prev_element == 'dp':
            asin = element
            break
            
        prev_element = element
        
    if not isinstance(asin, str):
        print('URL does not contain ASIN (Amazon product identifier code)')
        return asin
            
    return str(asin)
    
# Output
# str(ASIN) = get_asin('https://www.amazon.com/Game-Thrones-Song-Fire-Book/dp')

