#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import matplotlib.pyplot as plt


# In[13]:


def create_artificial_star_ratings_df(dict_of_star_ratings):
    
    artificial_star_ratings_df = []
    
    for star_rating, count in dict_of_star_ratings.items():
        artificial_star_ratings_df.extend([star_rating] * count)
        
    
    artificial_star_ratings_df = pd.DataFrame(artificial_star_ratings_df, columns=['rating'])
    # Here, I want to shuffle the dataframe, we are assuming here, that the different ratings are comming at random, hence this should sufficiently closely replicate real data.
    artificial_star_ratings_df = artificial_star_ratings_df.sample(frac=1).reset_index(drop=True)
        
    return artificial_star_ratings_df

# Output
# artificial_star_ratings_df = create_artificial_star_ratings_df(dict_of_star_ratings)


# In[14]:


def plot_convergence_of_stds(artificial_star_ratings_df, title, ax = None, show_plot = False):

    list_of_i_star_reviews_samples = []
    list_of_stds_samples = []
    previous_no_of_i_star_reviews_sample = None
    
    len_df = len(artificial_star_ratings_df)
    
    # somewhat arbitrary value for the no of reviews in the if condition 
    if len_df < 20:
        print('Sample is too small')
        return

    elif len_df > 100000:
        sampling_rate = 1000
    elif len_df > 10000:
        sampling_rate = 10
    else:
        sampling_rate = 1
        
    num_reviews = []
    
    
    for n in range(1, len_df + 1):
        
        x = sampling_rate * n
            
        sample_df = artificial_star_ratings_df.sample(min(x, len(artificial_star_ratings_df)), replace = False)
        
        # count no of i star reviews in the sample
        no_of_i_star_reviews_sample = sample_df['rating'].value_counts().reindex(range(1, 6), fill_value=0).to_dict()
        
        # for performance reasons we sort the dictionaries and convert them to tuples for comparison
        current_sample_tuple = tuple(sorted(no_of_i_star_reviews_sample.items()))
        previous_sample_tuple = tuple(sorted(previous_no_of_i_star_reviews_sample.items())) if previous_no_of_i_star_reviews_sample else None

        # stop condition, if we already sampled whole data
        if previous_sample_tuple is not None and current_sample_tuple == previous_sample_tuple:
            break
        
        list_of_i_star_reviews_samples.append(no_of_i_star_reviews_sample)
        num_reviews.append(len(sample_df))
        previous_no_of_i_star_reviews_sample = no_of_i_star_reviews_sample
    

    for k in range(0, len(list_of_i_star_reviews_samples)):
        stds, _, _, _, _, _ = analyze(list_of_i_star_reviews_samples[k])
        stds['num_reviews'] = num_reviews[k]  # Store number of reviews for each sample
        list_of_stds_samples.append(stds)

    series_data = pd.DataFrame(list_of_stds_samples)
    series_data = series_data.rename(columns={1: '1 star', 2: '2 star', 3: '3 star', 4: '4 star', 5: '5 star'})
    series_data = series_data.sort_values(by='num_reviews')
    series_data.set_index('num_reviews', inplace=True)

    # we smooth the data using moving average for better plot readability, if the data is sufficiently large
    if len_df > 1000:
        window_size = 30
    elif len_df > 50:
        window_size = 8
    else:
        window_size = 1

    if window_size > 1:
        for o in range(1, 6):
            series_data[f"{o} star"] = series_data[f"{o} star"].rolling(window=window_size, center=True).mean()
    
            
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        
    series_data.plot(ax=ax)
    ax.set_title(f"Convergence of standard deviations in model{' for product ' + title if title else ''}")
    ax.set_xlabel('Number of ratings')
    ax.set_ylabel('Standard deviation of sampled parameters')
    ax.grid(True)
    
    if show_plot:
        plt.show()
        

