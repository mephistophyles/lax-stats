from os import getcwd
from os.path import join
import re

def replace_names(data):
    names_to_replace = {"Boston U.": "BU",
                        "Ohio State": "OSU",
                        "Robert Morris": "RMU",
                        "Penn State": "PSU",
                        "Air Force": "AF",
                        "Detroit Mercy": "DMU",
                        "Mount St. Mary's": "MSM",
                        "Cleveland State": "CSU",
                        "North Carolina": "UNC",
                        "High Point": "HPU",
                        "UMass Lowell": "UMass-Lowell",
                        "Roberts Wesleyan": "Roberts-Wesleyan",
                        "Sacred Heart": "SHU",
                        "St. John's": "St-Johns",
                        "Baldwin Wallace": "Baldwin-Wallace",
                        "Saint Joseph's": "St-Josephs",
                        "Notre Dame": "ND",
                        "Ohio Valley": "Ohio-Valley",
                        "St. Thomas Aquinas": "St-Thomas-Aquinas",
                        "Holy Cross": "HCU",
                        "Johns Hopkins": "JHU",
                        "Stony Brook": "SBU",
                        "John Carroll": "John-Carroll",
                        "Baldwin Wallace": "Baldwin-Wallace",
                        "U. of DC": "UDC",
                        "Ohio Valley": "OV"
                        }
    for i in range(len(data)):
        try:
            for k, v in names_to_replace.items():
                if k in data[i]:
                    data[i] = data[i].replace(k, v)
        except:
            print("something went wrong with replacing names")
            continue
    return data


def convert_to_csv(data, year):
    f = open(join(getcwd(), f"data/{year}games.csv"), 'w+')
    header = "date,home,away,home-points,away-points\n"
    f.write(header)
    for line in data[2:]:
        new_line = " ".join(re.split("\s+", line, flags=re.UNICODE))
        new_line = new_line.split()
        if len(new_line) > 5:
            if new_line[1] == "N":
                new_line.pop(1)
            if new_line[1] == "T":
                new_line.pop(1)
        while len(new_line) > 5:
            new_line.pop()
        output_line = ",".join([i for i in new_line]) + "\n"
        f.write(output_line)
    f.close()



def parse(year):
    filename = f"data/{year}games.txt"
    filepath = join(getcwd(), filename)
    with open(filepath, 'r+') as f:
        data = f.read().split("\n")
    clean_data = replace_names(data)
    convert_to_csv(clean_data, year)


for year in [2013, 2014, 2015, 2016, 2017]:
    parse(year)