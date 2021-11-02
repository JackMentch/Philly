import re
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
from get_player_data import get_stats_from_name
import sys

# this function simply converts a string to an int
def string_to_int(string):

    if string is None:
        return None

    try:
        int_value = int(string)
        return int_value

    except ValueError:
        return None

# Call this function to search for a player's salary on baseball-reference
def find_salary(player_name, player_year):
    player_stats = get_stats_from_name(player_name, player_year)

    if player_stats:
        player_salary = player_stats["About"]["Salary"]
        player_salary = string_to_int(player_salary)
        return player_salary

    else:
        return None


# this function can be used if the user want to check if the salary data of the player in the given dataset is similar
# to the salary data of the player on baseball-reference
# if the function returns true, then there is a disparity between datasets
def check_salary_disparity(player_name, player_year, player_original_salary):
    player_stats = get_stats_from_name(player_name, player_year)

    if player_stats:
        player_salary = player_stats["About"]["Salary"]
        player_salary = string_to_int(player_salary)

        if player_salary is not None and player_original_salary is not None:

            ratio = float(player_salary/player_original_salary)

            if 0.8 > ratio or ratio > 1.25:
                return True

            else:
                return False

    return False

def link_to_dataframe(link, fill_in_missing_data, check_for_data_disparity):

    html = urlopen(link)
    bsObj = BeautifulSoup(html.read(),features="lxml")

    html_to_list = bsObj.findAll("tr")

    total_players = len(html_to_list)
    current_player = 0

    df = pd.DataFrame(columns = ['Name', 'Salary', 'Year', 'Level'])

    for player in html_to_list:
        current_player += 1

        player_name = player.find("td",{"class":"player-name"}).get_text()
        player_salary = player.find("td",{"class":"player-salary"}).get_text()
        player_year = player.find("td",{"class":"player-year"}).get_text()
        player_level = player.find("td",{"class":"player-level"}).get_text()

        player_salary = re.sub("[^0-9]", "", player_salary)

        player_salary = string_to_int(player_salary)
        player_year = string_to_int(player_year)


        # if there is no salary listed in the given dataset, the program will look it up on the baseball-reference webpage
        # if it cannot be found on the website, it will be set to None
        # running this section of code drastically slows runtime but improves the quality of data
        if fill_in_missing_data:
            if player_salary is None:
                player_salary = find_salary(player_name, player_year)

        # the code below checks if the salary data for a player on baseball-reference is significantly different than the
        # salary data from the dataset provided. Significantly slows down code so don't use it unless if necessary
        if check_for_data_disparity:
            if check_salary_disparity(player_name, player_year, player_salary):
                print(f"Salary disparity for:{player_name}")


        # append player to the pandas dataframe
        df = df.append({'Name': player_name, 'Salary': player_salary,
                        'Year': player_year, 'Level': player_level}, ignore_index=True)

        # print out to the terminal how many iterations have completed/remain
        sys.stdout.write("\r" + f"Loading players: {current_player}/{total_players}")
        sys.stdout.flush()

    print("\n")
    return df


# Examples of using the functions above

# link_to_dataframe(link = "https://questionnaire-148920.appspot.com/swe/data.html",
#                           fill_in_missing_data = False
#                           check_for_salary_disparity = False)