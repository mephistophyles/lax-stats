import json
from os.path import join
from os import getcwd
import requests
from bs4 import BeautifulSoup
import pandas as pd


class HTMLTableParser:

    def __init__(self, year, team):
        self.url = f"http://stats.ncaa.org/player/game_by_game?game_sport_year_ctl_id={year}&org_id={team}&stats_player_seq=-100"
        self.team = team
        self.year = year
        self.outputname = join(getcwd(), f"data/{test_translation[year]}/{test_translation[team]}.csv")
        print(f"starting on {self.outputname}")
        self.parse_url(self.url)

    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return self.parse_html_table(soup)

    def parse_html_table(self, souptag):
        soup = souptag.find_all("table", class_="mytable")[1]  # we want the game-by-game table, not the overall one
        # column_names = [x for x in soup.find("tr", class_="grey_heading").text.split("\n") if x != ""]
        column_names = ['Date', 'Opponent', 'Result', 'Goals', 'Assists', 'Points', 'Shots', 'SOG', 'GB', 'TO', 'CT', 'FO Won', 'FO Taken', 'Pen', 'Pen Time', 'G Min', 'Goals Allowed', 'Saves']
        df = pd.DataFrame(columns=column_names)
        i = 0
        # TODO deal with missing data, NJIT and Hampton don't have data for all these seasons
        for row in soup.find_all("tr")[2:]:
            row_contents = [x.strip() for x in row.text.split("\n") if x.strip() != '']
            if row_contents[0] != "Defensive Totals":
                while len(row_contents) > 18:
                    del row_contents[8]  # 8th index place is man down and/or man up goal
                df.loc[i] = row_contents
                i+=1
        df.to_csv(self.outputname, mode="w+")
        print(f"finished {self.outputname}")





# year_id = 11380
# team_id =193
# HTMLTableParser(year_id, team_id)
test_years = [11380, 11580, 12121]
test_teams = [688, 322, 19651, 148]

test_translation = {11380: 2013, 11580: 2014, 12121: 2015, 193:"Duke", 183: "Denver", 688: "Syracuse", 322: "JHU", 19651: "HPU", 148: "CSU"}

for team in test_teams:
    for year in test_years:
        hp = HTMLTableParser(year, team)
