from os import getcwd
from os.path import join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm


def goals_for_and_against(year, output=False):
    file = join(getcwd(), f"data/{year}games.csv")
    data = pd.read_csv(file)
    teams = {}
    home_goals = 0
    away_goals = 0
    games = 0
    for line in range(data.shape[0]):
        home = data.loc[line,:][1]
        away = data.loc[line,:][2]
        g_home = int(data.loc[line,:][3])
        g_away = int(data.loc[line,:][4])
        if home not in teams.keys():
            teams[home] = {"home_scored": 0, "home_givenup": 0, "away_scored": 0, "away_givenup": 0, "home_games_played": 0, "away_games_played": 0}
        if away not in teams.keys():
            teams[away] = {"home_scored": 0, "home_givenup": 0, "away_scored": 0, "away_givenup": 0, "home_games_played": 0, "away_games_played": 0}
        teams[home]["home_scored"] = teams[home]["home_scored"] + g_home
        teams[home]["home_givenup"] = teams[home]["home_givenup"] + g_away
        teams[away]["away_scored"] = teams[away]["away_scored"] + g_away
        teams[away]["away_givenup"] = teams[away]["away_givenup"] + g_home
        teams[away]["away_games_played"] = teams[away]["away_games_played"] + 1
        teams[home]["home_games_played"] = teams[home]["home_games_played"] + 1
        home_goals += g_home
        away_goals += g_away
        games += 1
    if output:
        print(f"Total goal advantage of the home team is {(home_goals-away_goals)/games}.")
        team_list = teams.keys()
        for team in team_list:
            try:
                played_home = teams[team]["home_games_played"]
                played_away = teams[team]["away_games_played"]
                goals_home_scored = teams[team]["home_scored"]
                goals_home_givenup = teams[team]["home_givenup"]
                goals_away_scored = teams[team]["away_scored"]
                goals_away_givenup = teams[team]["away_givenup"]
                print(f"{team} scored on average {goals_home_scored/played_home} goals, vs giving up {goals_home_givenup/played_home} at home\n"
                      f"they also scored {goals_away_scored/played_away} goals away, vs giving up {goals_away_givenup/played_away}\n\n")
            except:
                print()
    return pd.DataFrame.from_dict(teams).transpose()


def home_away_goals_df(year):
    file = join(getcwd(), f"data/{year}games.csv")
    data = pd.read_csv(file)
    return data


def plot_home_away(year):
    data = home_away_goals_df(year)
    plt.hist(data[['home-points', 'away-points']].values, range(25),
             alpha=0.7, label=['home goals', 'away goals'], normed=True, color=['red', 'blue'])
    plt.show()


# goals_for_and_against(2017, True)
#
# data = home_away_goals_df(2017)
# plt.plot(data['home-points'])
# plt.plot(data['away-points'])
# plt.show()
plot_home_away(2015)
