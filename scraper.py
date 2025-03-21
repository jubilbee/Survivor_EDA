import requests
from bs4 import BeautifulSoup
from io import StringIO
import difflib
import pandas as pd
import os

# Starting with the contestants table, I scrape the wikipedia page for Survivor contestants, and save it to a pandas Dataframe
# contestant table
URL = "https://en.wikipedia.org/wiki/List_of_Survivor_(American_TV_series)_contestants"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table', class_='wikitable')
# I use StringIO to avoid the FutureWarning about read_html passing literal html being deprecated
contestant_table = pd.read_html(StringIO(str(tables)))
contestant_table = pd.concat(contestant_table, axis=0).reset_index(drop=True)

# Function to create dictionaries of contestants with the same gender
def get_gender(main:str, gender:str) -> dict:
    """
    Takes url and scrapes contestant names, outputs names and input gender into a dictionary.
    
    Args:
        main (str): The url to be iterated through
        gender (str): The corresponding gender for contestants names being scraped
    Returns:
        dict: A dictionary of contestant names and their corresponding gender
    """
    # Starting with an empty dictionary and a variable with a null value
    gender_dict = {}
    contestants = None
    while True:
        # If the contestants variable is not null, the url will be set to contestants value, otherwise url will be main
        if contestants:
            url = contestants
        else:
            url = main
        # Webscraping to find all list elements with category-page__member, this is where the contestant names are.
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('div', class_='category-page__members')
        names = results.find_all('li', class_='category-page__member')
        # Go through each list element and find the hyperlink text, strip the text to get contestant name, then assign the gender to each name
        for name in names:
            name = name.find('a', class_='category-page__member-link').text.strip()
            gender_dict[name] = gender
        # Find the hyperlink element for next page
        contestant_links = soup.find('a', class_='category-page__pagination-next wds-button wds-is-secondary')
        # If next page exists, get the href and set that as the value for contestants. This way the code loops through the pages until there are no more
        if contestant_links:
            contestants = contestant_links.get('href')
        else:
            break
    return gender_dict
# Run get_gender function for Male and Female contestants, combine into one dictionary using ** operator
female_dict = get_gender('https://survivor.fandom.com/wiki/Category:Female_Contestants', 'F')
male_dict = get_gender('https://survivor.fandom.com/wiki/Category:Male_Contestants', 'M')
gender_dict = {**male_dict, **female_dict}
# Function to look for close name matches in the gender dictionary and contestant table, and replaces contestant table values with the gender dictionary values 
def find_closest_match(name:str, name_dict:dict, threshold=0.7) -> str:
    """
    Use difflib's get_close_matches to compare and replace contestant names with names in a dictionary of names.

    Args:
        name (str): The named to be matched
        name_dict (dict): A dictionary full of names to match against 
        threshold (float): Similarity threshold for matching the names. Set to a default of 0.7
    Returns:
        str: Returns either the closest match from name_dict, or the original name if no close matches were found.
    """
    # Creates a list of closest matches for a name using difflib, returning only the closest match (n=1). 
    closest_matches = difflib.get_close_matches(name, name_dict.keys(), n=1, cutoff=threshold)
    # If no close matches are found, return the name as is
    if not closest_matches:
        return name
    else:
        return closest_matches[0] 

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
contestant_table['Name'] = contestant_table['Name'].apply(lambda name: find_closest_match(name, gender_dict))

# Function to fill Ethnicity column in contestant table with data from list of urls
def get_ethnicity(URLS: list):
    """
    Iterates through a list of urls, creating a dictionary of names and their ethnicity, 
    then adds the ethnicity to a column in contestants table by mapping the names in the dictionary to the Name column

    Args:
        URLS (list): A list of urls to iterate through
    Returns:
        None: The function updates the Dataframe contestant_table's 'Ethnicity' column
    """
    ethnicity_dict = {}
    # Iterates through each url in the list, scraping the ethnicity and contestant names from each.
    for URL in URLS:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Finds the header for each url, then strips it down to just the ethnicity (ie 'African American Contestants' becomes 'African American')
        ethnicities = soup.find('h1', class_='page-header__title')
        ethnicity = ethnicities.text.strip()[:-12]
        # Finds all list elements withing the webpage
        results = soup.find('div', class_='category-page__members')
        names = results.find_all('li', class_='category-page__member')
        # For each name in the list, finds the hyperlink text and strips it down to plain text, then adds the ethnicity and name to a dictionary
        for name in names:
            name = name.find('a', class_='category-page__member-link').text.strip()
            ethnicity_dict[name] = ethnicity
    # Adds the ethnicities to 'Ethnicity' column, using map() to match names in the contestant_table column 'Name' to the names in the dictionary
    contestant_table['Ethnicity'] = contestant_table['Name'].map(ethnicity_dict)
    return
# List of urls to use with get_ethnicity() function
URLS = [
    "https://survivor.fandom.com/wiki/Category:African-American_Contestants",
    "https://survivor.fandom.com/wiki/Category:African-Canadian_Contestants",
    "https://survivor.fandom.com/wiki/Category:Asian-American_Contestants",
    "https://survivor.fandom.com/wiki/Category:Asian-Canadian_Contestants",
    "https://survivor.fandom.com/wiki/Category:Latin_American_Contestants",
]

