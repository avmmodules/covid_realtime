'''
    Description: Get data of COVID-19 in realtime with Python.
    Author: aulerjbailey
    Version: 1.0.0
    Video: https://youtu.be/tYJHAYA7wVI
'''
from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import matplotlib.pyplot as plt
import json

num = 0 # counter
analize = "infected" # what we're gonna analyze (see data_country.json file)
link = "https://www.worldometers.info/coronavirus/" # page

# open file
with open('src/data/data_country.json') as json_file:
    country = json.load(json_file)

def clean(data):
    ''' Cleaning data for easy usage '''
    D = []
    for i in data:
        i = i.replace("+","").replace("-","").replace(",","")
        if i == "":
            i = "0"
        D.append(i.strip())
    return D

while num < len(country):
    ''' Getting information by country '''
    try:
        # request to the page
        html = req.get(link)
    except req.exceptions.RequestException as e:
        print(e)
        continue

    # get information
    bs = BeautifulSoup(html.content, 'html.parser')
    search = bs.select('div tbody tr td')
    start = -1

    # search country
    for i in range(len(search)):
        if search[i].get_text().find(country[num]["name"]) != start:
            start = i
            break

    # search columns
    data = []
    for i in range(1,8):
        try:
            data += [search[start+i].get_text()]
        except:
            data += ["0"]
            pass
    
    data = clean(data)
    # assign cleaned data
    country[num]["infected"] = int(data[0])
    country[num]["new_cases"] = int(data[1])
    country[num]["total_deaths"] = int(data[2])
    num += 1

# creating a DataFrame
fig, ax = plt.subplots()
df = pd.DataFrame({
    'A': country[0][analize],
    'B': country[1][analize],
    'C': country[2][analize]
}, index=[analize])
df.plot(kind="bar", ax=ax)

# putting legends
ax.legend([
    "{} {:,d}".format(country[0]["code"], country[0][analize]),
    "{} {:,d}".format(country[1]["code"], country[1][analize]),
    "{} {:,d}".format(country[2]["code"], country[2][analize])
])

# saving graph and showing it
plt.savefig("graph.png")
plt.show()