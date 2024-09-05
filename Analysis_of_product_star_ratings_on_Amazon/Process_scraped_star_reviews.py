#!/usr/bin/env python
# coding: utf-8

# In[1]:


def convert_list_to_dict(star_reviews_list):
    
    # Initialize it this way, for if the ratings were "truanced", i.e. no 1 star rating etc.
    dict_of_ratings_percentages = {1:0, 2:0, 3:0, 4:0, 5:0}

    for label in star_reviews_list:
        parts = label.split(' percent of reviews have ')
        
        if len(parts) == 2:
            percentage_str = parts[0].strip()
            stars_str = parts[1].replace(' stars', '').strip()

            try:
                percentage_value = int(percentage_str)
                stars_value = int(stars_str)

                dict_of_ratings_percentages[stars_value] = percentage_value
                
            except ValueError:
                print(f"Error converting values: percentage_str='{percentage_str}', stars_str='{stars_str}'")
    
    return dict_of_ratings_percentages
    
# Output
# dict_of_ratings_percentages = convert_list_to_dict(star_reviews_list)


# In[2]:


def convert_star_percentages_to_values_df(dict_of_ratings_percentages, no_of_ratings):
    dict_of_star_ratings = {}
    
    # Here, we round the result, hoping that any inaccuracy we create by this is negligible
    for i in range(1,6):
        dict_of_star_ratings[i] = int(round((dict_of_ratings_percentages[i] / 100) * no_of_ratings))
        
    return dict_of_star_ratings
    
# Output
# dict_of_star_ratings = convert_star_percentages_to_values_df(dict_of_ratings_percentages, no_of_ratings)

