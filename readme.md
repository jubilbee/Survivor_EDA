<h1 style='text-align: center;'><b>Survivor: </b>Exploring Contestant Trends Through Data</h1>

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
This project contains two main dataset, including one focused on information about contestant demographics, including details such as age, ethnicity, gender, profession, hometown, whether they identify as lgbt, and whether they had a disability at the time of competing. The other includes statistic information about the contestants gameplay during their season. See **Data_dictionary.pdf** and **Survivor_database_ERD.pdf** for a more in-depth look into the structure and details of these datasets.

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
* Webscraping: Python script scraper.py is used to extract the data from websites listed [above](#data)

* Data Exploration: The Jupyter notebook Survivor_EDA.ipynb explores the dataset.

* Analysis: Using Python with the Pandas package to clean the data.

* Visualizations : Using Matplotlib and Seaborn to visualize findings.

* Dashboard: Tableau dashboard for this project can be found [here](https://public.tableau.com/app/profile/camilla.babb/viz/Survivor_17399844202740/Dashboard1 "Survivor Tableau Dashboard").
## Features Utilized for the Project
 | Feature        | Description                           |
  |----------------|---------------------------------------|
  | Scrape TWO pieces of data from anywhere on the internet and utilize it in your project. | Scraped data from multiple sources as listed in the [Data](#data) section.         |
  | Clean your data and perform a pandas merge with your two data sets, then calculate some new values based on the new data set.      | Cleaned my data (specifically, the stats, idols, immunity, and advantages dataset) and merged them with pandas.|
   Clean your data and perform a SQL join with your data sets using either plain sql or the pandasql Python library      | Used sqlite to join my data (stats and contestants) in multiple queries 
  | Make 3 matplotlib or seaborn (or another plotting library) visualizations to display your data.| Made various plots to show off my findings, using matplotlib and seaborn. |
  | Make a Tableau dashboard      | Made a dashboard with my findings. [Tableau](https://public.tableau.com/app/profile/camilla.babb/viz/Survivor_17399844202740/Dashboard1) |
  | Utilize a virtual environment      | Made a venv for this project. |
  | Notate your code with markdown cells in Jupyter Notebook | Included in my code, you will find clear notes describing each code block. |
## AI Usage

## Getting Started
To run this project, first you'll need to clone the repository to your local machine.
```bash
git clone https://github.com/jubilbee/Survivor_EDA.git
```
Navigate into the project repository:
```bash
cd Survivor_EDA
```
## Dependencies

### Virtual Environment Instructions
1. After you have cloned the repo to your machine, navigate to the project folder in GitBash/Terminal.
2. Create a virtual environment in the project folder.
3. Activate the virtual environment.
4. Install the required packages.
5. When you are done working on your repo, deactivate the virtual environment.

**Virtual environment commands**
| Command | Linux/Mac | GitBash |
| ------- | --------- | ------- |
| Create | `python3 -m venv venv` | `python -m venv venv` |
| Activate | `source venv/bin/activate` | `source venv/Scripts/activate` |
| Install | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Deactivate | `deactivate` | `deactivate` |


## Credits

