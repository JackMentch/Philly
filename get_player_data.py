from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
import re

# player name should be inserted in the format: <firstname lastname>
# example is player_name = "Bryce Harper"
# current year should be entered as an int in the format: <XXXX>
# example is current_year = 2016

def get_stats_from_name(player_name, current_year):


    link = get_player_page(find_player_name=player_name, current_year=current_year)
    return extract_data_from_link(link = link, current_year=current_year)


def get_player_page(find_player_name, current_year):


    first_letter_last_name = find_player_name.split(", ")[0][0].lower()

    # baseball references sorts players by the first letter of their last name
    # the link below returns a html file of all MLB players that have a last name beginning with a specified letter
    link = f"https://www.baseball-reference.com/players/{first_letter_last_name}"

    html = urlopen(link)
    bsObj = BeautifulSoup(html.read(),features="lxml")

    # we will extract the html file as a list of <p> tags that contain a player's name, service time, and a link to their
    # specific baseball-reference page
    list_of_players = bsObj.find("div",{"id":"div_players_"}).findAll("p")


    # we will iterate through the list of players, until we find a player with the name specified who is active in MLB
    # during the year specified
    for player in list_of_players:

        # Extract the link to the player's baseball reference page from the html code
        player_link = player.find("a")['href']

        # Some players have a '+' in their name, it must be removed in order to properly retrieve name and service time
        player_name, service_time = player.get_text().replace("+"," ").split("  ")

        # reformat player_name so it matches the structure of our input find_player_name <lastname, firstname>

        player_name = player_name.split(" ")

        # some players don't have last names so dont do anything
        if len(player_name) > 1:

            # format to <lastname>, <firstname>
            player_name = player_name[1] + ", " + player_name[0]

        # Reformat each year so we can use it to check if our specified year falls between the debut_year and final_year
        debut_year, final_year = service_time[1:-1].split("-")

        # There may be multiple players with the same name, but we want the player that is active during the year we specified
        # My code is limited here, if two players with the same name are active during the same year, it will choose whichever
        # player had the earlier debut year
        # if the dataset provided had an extra column for player_id or team, this could be avoided
        if int(debut_year) <= current_year <= int(final_year) and player_name == find_player_name:

            return f"https://www.baseball-reference.com{player_link}"

    # if no player exists with the name specified during the year specified, return None
    return None


# input a baseball-reference.com link for a player and this function scrapes the site and
# returns the data in JSON format.
def extract_data_from_link(link, current_year):

    # if no link is given just return None
    if not link:
        return None

    html = urlopen(link)
    bsObj = BeautifulSoup(html.read(),features="lxml")

    # Initialize the player's WAR to 0
    pitching_war = 0
    batting_war = 0
    player_salary = None
    player_age = None

    # Preform a BS find function to get the position of our player
    player_position = bsObj.find("div",{"itemtype":"https://schema.org/Person"}).find("p").get_text()

    # Clean up the string which was returned so we can store the players defensive position
    player_position = player_position.replace("\n","").replace(" ", "").split(":")[1]

    # Player position should be a list because players can play multiple positions
    player_position = re.split(',|and',player_position)


    # baseball-reference.com stores data like WAR and Salary in HTML that is commented out when you look at the source code.
    # To retrieve the data, I had to find all the comments, convert it to a string, then convert to a BeautifulSoup Object
    # from there I can run BS commands to find the tags/data I wanted.
    comments = bsObj.findAll(string=lambda text: isinstance(text, Comment))

    for c in comments:

        # convert the comment to BS Object
        c_string = BeautifulSoup(str(c), features="lxml")

        # this selects the row of a table for the particular year we want. One is done for pitching data, one is done for hitting data
        # it would make sense to only look at pitching_stats for pitchers, and batting_stats for batters, but pitchers hit in the National
        # League and often times position players are asked to pitch in games during the year
        pitching_stats = c_string.findAll("tr", {"id":f"pitching_value.{str(current_year)}"})
        batting_stats = c_string.findAll("tr", {"id":f"batting_value.{str(current_year)}"})


        # even if we specify one year, a player may have been traded mid-season. Meaning for one year, there can be multiple rows.
        # If a player was never traded that year, each for loop executes once. If a player was traded n times, the for loop, executes n times

        for pitching_stat in pitching_stats:

            # WAR is cumulative so if a player has 2 WAR with team A this year, and 3 WAR on team B this year,
            # The player would have 5 WAR for this year
            try:
                pitching_war += float(pitching_stat.find("td", {"data-stat":"WAR_pitch"}).get_text())

                player_age = pitching_stat.find("td", {"data-stat":"age"}).get_text()
                player_salary = pitching_stat.find("td", {"data-stat":"Salary"}).get_text()
                player_salary = re.sub("[^0-9]", "", player_salary)

            except ValueError:
                continue

        for batting_stat in batting_stats:

            # Same as above with pitching_war
            try:
                batting_war += float(batting_stat.find("td", {"data-stat":"WAR"}).get_text())

                player_age = batting_stat.find("td", {"data-stat":"age"}).get_text()
                player_salary = batting_stat.find("td", {"data-stat":"Salary"}).get_text()
                player_salary = re.sub("[^0-9]", "", player_salary)

            except ValueError:
                continue


    # Store and return the data in a JSON format for ease of use and readiblity

    return {"About": {"Position":player_position, "Salary":player_salary, "Age":player_age},
                "Pitching": {"Pitching WAR":pitching_war},
                "Batting": {"Batting WAR": batting_war}}



# Examples of using the functions above

# player_data = get_stats_from_name("Brooks, Aaron", 2015)
# print(player_data)

# print(player_data) ------> {'About': {'Position': 'Rightfielder', 'Salary': '5000000', 'Age': '23'},
#                             'Pitching': {'Pitching WAR': 0},
#                             'Batting': {'Batting WAR': 1.5}}

# print(player_data["About"]["Position"]) ------> Rightfielder