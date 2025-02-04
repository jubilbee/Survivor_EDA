import requests
from bs4 import BeautifulSoup
from io import StringIO
import difflib
import pandas as pd

#season overview table
URL = "https://en.wikipedia.org/wiki/Survivor_(American_TV_series)"
page = requests.get(URL)
soup  = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table', class_='wikitable')
table = tables[0]

season_table = pd.read_html(StringIO(str(table)))
season_table = pd.concat(season_table, axis=0).reset_index(drop=True)

# Should I turn these into functions? And call them in j notebook, or should i write to csv at end
#contestant table
URL = "https://en.wikipedia.org/wiki/List_of_Survivor_(American_TV_series)_contestants"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table', class_='wikitable')

contestant_table = pd.read_html(StringIO(str(tables)))
contestant_table = pd.concat(contestant_table, axis=0).reset_index(drop=True)

season_table.loc[season_table['Subtitle'] == 'Borneo[c]', 'Subtitle'] = 'Borneo'

def get_gender(main, gender):
    gender_dict = {}
    contestants = None
    while True:
        if contestants:
            url = contestants
        else:
            url = main
        #print("Fetching URL:", url) # Debug
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('div', class_='category-page__members')
        names = results.find_all('li', class_='category-page__member')
        for name in names:
            name = name.find('a', class_='category-page__member-link').text.strip()
            gender_dict[name] = gender
        contestant_links = soup.find('a', class_='category-page__pagination-next wds-button wds-is-secondary')
        if contestant_links:
            contestants = contestant_links.get('href')
            #print("Next page URL:", contestants) # Debug
        else:
            break
    return gender_dict

female_dict = get_gender('https://survivor.fandom.com/wiki/Category:Female_Contestants', 'F')
male_dict = get_gender('https://survivor.fandom.com/wiki/Category:Male_Contestants', 'M')
gender_dict = {**male_dict, **female_dict}

def find_closest_match(name, gender_dict, threshold=0.6):
    closest_matches = difflib.get_close_matches(name, gender_dict.keys(), n=1, cutoff=threshold)
    if not closest_matches:
        return name
    else:
        return closest_matches[0] 
    
contestant_table.replace('Jon "Jonny Fairplay" Dalton', 'Jon Dalton', inplace=True)        
contestant_table.replace('Leon Joseph "LJ" McKanas', 'LJ McKanas', inplace=True)
contestant_table.replace('Evelyn "Evvie" Jagoda', 'Evvie Jagoda', inplace=True)
contestant_table.replace('Janani "J. Maya" Krishnan-Jha', 'J. Maya', inplace=True)
contestant_table.replace('Solomon "Sol" Yi', 'Sol Yi', inplace=True)
contestant_table.replace('Christine "Teeny" Chirichillo', 'Teeny Chirichillo', inplace=True)

contestant_table['Name'] = contestant_table['Name'].apply(lambda name: find_closest_match(name, gender_dict, threshold=0.6))
season_table['Winner'] = season_table['Winner'].apply(lambda name: find_closest_match(name, gender_dict, threshold=0.6))
season_table['Runner(s)-up'] = season_table['Runner(s)-up'].apply(lambda name: find_closest_match(name, gender_dict, threshold=0.6))
season_table['Runner(s)-up.1'] = season_table['Runner(s)-up.1'].apply(lambda name: find_closest_match(name, gender_dict, threshold=0.6))

def get_ethnicity(URLS):
    ethnicity_dict = {}
    for URL in URLS:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        ethnicities = soup.find('h1', class_='page-header__title')
        ethnicity = ethnicities.text.strip()[:-12]
        results = soup.find('div', class_='category-page__members')
        names = results.find_all('li', class_='category-page__member')
        for name in names:
            name = name.find('a', class_='category-page__member-link').text.strip()
            ethnicity_dict[name] = ethnicity
    contestant_table['Ethnicity'] = contestant_table['Name'].map(ethnicity_dict)
    return
