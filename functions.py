import requests
from bs4 import BeautifulSoup
from io import StringIO
import difflib
import pandas as pd
import os

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

# Function to fill Ethnicity column in contestant table with data from list of urls
def get_ethnicity(URLS: list, table:pd.DataFrame):
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
    table['Ethnicity'] = table['Name'].map(ethnicity_dict)
    return

# Function to fill lgbt column in contestant table with True or False values based on url containing a list of lgbt contestants
def get_lgbt(main:str, table:pd.DataFrame):
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
    lgbt_dict = {name: False for name in table['Name']}
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
    table['Lgbt'] = table['Name'].map(lgbt_dict)
    return 

# function to fill a disability column in contestant table with True or False values
def has_disability(url:str, table:pd.DataFrame):
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
    disabled_dict = {name: False for name in table['Name']}
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
    table['Has Disability'] = table['Name'].map(disabled_dict)
    return 

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

# Flatten stats multiindex to single index
# Used ai to help get multiindex flattened, as droplevel was throwing a ValueError
def flatten_index(table:pd.DataFrame):
    """
    Flattens the multi-level (tuple) columns for Dataframe stats_table to a single level by keeping only the second level column names
    
    Note: AI assistance used for this code
    """
    # Keeps the second column names if column is also a tuple, otherwise keeps column name as is
    table.columns = [col[1] if isinstance(col, tuple) else col for col in table.columns]
    return

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
    

# Jupyter Notebook - specific functions:

