<h1 align="center"><b>Survivor: </b></h1>
<h3 align="center"><b>Exploring Contestant Trends Through Data</b></h3>

## Overview
This project webscrapes, cleans, and visualizes data related to contestant demographics and gameplay stats for the CBS hit show Survivor. The goal of this project is to examine the data and determine if there are any trends present that would point to certain demographics having better chances of winning the show than others, or conversely, if certain demographics have noteably lower chances of winning. It also looks at how these trends vary between the classic era of Survivor (seasons 1-39), and the new era (seasons 40 onward)


* Webscrapes the data from various sites 
* Cleans the data by removing unnecessary columns, uniformly formatting the column names and datatypes, and adding relevant attributes
* Some visualizations created in this project include:
    * A line graph of the average placement of contestants by age group per season
    * Pie charts showing the distribution of season winners by gender for the classic and new era's of Survivor
    * Pie charts showing the placements of contestants with disabilities for the new era and overall
    * Bar graphs depicting the distribution of contestants based on ethnicity, as present with contestants overall, winners, average placement, and average jury vote percentage earned
## Data
This project contains two main datasets, one focused on information about contestant demographics, while the other focuses on gameplay statistics. The 'contestants' dataset includes details such as age, ethnicity, gender, profession, hometown, whether they identify as lgbt, and whether they had a disability at the time of competing, while 'stats' includes statistic information about the contestants gameplay during their season, such as average jury vote %, challenge wins, and idols found. See **Data_dictionary.pdf** and **Survivor_database_ERD.pdf** for a more in-depth look into the structure and details of these datasets.

The datasets were created by webscraping various sources, such as the [US Survivor contestants](https://en.wikipedia.org/wiki/List_of_Survivor_(American_TV_series)_contestants "Contestants wiki") wikipedia page, and [season stats](https://www.truedorktimes.com/survivor/boxscores/s1.htm
 "Season stats") from The True Dork Times website. Other sites scraped for this project:
