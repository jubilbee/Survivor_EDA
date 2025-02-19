import requests
from bs4 import BeautifulSoup
from io import StringIO
import difflib
import pandas as pd
import os

# season overview table
URL = "https://en.wikipedia.org/wiki/Survivor_(American_TV_series)"
page = requests.get(URL)
soup  = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table', class_='wikitable')
table = tables[0]

season_table = pd.read_html(StringIO(str(table)))
season_table = pd.concat(season_table, axis=0).reset_index(drop=True)

# contestant table
URL = "https://en.wikipedia.org/wiki/List_of_Survivor_(American_TV_series)_contestants"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table', class_='wikitable')

contestant_table = pd.read_html(StringIO(str(tables)))
contestant_table = pd.concat(contestant_table, axis=0).reset_index(drop=True)

season_table.loc[season_table['Subtitle'] == 'Borneo[c]', 'Subtitle'] = 'Borneo'
# Function to create dictionaries of contestants with the same gender
def get_gender(main, gender):
    """
    
    """
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
# Run function for Male and Female contestants, combine into one dictionary
female_dict = get_gender('https://survivor.fandom.com/wiki/Category:Female_Contestants', 'F')
male_dict = get_gender('https://survivor.fandom.com/wiki/Category:Male_Contestants', 'M')
gender_dict = {**male_dict, **female_dict}
# Function to look for close name matches in the gender dictionary and contestant table, and replaces contestant table values with the gender dictionary values 
def find_closest_match(name, gender_dict, threshold=0.6):
    """
    
    """
    closest_matches = difflib.get_close_matches(name, gender_dict.keys(), n=1, cutoff=threshold)
    if not closest_matches:
        return name
    else:
        return closest_matches[0] # Pytest to double check that the names match up? Maybe

# Manually replaces what names won't be able to be replaced with find_closest_match    
contestant_table.replace('Jon "Jonny Fairplay" Dalton', 'Jon Dalton', inplace=True)        
contestant_table.replace('Leon Joseph "LJ" McKanas', 'LJ McKanas', inplace=True)
contestant_table.replace('Evelyn "Evvie" Jagoda', 'Evvie Jagoda', inplace=True)
contestant_table.replace('Janani "J. Maya" Krishnan-Jha', 'J. Maya', inplace=True)
contestant_table.replace('Solomon "Sol" Yi', 'Sol Yi', inplace=True)
contestant_table.replace('Christine "Teeny" Chirichillo', 'Teeny Chirichillo', inplace=True)
# Run closest match function for contestant table and Winner/ Runners up columns of season table
contestant_table['Name'] = contestant_table['Name'].apply(lambda name: find_closest_match(name, gender_dict, threshold=0.6))
season_table['Winner'] = season_table['Winner'].apply(lambda name: find_closest_match(name, gender_dict, threshold=0.6))
season_table['Runner(s)-up'] = season_table['Runner(s)-up'].apply(lambda name: find_closest_match(name, gender_dict, threshold=0.6))
season_table['Runner(s)-up.1'] = season_table['Runner(s)-up.1'].apply(lambda name: find_closest_match(name, gender_dict, threshold=0.6))
# Function to fill Ethnicity column in contestant table with data from list of urls
def get_ethnicity(URLS):
    """
    
    """
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

# Function to fill lgbt column in contestant table with True or False values based on url containing a list of lgbt contestants
def get_lgbt(main):
    """
    
    """
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
    contestant_table['Lgbt'] = contestant_table['Name'].map(lgbt_dict)
    return lgbt_dict
get_lgbt('https://survivor.fandom.com/wiki/Category:LGBT_Contestants')

# Manually replaces season names in contestant table with their season number
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
# function to fill a disability column in contestant table with True or False values
def has_disability(url):
    """
    
    """
    disabled_dict = {name: False for name in contestant_table['Name']}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='category-page__members')
    names = results.find_all('li', class_='category-page__member')
    for name in names:
        name = name.find('a', class_='category-page__member-link').text.strip()
        disabled_dict[name] = True
    contestant_table['Has Disability'] = contestant_table['Name'].map(disabled_dict)
    return disabled_dict
has_disability('https://survivor.fandom.com/wiki/Category:Disabled_Contestants') # <- add to contestant table, same as lgbt - a bool

# Creates a contestants stats table by iterating over various urls per season
def stats(): # need to add season column?
    """

    """
    seasons = 48
    all_stats = []
    # iterate over season urls
    for season in range(1, seasons + 1):
        url = f'https://www.truedorktimes.com/survivor/boxscores/s{season}.htm'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tables = soup.find('table')
        stats_table = pd.read_html(StringIO(str(tables)))[0]
        stats_table['Unnamed: 0_level_0','Season'] = season
        # find contestant name attributes
        name_links = soup.find_all('tr', class_='score')
        contestant_names = []
        for i in range(len(stats_table)):
            try:
                name = name_links[i]
                a_tag = name.find('a')
                if a_tag:
                    href = a_tag['href']
                    contestant_name = href.split('/')[-1].split('.')[0]
                    contestant_name = contestant_name.replace('_', ' ').title()
                else:
                    contestant_name = stats_table.loc[i, ('Unnamed: 0_level_0', 'Contestant')]
            except (IndexError, KeyError):
                contestant_name = stats_table.loc[i, ('Unnamed: 0_level_0', 'Contestant')]
            contestant_names.append(contestant_name)
        if ('Unnamed: 0_level_0', 'Contestant') in stats_table.columns:
            stats_table[('Unnamed: 0_level_0', 'Contestant')] = pd.Series(contestant_names)
        all_stats.append(stats_table)
    stats = pd.concat(all_stats, axis=0).reset_index(drop=True)
    return stats # used AI to help troubleshoot this function. (may add info on this in docstring)

