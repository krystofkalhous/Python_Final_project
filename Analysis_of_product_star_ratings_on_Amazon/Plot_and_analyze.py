#!/usr/bin/env python
# coding: utf-8

# In[3]:


import matplotlib.pyplot as plt
import scipy.stats as sts
import numpy as np


# In[4]:


def basic_bar_plot_of_star_reviews(dict_of_star_ratings = None, title = None,   ax = None, show_plot = False):
    
    if dict_of_star_ratings is None:
        raise ValueError("Please provide a valid dictionary of star ratings.")
    
    if ax is None:
        fig, ax = plt.subplots()

    rating_counts = list(dict_of_star_ratings.values())
    positions = list(dict_of_star_ratings.keys())
    
    ax.bar(positions, rating_counts, width=0.6, edgecolor='black', color='#FF9900')
    ax.set_xlabel('Star Ratings on 1 - 5 Scale')
    ax.set_ylabel('Number of Ratings')
    ax.set_title(f"Distribution of Star Ratings {' for ' + title if title else ''}")
    ax.set_xticks([1, 2, 3, 4, 5])
    
    total_reviews = sum(dict_of_star_ratings.values())
    
    if total_reviews > 0:
        weighted_sum = sum(star * count for star, count in dict_of_star_ratings.items())
        mean_rating = weighted_sum / total_reviews
        ax.axvline(x=mean_rating, color = 'red', linestyle = '--', linewidth = 2, label = f'Mean Rating: {mean_rating:.2f}')
        ax.legend()
        
    else:
        print("No reviews to display.")
    
    if show_plot:
        plt.show()
        

# Output
# "plot" = basic_bar_plot_of_star_reviews(dict_of_star_ratings, show_plot = True)


# In[5]:


def analyze(star_rating_counts, title = None, pri_1_s = 1, pri_2_s = 1, pri_3_s = 1, pri_4_s = 1, pri_5_s = 1, samples = 1000, plot = False):
    
    if not isinstance(star_rating_counts, dict):
        raise TypeError("star_rating_counts must be a dictionary")
        
    
    if not all(isinstance(i, int) for i in [pri_1_s, pri_2_s, pri_3_s, pri_4_s, pri_5_s]):
        raise TypeError("All priors must be integers")
    
    dirichlet_prior = {1: pri_1_s, 2: pri_2_s, 3: pri_3_s, 4: pri_4_s, 5: pri_5_s}
    
    # Combine the actual star counts and prior to form the parameters for the Dirichlet distribution
    value_dict = {}
    for i in range(1, 6):
        value_dict[i] = int(star_rating_counts.get(i, 0)) + dirichlet_prior.get(i, 0)
    
    # Draw samples from the Dirichlet distribution
    samples = np.random.dirichlet([value_dict[i] for i in range(1, 6)], size = samples)
    
    # Separate the samples by star rating
    data_list = [samples[:,i] for i in range(0, 5)]
    
    # Calculate statistics
    stds = {}
    upper_confint = {}
    lower_confint = {}
    means = {}
    
    for i in range(1,6):
        stds[i] = np.std(data_list[i-1])
        upper_confint[i] = np.quantile(data_list[i-1], 0.995)
        lower_confint[i] = np.quantile(data_list[i-1], 0.005)
        means[i] = np.mean(data_list[i-1])
    
    # Plot, if required
    if plot:
        plot_col_hist(
            labels = list(range(1, 6)),
            data_list = data_list,
            xaxis_label = 'Star Ratings',
            yaxis_label = f"Simulated proportions of star ratings in model{' for ' + title if title else ''}",
            means = means,
            upper_confint = upper_confint,
            lower_confint = lower_confint,
            ax = None,
            show_plot = True,
            figsize = (10, 8)
        )
        
    
    return stds, upper_confint, lower_confint, means, samples, data_list
    

# Output
# "Plot, if required" + stds, upper_confint, lower_confint, means, samples, data = analyze(star_rating_counts, pri_1_s = 1, pri_2_s = 1, pri_3_s = 1, pri_4_s = 1, pri_5_s = 1, samples = 1000, plot = True)


# In[7]:


def plot_col_hist(labels, data_list, xaxis_label, yaxis_label, means, upper_confint, lower_confint, title, 
                  ax = None, show_plot = False, figsize = (10, 8)):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    
    # Scatter plot of data. Here we added artificial noise to the x axis to make the plot more readable
    for i, j in enumerate(data_list):
        ax.scatter(sts.uniform.rvs(loc=i+1-0.2, scale=0.4, size=len(j)), 
                    j, s=4, alpha=1)
    
    # Plot means
    ax.plot(range(1, len(labels)+1),
             [means[k] for k in range(1, 6)], 
             marker='_', linewidth=0, color= "black", alpha=1, markersize=20, label='Mean of sampled data')
 
    # Plot upper confidence intervals
    ax.plot(range(1, len(labels)+1),
             [upper_confint[k] for k in range(1, 6)], 
             marker='_', linewidth=0, color="green", alpha=1, markersize=20, label='99% Confidence interval for sampled data')
    
    # Plot lower confidence intervals
    ax.plot(range(1, len(labels)+1),
             [lower_confint[k] for k in range(1, 6)], 
             marker='_', linewidth=0, color="green", alpha=1, markersize=20)
    
    # Set x-axis labels
    ax.set_xticks(range(1, len(labels)+1), labels)
    ax.set_xticklabels(labels)
    
    # Add legend and grid
    ax.legend()
    ax.set_title(f"Distribution of Star Ratings {' for ' + title if title else ''}")
    ax.grid(True, alpha=0.25, axis='y')
    ax.set_xlabel(xaxis_label)
    ax.set_ylabel(yaxis_label)
    
    if show_plot:
        plt.show()
        
# Output
# "plot, if required" = plot_col_hist(labels, data_list, xaxis_label, yaxis_label, means, upper_confint, lower_confint, show_plot = True)


# In[8]:


def combine_plots(dict_of_star_ratings, data, means, upper_confint, lower_confint, title,
                   figsize=(20, 10), show_plot=True):
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    basic_bar_plot_of_star_reviews(dict_of_star_ratings, title, ax=ax1)

    plot_col_hist(
        labels=list(range(1, 6)),
        data_list=data,
        xaxis_label='Star Ratings',
        yaxis_label='Proportions of star Ratings in model output',
        means=means,
        upper_confint=upper_confint,
        lower_confint=lower_confint,
        title=title,
        ax=ax2
    )

    plt.tight_layout()
    
    if show_plot:
        plt.show()

    return fig, (ax1, ax2)

# Output
# "Two plots, if required" = combine_plots(dict_of_star_ratings, data, means, upper_confint, lower_confint, title)

