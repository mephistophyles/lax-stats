import json
from os.path import isfile, join
from os import getcwd
import requests
from bs4 import BeautifulSoup
import pandas as pd


class HTMLTableParser:

    def __init__(self, year, team):
        self.team = team
        self.year = str(year)
        self.url = f"http://stats.ncaa.org/player/game_by_game?game_sport_year_ctl_id={year_list[self.year]}&org_id={team_list[self.team]}&stats_player_seq=-100"
        self.outputname = join(getcwd(), f"data/{self.year}/{self.team}.csv")
        print(f"starting on {self.outputname}")
        self.parse_url(self.url)

    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return self.parse_html_table(soup)

    def parse_html_table(self, souptag):
        try:
            soup = souptag.find_all("table", class_="mytable")[1]  # we want the game-by-game table, not the overall one
            # column_names = [x for x in soup.find("tr", class_="grey_heading").text.split("\n") if x != ""]
            column_names = ['Date', 'Opponent', 'Result', 'Goals', 'Assists', 'Points', 'Shots', 'SOG', 'EMOG', 'MDDG', 'GB', 'TO', 'CT', 'FO Won', 'FO Taken', 'Pen', 'Pen Time', 'G Min', 'Goals Allowed', 'Saves']
            df = pd.DataFrame(columns=column_names)
            i = 0
            for row in soup.find_all("tr")[2:]:
                row_contents = [x.strip() for x in row.text.split("\n") if x.strip() != '']
                # TODO make this more robust to handle man up, man down, and penalties
                if row_contents[0] != "Defensive Totals":
                    row_data = []
                    for td in row.find_all("td"):
                        row_data.append(td.text)
                    df.loc[i] = row_data[:20]
                    i+=1
            df.to_csv(self.outputname, mode="w+")
            print(f"finished {self.outputname}")
        except:
            print(f"We seem to have run into a problem parsing {self.team}'s {self.year} season data")

json_file = join(getcwd(), "data/ncaaorgdata.json")
with open(json_file, 'r') as f:
    site_data = json.load(f)
team_list = site_data["teams"]
year_list = site_data["year_codes"]

for team in team_list.keys():
    for year in year_list.keys():
        # print(f"Let's parse the {year} season of {team}")
        if not isfile(join(getcwd(), f"data/{year}/{team}.csv")):
            hp = HTMLTableParser(year, team)
        else:
            print(f"Already processed {year} of {team}")