stats_table = stats()
# Manually replaces names that couldn't be handled when making stats table, with their full name
stats_table.replace({
    'Colby': 'Colby Donaldson',
    'Tina': 'Tina Wesson',
    'Keith': 'Keith Famie',
    'Nick': 'Nick Brown',
    'Jerri': 'Jerri Manthey',
    'Skupin*': 'Michael Skupin',
    'Mitchell': 'Mitchell Olson',
    'Jeff V': 'Jeff Varner',
    'Alicia': 'Alicia Calaway',
    'Elisabeth': 'Elisabeth Filarski',
    'Amber': 'Amber Mariano',
    'Rodger': 'Rodger Bingham',
    'Kimmi': 'Kimmi Kappenberg',
    'Maralyn': 'Maralyn Hershey',
    'Kel': 'Kel Gleason',
    'Debb': 'Debb Eaton',
    'Austin': 'Austin Li Coon',
    'Dee': 'Dee Valladares',
    'Emily': 'Emily Flippen',
    'Bruce': 'Bruce Perreault',
    'Katurah': 'Katurah Topps',
    'J.Maya': 'J. Maya',
    'Drew': 'Drew Basile',
    'Julie': 'Julie Alley',
    'Kellie': 'Kellie Nalbandian',
    'Kaleb': 'Kaleb Gebrewold',
    'Sifu': 'Sifu Alsup',
    'Jake': "Jake O'Kane",
    'Sean': 'Sean Edwards',
    'Kendra': 'Kendra McQuarrie',
    'Brando': 'Brando Meyer',
    'Sabiyah': 'Sabiyah Broderick',
    'Brandon': 'Brandon Donlon',
    'Hannah': 'Hannah Rose'
}, inplace=True)

# Copy values from duplicate columns over to original column (where value is null) 
if stats_table[('Overall scores', 'SurvSc')].isnull().any():
    stats_table.loc[stats_table[('Overall scores', 'SurvSc')].isnull(), ('Overall scores', 'SurvSc')] = stats_table[('Unnamed: 1_level_0', 'SurvSc')]

if stats_table[('Overall scores', 'SurvAv')].isnull().any():
    stats_table.loc[stats_table[('Overall scores', 'SurvAv')].isnull(), ('Overall scores', 'SurvAv')] = stats_table[('Unnamed: 2_level_0', 'SurvAv')]

if stats_table[('Unnamed: 0_level_0', 'Contestant')].isnull().any():
    stats_table.loc[stats_table[('Unnamed: 0_level_0', 'Contestant')].isnull(), ('Unnamed: 0_level_0', 'Contestant')] = stats_table[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')]

if stats_table[('Challenge stats', 'ChW%')].isnull().any():
    stats_table.loc[stats_table[('Challenge stats', 'ChW%')].isnull(), ('Challenge stats', 'ChW%')] = stats_table[('Challenge stats', 'ChW.1')]
# Drop unnecessary/ duplicate columns
stats_table.drop(('Unnamed: 1_level_0', 'SurvSc'), axis = 1, inplace=True)
stats_table.drop(('Unnamed: 2_level_0', 'SurvAv'), axis = 1, inplace=True)
stats_table.drop(('Unnamed: 0_level_0', 'Unnamed: 0_level_1'), axis = 1, inplace=True)
stats_table.drop(('Challenge stats', 'ChW.1'), axis = 1, inplace=True)
# Flatten stats multiindex to single index
# Used ai to help get multiindex flattened, as droplevel was throwing a ValueError
stats_table.columns = [col[1] if isinstance(col, tuple) else col for col in stats_table.columns]


# most idols table
page = requests.get('https://truedorktimes.com/survivor/boxscores/idolsfound-season.htm')
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all('table')
idols = pd.read_html(StringIO(str(tables)))
idols = pd.concat(idols, axis=0).reset_index(drop=True)

# advantages - (only through season 40) 
page = requests.get('https://truedorktimes.com/survivor/boxscores/advantages.htm')
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all('table')
advantages = pd.read_html(StringIO(str(tables)))
advantages = pd.concat(advantages, axis=0).reset_index(drop=True)

#  individual immunity wins
page = requests.get('https://truedorktimes.com/survivor/boxscores/icwin.htm')
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all('table')
immunity = pd.read_html(StringIO(str(tables)))
immunity = pd.concat(immunity, axis=0).reset_index(drop=True)

# contestants, seasons, stats (idols, advantages, indiv. immunities)
def create_csv(df, file):
    """
    
    """
    if os.path.exists(file):
        return print(f'{file} already exists.')
    else:
        df.to_csv(file, index=False)
        print(f'{file} has been created.')
    return
seasons = create_csv(season_table, 'seasons.csv')
contestants = create_csv(contestant_table, 'contestants.csv')
stats = create_csv(stats_table, 'stats.csv')
idols = create_csv(idols, 'idols.csv') # Note - Manually added values in that were left off initial table
advantages = create_csv(advantages, 'advantages.csv')
immunities = create_csv(immunity, 'immunities.csv')