URLS = [
    "https://survivor.fandom.com/wiki/Category:African-American_Contestants",
    "https://survivor.fandom.com/wiki/Category:African-Canadian_Contestants",
    "https://survivor.fandom.com/wiki/Category:Asian-American_Contestants",
    "https://survivor.fandom.com/wiki/Category:Asian-Canadian_Contestants",
    "https://survivor.fandom.com/wiki/Category:Latin_American_Contestants",
]

get_ethnicity(URLS)
contestant_table['Ethnicity'] = contestant_table['Ethnicity'].fillna('White')

# Filling in nonbinary genders
contestant_table['Gender'] = contestant_table['Name'].map(gender_dict)
contestant_table.loc[contestant_table['Name'] == 'Teeny Chirichillo', 'Gender'] = 'N'
contestant_table.loc[contestant_table['Name'] == 'Evvie Jagoda', 'Gender'] = 'N'


def get_lgbt(main):
    lgbt_dict = {name: False for name in contestant_table['Name']}
    contestants = None
    while True:
        if contestants:
            url = contestants
        else:
            url = main
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('div', class_='category-page__members')
        names = results.find_all('li', class_='category-page__member')
        for name in names:
            name = name.find('a', class_='category-page__member-link').text.strip()
            lgbt_dict[name] = True
        contestant_links = soup.find('a', class_='category-page__pagination-next wds-button wds-is-secondary')
        if contestant_links:
            contestants = contestant_links.get('href')
        else:  
            break
    contestant_table['LGBT'] = contestant_table['Name'].map(lgbt_dict)
    return lgbt_dict
lgbt_dict = get_lgbt('https://survivor.fandom.com/wiki/Category:LGBT_Contestants')


contestant_table.replace({'Survivor: Borneo': 1, 
    'Survivor: The Australian Outback': 2,
    'Survivor: Africa': 3, 
    'Survivor: Marquesas': 4, 
    'Survivor: Thailand': 5, 
    'Survivor: The Amazon': 6, 
    'Survivor: Pearl Islands': 7,
    'Survivor: All-Stars': 8, 
    'Survivor: Vanuatu': 9, 
    'Survivor: Palau': 10, 
    'Survivor: Guatemala': 11,
    'Survivor: Panama': 12, 
    'Survivor: Cook Islands': 13, 
    'Survivor: Fiji': 14, 
    'Survivor: China': 15, 
    'Survivor: Micronesia': 16, 
    'Survivor: Gabon': 17, 
    'Survivor: Tocantins': 18, 
    'Survivor: Samoa': 19, 
    'Survivor: Heroes vs. Villains': 20, 
    'Survivor: Nicaragua': 21, 
    'Survivor: Redemption Island': 22, 
    'Survivor: South Pacific': 23, 
    'Survivor: One World': 24, 
    'Survivor: Philippines': 25, 
    'Survivor: Caramoan': 26, 
    'Survivor: Blood vs. Water': 27, 
    'Survivor: Cagayan': 28, 
    'Survivor: San Juan del Sur': 29, 
    'Survivor: Worlds Apart': 30, 
    'Survivor: Cambodia': 31, 
    'Survivor: Kaôh Rōng': 32, 
    'Survivor: Millennials vs. Gen X': 33, 
    'Survivor: Game Changers': 34, 
    'Survivor: Heroes vs. Healers vs. Hustlers': 35, 
    'Survivor: Ghost Island': 36, 
    'Survivor: David vs. Goliath': 37, 
    'Survivor: Edge of Extinction': 38, 
    'Survivor: Island of the Idols': 39, 
    'Survivor: Winners at War': 40}, inplace=True) #.infer_objects(copy=False) 



# Then webscrape new table on idols/ whatever ig?
# Have found a site with some tables on idol, advantage/disadvantage, immunity stats
# Determining whether to make add this info to the contestant table, or its own table
# If it's own table, probably need to find a way to convert the contestant name to the contestant tables index? (foreign key)




contestant_table