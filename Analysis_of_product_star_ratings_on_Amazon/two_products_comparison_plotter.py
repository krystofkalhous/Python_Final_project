#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import packages
import matplotlib.pyplot as plt
import scipy.stats as sts

# Import modules
import Plot_and_analyze


# In[1]:


def two_hist_comparison(dict_of_star_ratings_product_A, title_A, dict_of_star_ratings_product_B, title_B):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    Plot_and_analyze.basic_bar_plot_of_star_reviews(dict_of_star_ratings_product_A, title_A, ax = ax1)

    Plot_and_analyze.basic_bar_plot_of_star_reviews(dict_of_star_ratings_product_B, title_B, ax = ax2)

    plt.tight_layout()
    plt.show()
    


# In[ ]:


def two_sims_hist_comparison(data_A, means_A, upper_confint_A, lower_confint_A, title_A, data_B, means_B, upper_confint_B, lower_confint_B, title_B):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    Plot_and_analyze.plot_col_hist(labels=list(range(1, 6)), data_list=data_A, xaxis_label='Star Ratings', yaxis_label='Proportions of star Ratings in model output', means=means_A, upper_confint=upper_confint_A, lower_confint=lower_confint_A, title = title_A, ax = ax1)
    
    Plot_and_analyze.plot_col_hist(labels=list(range(1, 6)), data_list=data_B, xaxis_label='Star Ratings', yaxis_label='Proportions of star Ratings in model output', means=means_B, upper_confint=upper_confint_B, lower_confint=lower_confint_B, title = title_B, ax = ax2)
    
    y_min = min(ax1.get_ylim()[0], ax2.get_ylim()[0])
    y_max = max(ax1.get_ylim()[1], ax2.get_ylim()[1])
    
    ax1.set_ylim([y_min, y_max])
    ax2.set_ylim([y_min, y_max])
    
    
    plt.tight_layout()
    plt.show()
    


# In[ ]:


def modify_data_for_detailed_comparison_of_stars(title_A, stds_A, upper_confint_A, lower_confint_A, means_A, data_A, title_B, stds_B, upper_confint_B, lower_confint_B, means_B, data_B, i_stars):

    if not isinstance(i_stars, int) or not (1 <= i_stars <= 5):
        raise ValueError('i_stars should be an integer between 1 and 5.')

    stds_i_stars = {'A':0, 'B':0}
    upper_confint_i_stars = {'A': 0, 'B': 0}
    lower_confint_i_stars = {'A': 0, 'B': 0}
    means_i_stars = {'A': 0, 'B': 0}

    stds_i_stars['A'] = stds_A[i_stars]
    stds_i_stars['B'] = stds_B[i_stars]
    upper_confint_i_stars['A'] = upper_confint_A[i_stars]
    upper_confint_i_stars['B'] = upper_confint_B[i_stars]
    lower_confint_i_stars['A'] = lower_confint_A[i_stars]
    lower_confint_i_stars['B'] = lower_confint_B[i_stars]
    means_i_stars['A'] = means_A[i_stars]
    means_i_stars['B'] = means_B[i_stars]

    data_list_i_stars = []
    data_list_i_stars.append(data_A[i_stars-1])
    data_list_i_stars.append(data_B[i_stars-1])
    
    labels = [title_A, title_B]

    return stds_i_stars, upper_confint_i_stars, lower_confint_i_stars, means_i_stars, data_list_i_stars, labels, i_stars


# In[ ]:


def plot_col_hist_compare(labels, data_list, means, upper_confint, lower_confint, i_stars, ax = None, 
                  show_plot = False, figsize = (10, 8)):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # Scatter plot of data. Here we added artificial noise to the xaxis to make the plot more readable
    for i, j in enumerate(data_list):
        title = f"{i+1}: title {labels[i]}"
        ax.scatter(sts.uniform.rvs(loc=i+1-0.2, scale=0.4, size=len(j)), 
                    j, s=4, alpha=1)
    
    # Plot means
    ax.plot(range(1, len(labels)+1),
             [means[k] for k in ['A','B']], 
             marker='_', linewidth=0, color="black", alpha=1, markersize=20, label='Mean of sampled data')
 
    # Plot upper confidence intervals
    ax.plot(range(1, len(labels)+1),
             [upper_confint[k] for k in ['A','B']], 
             marker='_', linewidth=0, color="green", alpha=1, markersize=20, label='99% Confidence interval for sampled points')
    
    # Plot lower confidence intervals
    ax.plot(range(1, len(labels)+1),
             [lower_confint[k] for k in ['A','B']], 
             marker='_', linewidth=0, color="green", alpha=1, markersize=20)
    
    # Set x-axis labels
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    
    # Add legend and grid
    ax.legend()
    ax.grid(True, alpha=0.25, axis='y')
    ax.set_ylabel(f'Sampled probability of a {i_stars} star rating')
    
    if show_plot:
        plt.show()

