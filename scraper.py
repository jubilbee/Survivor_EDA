import requests
from bs4 import BeautifulSoup
from io import StringIO
import difflib
import pandas as pd
import os
import functions as f

# Starting with the contestants table, I scrape the wikipedia page for Survivor contestants, and save it to a pandas Dataframe
# contestant table
URL = "https://en.wikipedia.org/wiki/List_of_Survivor_(American_TV_series)_contestants"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table', class_='wikitable')
# I use StringIO to avoid the FutureWarning about read_html passing literal html being deprecated
contestant_table = pd.read_html(StringIO(str(tables)))
contestant_table = pd.concat(contestant_table, axis=0).reset_index(drop=True)

# Run get_gender function for Male and Female contestants, combine into one dictionary using ** operator
female_dict = f.get_gender('https://survivor.fandom.com/wiki/Category:Female_Contestants', 'F')
male_dict = f.get_gender('https://survivor.fandom.com/wiki/Category:Male_Contestants', 'M')
gender_dict = {**male_dict, **female_dict}

# Manually replaces what names won't be replaced with find_closest_match   
contestant_table.replace({'Jon "Jonny Fairplay" Dalton': 'Jon Dalton',
            'Leon Joseph "LJ" McKanas': 'LJ McKanas', 
            'Evelyn "Evvie" Jagoda': 'Evvie Jagoda', 
            'Janani "J. Maya" Krishnan-Jha': 'J. Maya',
            'Solomon "Sol" Yi': 'Sol Yi',
            'Christine "Teeny" Chirichillo': 'Teeny Chirichillo',
            'Kimberly "Kim" Powers': 'Kim Powers',
            'Robert "The General" DeCanio': 'Robert DeCanio',
            'Cassandra "Angie" Jakusz': 'Angie Jakusz',
            'Virgilio "Billy" Garcia': 'Billy Garcia',
            'John Paul "J.P." Calderon': 'J.P. Calderon',
            'Anh-Tuan "Cao Boi" Bui': 'Cao Boi Bui',
            'Bradley "Brad" Virata': 'Brad Virata',
            'Rebekah "Becky" Lee': 'Becky Lee',
            'Alejandro "Alex" Angarita': 'Alex Angarita',
            'Kenward "Boo" Bernis': 'Boo Bernis',
            'Michael "Mikey B" Bortone': 'Michael Bortone',
            'Danny "GC" Brown': 'GC Brown',
            'Jessica "Sugar" Kiper': 'Sugar Kiper',
            'Jesusita "Susie" Smith': 'Susie Smith',
            'Benjamin "Coach" Wade': 'Coach Wade',
            'James "J.T." Thomas, Jr.': 'JT Thomas, Jr.',
            'Elizabeth "Liz" Kim': 'Liz Kim',
            'Yvette "Yve" Rojas': 'Yve Rojas',
            'Mark "Papa Bear" Caruso': 'Mark Caruso',
            'Roxanne "Roxy" Morris': 'Roxy Morris',
            'Edward "Eddie" Fox': 'Eddie Fox',
            'Latasha "Tasha" Fox': 'Tasha Fox',
            'Elisabeth "Liz" Markahm': 'Liz Markham',
            'Ciandre "CeCe" Taylor': 'CeCe Taylor',
            'Alexandrea "Ali" Elliott': 'Ali Elliott',
            'John Paul "JP" Hilsabeck': 'JP Hilsabeck',
            '''Tra'mese "Missy" Byrd''': 'Missy Byrd',
            'Shantel "Shan" Smith': 'Shan Smith',
            'Michael "Mike" Turner': 'Mike Turner',
            'Elisabeth "Elie" Scott': 'Elie Scott',
            'Nicholas "Sifu" Alsup': 'Sifu Alsup',
            'Jessica "Jess" Chong': 'Jess Chong',
            'Quintavius "Q" Burdette': 'Q Burdette',
            'Terran "TK" Foster': 'TK Foster',
            'James "Jim" Lynch': 'Jim Lynch',
            'Elisabeth "Liz" Markham': 'Liz Markham',
            'Charlotte "So" Kim': 'So Kim',
            'Amber Brkich' : 'Amber Mariano'
            }, inplace=True)