def clean_and_merge(advantages:pd.DataFrame, idols:pd.DataFrame, immunities:pd.DataFrame, stats:pd.DataFrame) -> pd.DataFrame:
    """
    Cleans tables for advantages, idols and immunities, then merges them to the stats table.

    Args:
        advantages(DataFrame): pd.DataFrame containing data on contestants who have found advantages
        idols(DataFrame): pd.DataFrame containing data on top contestants who have found immunity idols
        immunities(DataFrame): pd.DataFrame containing data on contestants who have won individual immunity challenges
        stats(DataFrame): pd.DataFrame consisting of data on contestants overall performance in the game
    Returns:
        DataFrame: Merges advantages, idols, and immunities Dataframes into the stats Dataframe
    """
    # first I create the variable final_stats and set it to equal stats, so that if the Jupyter Notebook is ran after the data is all cleaned and merged, it should just read the cleaned stats DataFrame
    final_stats = stats
    # since the Notes column should only exist in the stats DataFrame if everything is already merged, I use an if statement checking if it exists in columns, only running the code to clean and merge if Notes column is not in stats.
    if 'Notes' not in stats.columns:
            # Copy all data over from Contestant.1 column to the Contestant column for each dataset in preparation to drop the duplicated column
            idols['Contestant'] = idols['Contestant.1']  
            advantages['Contestant'] = advantages['Contestant.1'] 
            immunities['Contestant'] = immunities['Contestant.1']  

            # Next I drop unnecessary or duplicate columns from the dataset to be merged with stats
            advantages = advantages.drop(columns=['Rank', 'Contestant.1', 'VV', 'VFB', 'Tie broken?'])
            idols = idols.drop(columns=['Rank', 'Contestant.1'])
            immunities = immunities.drop(columns=['Rank', 'Contestant.1'])
                
            # strip and replace values (Season column of S, idols table of special characters (*,†/+,#))
            advantages['Season'] = advantages['Season'].str.replace('S', '')
            # replace all string versions of seasons with their corresponding number value
            advantages['Season'] = advantages['Season'].replace({
                    'Game Changers': 34,
                    'David vs. Goliath': 37,
                    'Winners at War': 40,
                    'Cambodia': 31,
                    'Island of the Idols': 39,
                    'HvHvH': 35,
                    'Worlds Apart': 30,
                    'Kaoh Rong': 32,
                    'Ghost Island': 36,
                    'urvivor 42': 42,
                    'Edge of Extinction': 38,
                    'MvGX': 33   
                })
            # change the advantages dataset Season column to an int datatype
            advantages['Season'] = advantages['Season'].astype(int) 

            # Next I make sure all of the row values are cleaned and ready to be switched to appropiate datatypes
            # There was a row in the idols column that did not represent a specific contestant so that was dropped
            idols = idols.drop(idols[idols['Season'].str.strip() == '--'].index)
            # Then strip down any special characters from rows where they were present, (and S from Season)
            idols['Season'] = idols['Season'].str.replace('S', '') 
            idols['Contestant'] = idols['Contestant'].str.rstrip('*').str.rstrip('#').str.rstrip('+')
            idols['IH'] = idols['IH'].str.rstrip('*').str.rstrip('#').str.rstrip('+')
            idols['IP'] = idols['IP'].str.rstrip('*').str.rstrip('#').str.rstrip('+')
            idols['VV'] = idols['VV'].str.rstrip('†').str.rstrip('#')

            # Change the idols columns to correct datatypes
            idols['IH'] = idols['IH'].astype(int)
            idols['IP'] = idols['IP'].astype(int)
            idols['VV'] = idols['VV'].astype(int)
            idols['Season'] = idols['Season'].astype(int)

            # Repeat the process of stripping columns and converting their datatypes with the immunites dataset
            immunities['Season'] = immunities['Season'].str.split(':').str[0]
            immunities['Season'] = immunities['Season'].str.strip('Survivor').str.strip('S')
            immunities['Season'] = immunities['Season'].astype(int)     
            
            # There were values in all of the .csv files for the dataframes being cleaned here that had double spaces instead of single space, which may have been causing issues with data merging over,so those were replaced 
            idols['Contestant'] = idols['Contestant'].str.replace('  ', ' ').str.strip()
            advantages['Contestant'] = advantages['Contestant'].str.replace('  ', ' ').str.strip()
            immunities['Contestant'] = immunities['Contestant'].str.replace('  ', ' ').str.strip()
            
            # with all the datasets sufficiently cleaned, we then go ahead and merge the datasets to the stats table
            merged_idols = pd.merge(stats, idols, on=['Contestant', 'Season'], how='left')
            merged_with_advantages = pd.merge(merged_idols, advantages, on=['Contestant', 'Season'], how='left')
            final_stats = pd.merge(merged_with_advantages, immunities, on=['Contestant', 'Season'], how='left')

            # I then reorder the columns by creating a list with them in the desired order, and then reindex the merged table
            reorder_columns = ['Season', 'Contestant', 'SurvSc', 'SurvAv', 'ChW', 'ChA', 'ChW%',
                            'SO', 'VFB', 'VAP', 'TotV', 'TCA', 'TC%', 'wTCR', 'JVF', 'TotJ',
                            'JV%', 'IF', 'IH', 'IP', 'VV', 'ICW', 'ICA', 'AF', 'AP', 'Notes']
            final_stats = final_stats.reindex(columns=reorder_columns, fill_value=0)
            
            # I do some more stripping for values from the original stats table that hadn't been handled yet
            final_stats['VAP'] = final_stats['VAP'].astype(str).str.rstrip('*')
            final_stats['TotV'] = final_stats['TotV'].astype(str).str.rstrip('*')
            final_stats['TCA'] = final_stats['TCA'].astype(str).str.rstrip('*')
            final_stats['TC%'] = final_stats['TC%'].astype(str).str.rstrip('*')
            final_stats['wTCR'] = final_stats['wTCR'].astype(str).str.rstrip('*')
                
            # Then I drop rows where SurvSc is null (Season 48 - no values for stats yet)
            final_stats = final_stats.dropna(subset='SurvSc')
            # Handling the rest of the null values by filling
            final_stats['Notes'] = final_stats['Notes'].fillna('NA')  
            final_stats = final_stats.fillna(0)
            # Some of the tables had '-' for null values, I replaced those with 0 for the sake of converting their datatype to int later
            final_stats = final_stats.replace('-', '0')

            # then I ensure all of the columns are the appropriate datatype by creating a dictionary
            final_stats = final_stats.astype({
            'SurvSc': 'float64', 'SurvAv': 'float64', 'ChW': 'float64', 'ChA': 'float64',
            'ChW%': 'float64', 'TC%': 'float64', 'wTCR': 'float64', 'JV%': 'float64',
            'SO': 'int64', 'VFB': 'int64', 'VAP': 'int64', 'TotV': 'int64', 'TCA': 'int64',
            'JVF': 'int64', 'TotJ': 'int64', 'IF': 'int64', 'IH': 'int64', 'IP': 'int64',
            'VV': 'int64', 'ICW': 'int64', 'ICA': 'int64', 'AF': 'int64', 'AP': 'int64'
            })
            # Lastly I ensure there were no duplicate columns
            final_stats = final_stats.drop_duplicates(subset=['Contestant', 'Season'], keep='last')
    # For some reason the Notes column sometimes unfills the null values on repeat runs, this if statement ensures the values are filled as intended
    if 'Notes' in stats.columns:
        final_stats['Notes'] = final_stats['Notes'].fillna('NA') 
    return final_stats 