* [Female contestants wiki](https://survivor.fandom.com/wiki/Category:Female_Contestants "Female contestants")
* [Male contestants wiki](https://survivor.fandom.com/wiki/Category:Male_Contestants "Male contestants")
* [African American contestants wiki](https://survivor.fandom.com/wiki/Category:African-American_Contestants "African American contestants")
* [African Canadian contestants wiki](https://survivor.fandom.com/wiki/Category:African-Canadian_Contestants "African Canadian contestants")
* [Asian American contestants wiki](https://survivor.fandom.com/wiki/Category:Asian-American_Contestants "Asian American contestants")
* [Asian Canadian contestants wiki](https://survivor.fandom.com/wiki/Category:Asian-Canadian_Contestants "Asian Canadian contestants")
* [Latin American contestants wiki](https://survivor.fandom.com/wiki/Category:Latin_American_Contestants "Latin American contestants")
* [LGBT contestants wiki](https://survivor.fandom.com/wiki/Category:LGBT_Contestants "LGBT contestants")
* [Disabled contestants wiki](https://survivor.fandom.com/wiki/Category:Disabled_Contestants "Disabled contestants")
* [Idols stats](https://truedorktimes.com/survivor/boxscores/idolsfound-season.htm "Idols stats")
* [Advantage stats](https://truedorktimes.com/survivor/boxscores/advantages.htm "Advantage stats")
* [Individual immunity challenge wins](https://truedorktimes.com/survivor/boxscores/icwin.htm "Individual Immunity wins")

## Project Structure
The project is organized as follows:
* Webscraping: Python script scraper.py is used to extract the data from websites listed [above](#data).

* Data Exploration: The Jupyter notebook Survivor_EDA.ipynb explores the dataset.

* Analysis: Using Python with the Pandas package to clean the data.

* Visualizations : Using Matplotlib and Seaborn to visualize findings.

* Dashboard: Tableau dashboard for this project can be found [here](https://public.tableau.com/app/profile/camilla.babb/viz/Survivor_17399844202740/Dashboard1 "Survivor Tableau Dashboard").
## Features Utilized for the Project
 | Feature        | Description                           |
  |----------------|---------------------------------------|
  | Scrape TWO pieces of data from anywhere on the internet and utilize it in your project | Scraped data from multiple sources as listed in the [Data](#data) section.         |
  | Clean your data and perform a pandas merge with your two data sets, then calculate some new values based on the new data set      | Cleaned my data (specifically, the stats, idols, immunity, and advantages dataset) and merged them with pandas.|
   Clean your data and perform a SQL join with your data sets using either plain sql or the pandasql Python library      | Used sqlite3 to join my data (stats and contestants) in multiple queries. 
  | Make 3 matplotlib or seaborn (or another plotting library) visualizations to display your data| Made various plots to show off my findings, using matplotlib and seaborn. |
  | Make a Tableau dashboard      | Made a dashboard with my findings on [Tableau](https://public.tableau.com/app/profile/camilla.babb/viz/Survivor_17399844202740/Dashboard1 "Survivor Tableau Dashboard"). |
  | Utilize a virtual environment      | Made a venv for this project. |
  | Notate your code with markdown cells in Jupyter Notebook | Included in my code, you will find clear notes describing each code block. |
  Build a custom data dictionary and include it either in your README or as a separate document  | Created a data dictionary to add context.
## AI Usage
AI assistance was used in this project. Specifically, in the scraper.py script for troubleshooting the functions extract_contestant_names(), stats(), and flatten_index(). 

I ran into issues particularly with getting the pagination for the urls involved in extracting the base data for the stats dataframe to work, first because it had noticeable discrepencies in how the tables the data came from were set up, then with less obvious discrepencies with how the html was formatted, which resulted in misalignment in how the data was extracted. The troubleshooting lead me to separating the extraction of contestant names from the main stats() function, turning it into a helper function. 

I also ran into issues with flattening the stats table, which was extracted as a multi-level index, and needed to consult with ai to find a solution, as the methods I found on handling multi-level indexes weren't working in this case.
## Getting Started
To run this project, first you'll need to clone the repository to your local machine.
```bash
git clone https://github.com/jubilbee/Survivor_EDA.git
```
Navigate into the project repository:
```bash
cd Survivor_EDA
```
Set up the virtual environment using the instructions below, ensuring the environment is being made inside the Survivor_EDA folder. 
## Dependencies
To properly run this project, the user will need to have the following: 
* An integrated development environment such as __VS Code__ (Recommended for this project)
* __Python 3.13.1 or higher__ installed on the user's system. 
    * Ensure that Python is located on the system's PATH, allowing Python commands to be executed from the terminal or command prompt. Refer to the official [Python](https://docs.python.org/3/using/windows.html#the-full-installer) documentation for more info.
    * ___For VS Code Users___: Ensure that the Python Extension is installed on VS Code.
* Jupyter Notebook is required for running __Survivor_EDA.ipynb__.
    * ___For VS Code Users___: Install the Jupyter Extension on VS Code.
* __Git Bash__ (Recommended for Windows Users) 

### Modules:
The following modules are used in this project and are included in __requirements.txt:__
* requests 
* BeautifulSoup
* pandas
* matplotlib
* seaborn 

Refer to requirements.txt for full list of version-specific dependencies and requirements.
### Virtual Environment Instructions
1. After you have cloned the repo to your machine, navigate to the project folder in GitBash/Terminal.
2. Create a virtual environment in the project folder.
3. Activate the virtual environment.
4. Install the required packages.
5. When you are done working on your repo, deactivate the virtual environment.

__Virtual environment commands__
| Command | Linux/Mac | Git Bash |
| ------- | --------- | ------- |
| Create | `python3 -m venv venv` | `python -m venv venv` |
| Activate | `source venv/bin/activate` | `source venv/Scripts/activate` |
| Install | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Deactivate | `deactivate` | `deactivate` |

__Note for VS Code Users__:

If you're using VS Code to run the Jupyter Notebook or Python script, ensure that the virtual environment(```venv```) is selected as the kernel. This is necessary for the modules installed from __requirements.txt__ to be active when running the project.
* To select the kernel, open the __Command Palette__ (``Ctrl+Shift+P`` or ``Cmd+Shift+P`` on Mac) and search for __"Python: Select Interpreter"__. Choose the one for the virtual environment (``venv``).


### Running the Project
This repository includes .csv files that were created during the project. If these files are present, the user can directly open and run __Survivor_EDA.ipynb__ in VS Code or their chosen IDE.

__If .csv files are missing:__
* Open __scraper.py__ in VS Code/chosen IDE
* Run the script to create the missing .csv files
* Once the files are created, open and run __Survivor_EDA.ipynb__.
* When running the notebook for the first time, VS Code may prompt you to install `ipykernel`. Click "Yes" to allow the installation. This is required for the notebook to function.

__Note on Webscraping and  Files:__

Though running __scraper.py__ should create .csv files if they're missing, errors may occur due to changes in the structure of the [websites](#data) being scraped. If any of the pages used in this process are updated or restructured, the script may no longer function as intended. 

The .csv files were added in this project as a way to ensure the Jupyter notebook __Survivor_EDA.ipynb__ would run for users regardless of any issues that may arise with the webscraping script.

## Credits
I would like to highlight a few of the resources I used in the creation of this project, specifically pages I used to learn new modules, and to inform decisions made throughout my scripts. Here is an (incomplete) list of sites I used in research for this project:
* [difflib.get_close_matches() — Python Standard Library](https://tedboy.github.io/python_stdlib/generated/generated/difflib.get_close_matches.html "Github.io")
* [Adding New Column to Existing DataFrame in Pandas - GeeksforGeeks](https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/# "GeeksforGeeks")
* [Beautiful Soup: Build a Web Scraper With Python – Real Python](https://realpython.com/beautiful-soup-web-scraper-python/ "Real Python")
* [Read Html File In Python Using Pandas - GeeksforGeeks](https://www.geeksforgeeks.org/read-html-file-in-python-using-pandas/# "GeeksforGeeks")
* [Python Pandas: Drop a Column From a Multi-level Column Index? - Stack Overflow](https://stackoverflow.com/questions/25135578/python-pandas-drop-a-column-from-a-multi-level-column-index "Stack Overflow")
* [Check if a File Exists in Python - GeeksforGeeks](https://www.geeksforgeeks.org/check-if-a-file-exists-in-python/# "GeeksforGeeks")
* [How to Add One Row in Existing Pandas DataFrame? - GeeksforGeeks](https://www.geeksforgeeks.org/how-to-add-one-row-in-an-existing-pandas-dataframe/ "GeeksforGeeks")
* [Pandas Strip Characters Left and Right Using Wildcards - Stack Overflow](https://stackoverflow.com/questions/69411654/pandas-strip-characters-left-and-right-using-wildcards "Stack Overflow")
* [Reorder Pandas Columns: Pandas Reindex and Pandas insert • datagy](https://datagy.io/reorder-pandas-columns/ "Datagy.io")
* [Python Docstrings - GeeksforGeeks](https://www.geeksforgeeks.org/python-docstrings/# "GeeksforGeeks")
* [SQL Server CAST() Function](https://www.w3schools.com/sql/func_sqlserver_cast.asp "w3schools")