# Run closest match function for contestant table by using .apply to apply it to each column value.
contestant_table['Name'] = contestant_table['Name'].apply(lambda name: f.find_closest_match(name, gender_dict))

# List of urls to use with get_ethnicity() function
URLS = [
    "https://survivor.fandom.com/wiki/Category:African-American_Contestants",
    "https://survivor.fandom.com/wiki/Category:African-Canadian_Contestants",
    "https://survivor.fandom.com/wiki/Category:Asian-American_Contestants",
    "https://survivor.fandom.com/wiki/Category:Asian-Canadian_Contestants",
    "https://survivor.fandom.com/wiki/Category:Latin_American_Contestants",
]
f.get_ethnicity(URLS, contestant_table)

# Fills any null values in the 'Ethnicity' column
contestant_table['Ethnicity'] = contestant_table['Ethnicity'].fillna('White')

# Add genders from the previously created gender_dict to the 'Gender' column, using map() to match names in contestant_table 'Name' column to the names in gender_dict
contestant_table['Gender'] = contestant_table['Name'].map(gender_dict)
# Manually fill in the genders of nonbinary contestants, since they weren't in the gender_dict
contestant_table.loc[contestant_table['Name'] == 'Teeny Chirichillo', 'Gender'] = 'N'
contestant_table.loc[contestant_table['Name'] == 'Evvie Jagoda', 'Gender'] = 'N'

# Calling the get_lgbt() function
f.get_lgbt('https://survivor.fandom.com/wiki/Category:LGBT_Contestants', contestant_table)

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

# Call has_disability() function
f.has_disability('https://survivor.fandom.com/wiki/Category:Disabled_Contestants', contestant_table) 

# Now we call the stats function to create the Dataframe
stats_table = f.stats()

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

# Some of the pages used to create the stats table were missing column names, resulting in different columns being appended to the multi index
# I handled this by copying values from duplicate columns over to original column (where value is null) 
if stats_table[('Overall scores', 'SurvSc')].isnull().any():
    stats_table.loc[stats_table[('Overall scores', 'SurvSc')].isnull(), ('Overall scores', 'SurvSc')] = stats_table[('Unnamed: 1_level_0', 'SurvSc')]

if stats_table[('Overall scores', 'SurvAv')].isnull().any():
    stats_table.loc[stats_table[('Overall scores', 'SurvAv')].isnull(), ('Overall scores', 'SurvAv')] = stats_table[('Unnamed: 2_level_0', 'SurvAv')]

if stats_table[('Unnamed: 0_level_0', 'Contestant')].isnull().any():
    stats_table.loc[stats_table[('Unnamed: 0_level_0', 'Contestant')].isnull(), ('Unnamed: 0_level_0', 'Contestant')] = stats_table[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')]

if stats_table[('Challenge stats', 'ChW%')].isnull().any():
    stats_table.loc[stats_table[('Challenge stats', 'ChW%')].isnull(), ('Challenge stats', 'ChW%')] = stats_table[('Challenge stats', 'ChW.1')]
# With the values copied to the correct columns, I drop the duplicate columns
stats_table.drop(('Unnamed: 1_level_0', 'SurvSc'), axis = 1, inplace=True)
stats_table.drop(('Unnamed: 2_level_0', 'SurvAv'), axis = 1, inplace=True)
stats_table.drop(('Unnamed: 0_level_0', 'Unnamed: 0_level_1'), axis = 1, inplace=True)
stats_table.drop(('Challenge stats', 'ChW.1'), axis = 1, inplace=True)

# Call the flatten_index function
f.flatten_index(stats_table)

# most idols table
idols = f.create_tables('https://truedorktimes.com/survivor/boxscores/idolsfound-season.htm')
# advantages - (only through season 40) 
advantages = f.create_tables('https://truedorktimes.com/survivor/boxscores/advantages.htm')
# individual immunity wins
immunity = f.create_tables('https://truedorktimes.com/survivor/boxscores/icwin.htm')

# Write all the tables I've created to csv files by calling the function create_csv
f.create_csv(contestant_table, 'csv_files/contestants.csv')
f.create_csv(stats_table, 'csv_files/stats.csv')
f.create_csv(idols, 'csv_files/idols.csv') 
f.create_csv(advantages, 'csv_files/advantages.csv')
f.create_csv(immunity, 'csv_files/immunities.csv')
