from link_to_dataframe import link_to_dataframe
from get_player_data import get_stats_from_name
from plotter import *
from dataframe_functions import *

link = "https://questionnaire-148920.appspot.com/swe/data.html"

# generates a dataframe from the dataset link
# fill_in_missing_data and check_for_data_disparity are left False because they significantly slow down system preformance
df = link_to_dataframe(link=link, fill_in_missing_data=False, check_for_data_disparity = False)

# look at the stats for a given player during 2016
print(f"Bryce Harper 2016 stats: {get_stats_from_name('Harper, Bryce', 2016)}")
print(f"Jean Segura 2016 stats: {get_stats_from_name('Segura, Jean', 2016)}")

# sorting out dataset so highest earning players are at the top
df = sort_by_salary(df=df)

# shortens the dataframe to only the to 125 highest earners
df = nth_largest(df=df, n=125)

qual_offer = average_salary(df)

print(f"\nQualifying Offer: ${qual_offer}")

salary_histogram(df=df)

# salary_war_plot(df)

# salary_position_plot(df)
