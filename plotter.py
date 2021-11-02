import matplotlib as plt
from get_player_data import get_stats_from_name
import matplotlib.pyplot as plt
import sys


def salary_war_plot(df):
    total_players, current_player = len(df), 0

    for ind in df.index:
        current_player += 1

        player_name, player_salary, current_year = df['Name'][ind], df['Salary'][ind], df['Year'][ind]

        player_data = get_stats_from_name(player_name,current_year= current_year)

        player_salary = float(player_salary/1000000)

        total_war = 0

        plt.title('Salary vs WAR Graph')
        plt.xlabel('Salary $ (in Millions)')
        plt.ylabel('WAR')


        if player_data is not None:
            pitching_war = player_data["Pitching"]["Pitching WAR"]
            batting_war = player_data["Batting"]["Batting WAR"]

            total_war = 0

            if pitching_war is not None:
                total_war += pitching_war

            if batting_war is not None:
                total_war += batting_war

            plt.scatter( player_salary,total_war, c='blue')

        sys.stdout.write("\r" + f"Loading players: {current_player}/{total_players}")
        sys.stdout.flush()

    print("\n")
    return plt.show()


def salary_position_plot(df):
    total_players, current_player = len(df), 0

    total_positions = []

    plt.title('Representation of Positions Within the Dataframe')
    plt.xlabel('Positions')
    plt.ylabel('Number of players')

    for ind in df.index:
        current_player += 1

        player_name, player_salary, current_year = df['Name'][ind], df['Salary'][ind], df['Year'][ind]

        player_data = get_stats_from_name(player_name,current_year= current_year)

        if player_data is not None:

            player_positions = player_data["About"]["Position"]

            for position in player_positions:
                total_positions.append(position)

        sys.stdout.write("\r" + f"Loading players: {current_player}/{total_players}")
        sys.stdout.flush()


    unique_positions = set(total_positions)

    for position in unique_positions:

        plt.bar(position, total_positions.count(position), color='green')

    print("\n")
    return plt.show()


def salary_histogram(df):

    salaries = df['Salary'].tolist()
    salaries = [float(item/1000000) for item in salaries if item is not None]

    plt.title('Salary Histogram')
    plt.xlabel('Salary $ (in Millions)')
    plt.ylabel('Number of players')

    num_bins = len(set(salaries))//3

    n, bins, patches = plt.hist(salaries, num_bins, facecolor='blue', alpha=0.5)

    return plt.show()
