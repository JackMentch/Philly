from link_to_dataframe import link_to_dataframe
from get_player_data import get_stats_from_name
from plotter import *
from dataframe_functions import *

link = "https://questionnaire-148920.appspot.com/swe/data.html"

df = link_to_dataframe(link=link, fill_in_missing_data=False, check_for_data_disparity = False)

# print(get_stats_from_name("Harper, Bryce", 2016))

df = sort_by_salary(df=df)

df = nth_largest(df=df, n=15)

# print(average_salary(df))

# salary_histogram(df=df)


# salary_war_plot(df=df)

salary_position_plot(df)

# things to consider

# think about how someone should use this tool. should it be a library? an app?

# who will be using the tool? a developer? a data analyst?

# how do you want to organize the code given all the visualizations/queries you want to add? might be worth looking up
# some examples of how to structure python projects?

# does the user want to run the same visualizations/queries every time or do they want to be able to pick which queries
# to run

# are the interesting analyses you want to do using data from outside this webpage?

# (qualOfferProj) jackmentch@Jacks-MacBook-Pro Phillies % conda env export > environment.yml