def rename_columns(stats:pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns in stats table to be more readable
    """
    # manually renames column names in stats table from their abbreviated names for better readability
    stats = stats.rename(columns={
        'SurvSc': 'Survival Score',
        'SurvAv': 'Survival Average',
        'ChW': 'Challenge Wins',
        'ChA': 'Challenge Appearances',
        'ChW%': 'Challenge Win %',
        'SO': 'Sit Outs',
        'VFB': 'Votes For Bootee',
        'VAP': 'Votes Against (Total)',
        'TotV': 'Total Votes Cast',
        'TCA': 'Tribal Council Appearances',
        'TC%': 'Tribal Counicl %',
        'wTCR': 'Tribal Council Ratio (Weighted)',
        'JVF': 'Jury Votes For',
        'TotJ': 'Total Numbers Of Jurors',
        'JV%': 'Jury Votes %',
        'IF': 'Idols Found',
        'IH': 'Idols Held',
        'IP': 'Idols Played',
        'VV': 'Votes Voided',
        'ICW': 'Immunity Challenge Wins',
        'ICA': 'Immunity Challenge Appearances',
        'AF': 'Advantages Found',
        'AP': 'Advantages Played'
    })
    return stats

def extract_state(hometown:str) -> str:
    '''
    Extracts the state or province from values in the pd.Dataframe column contestants['Hometown'] 
    in preparation to be stored in the column contestants['State']

    Args:
        hometown(str): The value in contestants['Hometown']. Most commonly formatted 'City, ST'
    Returns:
        str: The state or province extracted from the 'hometown' value. 
    '''
    try:
        # ensures that if the hometown value is Washington DC with no comma, that a comma is added to fit the format for extraction
        if hometown == 'Washington DC':
            hometown = 'Washington, DC'
        # if the hometown has parenthesis such as when a contestant is from Canada, that only the section before the parenthesis is kept
        if '(' in hometown:
            hometown = hometown.split(' (')[0]
        # splits the hometown by the comma, keeps anything after the comma
        return hometown.split(', ')[1]
    except:
        # prints an error message in case an issue arises
        print(f'Error- {hometown} unable to be stripped')    

def add_countries(hometown:str) -> str:
    '''
    Returns either 'Canada' or 'USA' as corresponds to the value in contestants['Hometown']
    in preparation to be stored in the column contestants['Country']

    Args:
        hometown(str): The value in contestants['Hometown']. Most commonly formatted 'City, ST'
    Returns:
        str: The country as determined by the 'hometown' value.
    '''
    # assuming there will be no contestants from outside the usa or canada, returns Canada as country if it is present in the hometown value
    if 'Canada' in hometown:
        return 'Canada'
    # otherwise, returns USA as country
    else:
        return 'USA'