get_ethnicity(URLS)
# Fills any null values in the 'Ethnicity' column
contestant_table['Ethnicity'] = contestant_table['Ethnicity'].fillna('White')

# Add genders from the previously created gender_dict to the 'Gender' column, using map() to match names in contestant_table 'Name' column to the names in gender_dict
contestant_table['Gender'] = contestant_table['Name'].map(gender_dict)
# Manually fill in the genders of nonbinary contestants, since they weren't in the gender_dict
contestant_table.loc[contestant_table['Name'] == 'Teeny Chirichillo', 'Gender'] = 'N'
contestant_table.loc[contestant_table['Name'] == 'Evvie Jagoda', 'Gender'] = 'N'

# Function to fill lgbt column in contestant table with True or False values based on url containing a list of lgbt contestants
def get_lgbt(main:str):
    """
    Stores names into a dictionary using the 'Name' column from the Dataframe contestant_table. 
    Assigns the names True or False values depending on if the name appears in the url or not.
    Adds the True or False values from the dictionary to the contestant_table column 'Lgbt'

    Args:
        main (str): Initial url to iterate through
    Returns:
        None: Updates the Dataframe contestant_table's 'Lgbt' column with boolean values
    """
    # First I will create the dictionary, using names in contestant_table['Name'] as the key, and filling the values with False as the default
    lgbt_dict = {name: False for name in contestant_table['Name']}
    contestants = None
    # The process for iterating through webpages here is very similar to in the get_gender() function
    while True:
        # If the contestants variable is not null, set it as the value for the url, otherwise url will equal main
        if contestants:
            url = contestants
        else:
            url = main
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Find all list elements on the webpage that contestant names are stored in
        results = soup.find('div', class_='category-page__members')
        names = results.find_all('li', class_='category-page__member')
        # Going through each name, strip the text and change the value for name's key to True
        for name in names:
            name = name.find('a', class_='category-page__member-link').text.strip()
            lgbt_dict[name] = True
        # Find the next page button/ hyperlink
        contestant_links = soup.find('a', class_='category-page__pagination-next wds-button wds-is-secondary')
        # If there is a next page, set the contestants variable to the next pages href/link so we continue looping through pages
        if contestant_links:
            contestants = contestant_links.get('href')
        else:  
            break
    # Add the values in the lgbt_dict to contestant_table's Lgbt column, using map()
    contestant_table['Lgbt'] = contestant_table['Name'].map(lgbt_dict)
    return 
# Running the get_lgbt() function
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
def has_disability(url:str):
    """
    Creates a dictionary of names using the 'Name' column of the Dataframe contestant_table.
    Webscrapes contestant names from a url, and assigns them a True value into the dictionary.
    Adds the values from the dictionary to the contestant_table column 'Has Disability'

    Args:
        url (str): The url of the webpage to be scraped
    Returns:
        None: Adds values from disabled_dict to the 'Has Disability' column in contestant_table
    """
    # This function works the same as get_lgbt(), except the webpage for contestants with disabilities doesn't have multiple pages to iterate through
    # Create dictionary of names from contestant_table's 'Name' column 
    disabled_dict = {name: False for name in contestant_table['Name']}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Find all list elements on the webpage that contestant names are stored in
    results = soup.find('div', class_='category-page__members')
    names = results.find_all('li', class_='category-page__member')
    # Going through each name, strip the text and change the value for name's key to True
    for name in names:
        name = name.find('a', class_='category-page__member-link').text.strip()
        disabled_dict[name] = True
    # Add the values in disabled_dict to contestant_table's 'Has Disability' column, using map()
    contestant_table['Has Disability'] = contestant_table['Name'].map(disabled_dict)
    return 
# Call has_disability() function
has_disability('https://survivor.fandom.com/wiki/Category:Disabled_Contestants') 

# Creates a contestants stats table by iterating over various urls per season
# AI was used here, the code I had initially for the following two functions seemed to work, but upon further examining the .csv file after running everything, it was misaligned, skipping some rows and then incorrectly replacing the following rows
# I also was having issues with specific pages being iterated through not having the same html elements as other pages, such as some missing hyperlinks for contestant names
def extract_contestant_names(soup:BeautifulSoup, season:int) -> list:
    """
    Extracts contestant names from the HTML content of a given Survivor season.

    Note: This function was written with AI assistance. 

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content.
        season (int): The Survivor season number.
    Returns:
        list: List of contestant names extracted
    """
    # First, find all tables, since the pages being scraped from generally have 2, but we only want data from the first
    tables = soup.find_all('table')
    # In the html used for the stats table, the names of contestants were stored in table row elements
    if tables:
        # Ensure only the first table is being used, and search for the table row elements
        name_links = tables[0].find_all('tr', class_='score')
    else:
        name_links = []
    # We create an empty list that will be used to store contestant names
    contestant_names = []
    # Loops through each element in name_links, pairing each element to an index
    for i, name in enumerate(name_links):
        # Skip header rows - this should fix the misalignment issues that I was struggling with
        if name.find('th'):
            continue
        # Find the a element for each name_link name
        a_tag = name.find('a')
        # If there is an a element, get the href, and then split and clean it to get only the contestant name, storing it in the list
        if a_tag:
            href = a_tag['href']
            contestant_name = href.split('/')[-1].split('.')[0]
            contestant_name = contestant_name.replace('_', ' ').title()
        # If there is no a element found, instead find the td element, and strip that to plain text and storing in the list 
        else:
            # Fallback: Extract text directly from the td element
            td_tag = name.find('td')
            contestant_name = td_tag.get_text().strip() if td_tag else None
        # Update the list of contestant names 
        contestant_names.append(contestant_name)
        
    return contestant_names
