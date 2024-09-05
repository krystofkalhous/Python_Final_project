#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Imports
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sts

# Import modules
import Scrape_star_reviews_from_Amazon
import Process_scraped_star_reviews
import Plot_and_analyze
import Test_convergence_of_stds_in_model
import two_products_comparison_plotter


# In[ ]:


# helper functions
def get_optional_int_input(prompt, default_value=1):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            return default_value
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer.")
            
def prompt_user_for_yes_no_input(prompt):
    while True:
        yes_no = input(prompt).strip().lower()
        if yes_no in ['yes', 'no']:
            return yes_no
        else:
            print('Please input just yes or no')
            


# Input URL of product

def perform_analysis_based_on_user_input():
    url1 = input('Please input the url of Amazon product: ')
    
    compare_with_another_product = prompt_user_for_yes_no_input('Do you want to compare it to another Amazon product? Please input yes/no :')
        
    
    if compare_with_another_product == 'yes':
        url2 = input('Please input the url of second Amazon product: ')


    # Analysis settings
    show_hist_of_ratings = prompt_user_for_yes_no_input('Do you want to see histogram of star ratings? If yes, input: yes (else click Enter) :')
    
    show_plot_of_simulated_ratings = prompt_user_for_yes_no_input('Do you want to see plot of simulated star ratings? If yes, input: yes (else click Enter) :')

    detailed_two_products_star_comparison = 'no'
    if compare_with_another_product == 'yes':
        detailed_two_products_star_comparison = prompt_user_for_yes_no_input('Do you want to compare one specific star distributions between two models?: yes/no')
        assert detailed_two_products_star_comparison == 'yes' or detailed_two_products_star_comparison == 'no' 'Please input just yes/no'

        if detailed_two_products_star_comparison == 'yes':
            while True:
                i_stars = get_optional_int_input('Please imput which star rating do you want to compare in detail (i.e.: 1, 2, 3, 4, 5): ')
                if 1 <= i_stars <= 5:
                    break
                else:
                    print("The value must be between 1 and 5. Please try again.")



    if show_plot_of_simulated_ratings == 'yes':
        
        pri_1_s = get_optional_int_input(
        f"Please input integer priors for the Dirichlet distribution {' for the first product' if compare_with_another_product == 'yes' else ''}, else they all default to 1, Prior for 1 star reviews: ")

        pri_2_s = get_optional_int_input('Prior for 2 star reviews (default is 1): ')
        pri_3_s = get_optional_int_input('Prior for 3 star reviews (default is 1): ')
        pri_4_s = get_optional_int_input('Prior for 4 star reviews (default is 1): ')
        pri_5_s = get_optional_int_input('Prior for 5 star reviews (default is 1): ')


        if compare_with_another_product == 'yes':
            pri_1_s_B = get_optional_int_input('Please input integer priors for the second product, else they all default to 1, Prior for 1 star reviews: ')
            pri_2_s_B = get_optional_int_input('Prior for 2 star reviews (default is 1): ')
            pri_3_s_B = get_optional_int_input('Prior for 3 star reviews (default is 1): ')
            pri_4_s_B = get_optional_int_input('Prior for 4 star reviews (default is 1): ')
            pri_5_s_B = get_optional_int_input('Prior for 5 star reviews (default is 1): ')



    analyze_convergence = prompt_user_for_yes_no_input('Do you want to see plot of the analysis of convergence of standard deviations in the model? If yes, input: yes (else click Enter) :')

    # Execution
    star_reviews_list, no_of_ratings, title = Scrape_star_reviews_from_Amazon.retrieve_star_ratings_from_Amazon(url1)
    dict_of_star_ratings = Process_scraped_star_reviews.convert_star_percentages_to_values_df(Process_scraped_star_reviews.convert_list_to_dict(star_reviews_list), no_of_ratings)   

    if compare_with_another_product == 'yes':
        # Scrape data for product B
        star_reviews_list_B, no_of_ratings_B, title_B = Scrape_star_reviews_from_Amazon.retrieve_star_ratings_from_Amazon(url2)
        # Process data for product B
        dict_of_star_ratings_B = Process_scraped_star_reviews.convert_star_percentages_to_values_df(Process_scraped_star_reviews.convert_list_to_dict(star_reviews_list_B), no_of_ratings_B) 
    

    if show_hist_of_ratings == 'yes' and show_plot_of_simulated_ratings == 'yes' and compare_with_another_product == 'no':
        stds, upper_confint, lower_confint, means, samples, data = Plot_and_analyze.analyze(dict_of_star_ratings, title, pri_1_s, pri_2_s, pri_3_s, pri_4_s, pri_5_s, samples = 1000, plot = False)
        Plot_and_analyze.combine_plots(dict_of_star_ratings, data, means, upper_confint, lower_confint, title, show_plot=True)



    if show_hist_of_ratings == 'yes':
        if compare_with_another_product == 'yes':
            two_products_comparison_plotter.two_hist_comparison(dict_of_star_ratings, title, dict_of_star_ratings_B, title_B)

        elif show_hist_of_ratings == 'yes' and show_plot_of_simulated_ratings == 'no':
            Plot_and_analyze.basic_bar_plot_of_star_reviews(dict_of_star_ratings, title, ax = None, show_plot = True)
    
    if show_plot_of_simulated_ratings == 'yes':
        if compare_with_another_product == 'yes':
            _, upper_confint, lower_confint, means, samples, data = Plot_and_analyze.analyze(dict_of_star_ratings, title, pri_1_s, pri_2_s, pri_3_s, pri_4_s, pri_5_s, samples = 1000, plot = False)
            _, upper_confint_B, lower_confint_B, means_B, samples_B, data_B = Plot_and_analyze.analyze(dict_of_star_ratings_B, title_B, pri_1_s_B, pri_2_s_B, pri_3_s_B, pri_4_s_B, pri_5_s_B, samples = 1000, plot = False)
            two_products_comparison_plotter.two_sims_hist_comparison(data, means, upper_confint, lower_confint, title, data_B, means_B, upper_confint_B, lower_confint_B, title_B)

        elif show_hist_of_ratings == 'no' and show_plot_of_simulated_ratings == 'yes':
            Plot_and_analyze.analyze(dict_of_star_ratings, title, pri_1_s, pri_2_s, pri_3_s, pri_4_s, pri_5_s, samples = 1000, plot = True)

    if detailed_two_products_star_comparison == 'yes':
        stds, upper_confint, lower_confint, means, samples, data = Plot_and_analyze.analyze(dict_of_star_ratings, title, pri_1_s, pri_2_s, pri_3_s, pri_4_s, pri_5_s, samples = 1000, plot = False)
        stds_B, upper_confint_B, lower_confint_B, means_B, samples_B, data_B = Plot_and_analyze.analyze(dict_of_star_ratings_B, title_B, pri_1_s_B, pri_2_s_B, pri_3_s_B, pri_4_s_B, pri_5_s_B, samples = 1000, plot = False)

        stds_i_stars, upper_confint_i_stars, lower_confint_i_stars, means_i_stars, data_list_i_stars, labels, i_stars = two_products_comparison_plotter.modify_data_for_detailed_comparison_of_stars(title, stds, upper_confint, lower_confint, means, data, title_B, stds_B, upper_confint_B, lower_confint_B, means_B, data_B, i_stars)
        two_products_comparison_plotter.plot_col_hist_compare(labels, data_list_i_stars, means_i_stars, upper_confint_i_stars, lower_confint_i_stars, i_stars, ax = None, show_plot = True)

    if analyze_convergence == 'yes':
        
        if compare_with_another_product == 'yes':
            Test_convergence_of_stds_in_model.plot_convergence_of_stds(Test_convergence_of_stds_in_model.create_artificial_star_ratings_df(dict_of_star_ratings), title, ax = None, show_plot = True)
            Test_convergence_of_stds_in_model.plot_convergence_of_stds(Test_convergence_of_stds_in_model.create_artificial_star_ratings_df(dict_of_star_ratings_B), title_B, ax = None, show_plot = True)


        else:
            Test_convergence_of_stds_in_model.plot_convergence_of_stds(Test_convergence_of_stds_in_model.create_artificial_star_ratings_df(dict_of_star_ratings), title, ax = None, show_plot = True)
        

# Output
# "Performs analysis of the star ratings of the products" = perform_analysis_based_on_user_input()