# The next function handles extracting the entire stats table, while also ensuring that the contestant names are added to the table without error
def stats() -> pd.DataFrame:
    """
    Creates the Dataframe 'stats' by iterating through and scraping webpages using BeautifulSoup

    Note: This function was written with AI assistance

    Args:
        None
    Returns:
        Dataframe: The Dataframe the stats data is stored in
    """
    # The website we're pulling from here has a different stats page for each season, so we define the number of seasons to iterate through
    seasons = 48
    all_stats = []
    # Starting with season one we loop through a range of all the seasons
    for season in range(1, seasons + 1):
        # I set the url to change the season number through the iterations, as that is the only change for each page
        url = f'https://www.truedorktimes.com/survivor/boxscores/s{season}.htm'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        tables = soup.find('table')
        stats_table = pd.read_html(StringIO(str(tables)))[0]
        # I create a column to list the season for each row, as some contestants appear in multiple seasons
        stats_table['Unnamed: 0_level_0','Season'] = season

        # Extract contestant names using helper function
        contestant_names = extract_contestant_names(soup, season)
               
        # Goes through each name in contestant_names list, only keeping list items that aren't null
        contestant_names = [name for name in contestant_names if name]
        # Adding a check to raise an error if contestant_names and stats_table are not the same length
        if len(contestant_names) != len(stats_table):
            raise ValueError(f"Length mismatch: contestant_names ({len(contestant_names)}) vs stats_table ({len(stats_table)})")
        # Assign extracted names to the stats table
        stats_table['Unnamed: 0_level_0','Contestant'] = pd.Series(contestant_names)
        #Append stats_table to all_stats
        all_stats.append(stats_table)
    # Concatenate all_stats to Dataframe stats
    stats = pd.concat(all_stats, axis=0).reset_index(drop=True)
    return stats # END OF - AI ASSISTED CODE
# Now we call the stats function to create the Dataframe
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

# Flatten stats multiindex to single index
# Used ai to help get multiindex flattened, as droplevel was throwing a ValueError
def flatten_index():
    """
    Flattens the multi-level (tuple) columns for Dataframe stats_table to a single level by keeping only the second level column names
    
    Note: AI assistance used for this code
    """
    # Keeps the second column names if column is also a tuple, otherwise keeps column name as is
    stats_table.columns = [col[1] if isinstance(col, tuple) else col for col in stats_table.columns]
    return
flatten_index()

# Taking urls from truedorktimes, I scrape to create 3 more tables. Since they all have the same html structure, I create a function to scrape the data
def create_tables(url:str) -> pd.DataFrame:
    """
    Scrapes data from given url and creates a Dataframe with that data

    Args:
        url(str): The url to be scraped
    Returns:
        DataFrame: The pd.DataFrame the webscraped data is stored in
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table')
    table = pd.read_html(StringIO(str(tables)))
    table = pd.concat(table, axis=0).reset_index(drop=True)
    return table
# most idols table
idols = create_tables('https://truedorktimes.com/survivor/boxscores/idolsfound-season.htm')
# advantages - (only through season 40) 
advantages = create_tables('https://truedorktimes.com/survivor/boxscores/advantages.htm')
# individual immunity wins
immunity = create_tables('https://truedorktimes.com/survivor/boxscores/icwin.htm')

# Finally, I create a function to write my tables to csv files.
def create_csv(df:pd.DataFrame, file:str) -> str:
    """
    Checks if the file already exists, if not, writes the dataframe to file.

    Args:
        df (pd.Dataframe): Pandas table created through webscraping
        file (str): Desired name of .csv file to write the dataframe to.

    Returns:
        str: Print statement either declaring the .csv file has been created, or that it already exists
    """
    # If the path for the desired .csv already exists on the os, prints a statement telling the user the file already exists
    if os.path.exists(file):
        return print(f'{file} already exists.')
    else:
        # if the file doesn't exist, writes the dataframe to csv, then prints a statement telling user the file has been created
        df.to_csv(file, index=False)
        return print(f'{file} has been created.')
# Write all the tables I've created to csv
create_csv(contestant_table, 'contestants.csv')
create_csv(stats_table, 'stats.csv')
create_csv(idols, 'idols.csv') 
create_csv(advantages, 'advantages.csv')
create_csv(immunity, 'immunities.csv')
