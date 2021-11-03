<!-- SETUP -->
## SETUP

Thank you for visiting my repo. To ensure you have the proper packages run the following commands to 
set up a virtual environment.

  ```sh
  conda env create -f environment.yml
  conda activate qualoffer
  ```


<!-- GETTING STARTED -->
## Getting Started

In this repo you will find 5 seperate python files:

- main.py
- plotter.py
- dataframe_functions.py
- get_player_data.py
- link_to_dataframe.py

main.py is meant to be the point of execution of the program.
The other files are intended to be wrappers/functions that are called upon from the main.py file

_Below is an introduction of the functions each helper file provides to main.py_

### link_to_dataframe.py

The main purpose of this file is to scrape the data from the link that was provided and 
convert it into a pandas dataframe. The functions are listed below:

  ```sh
  link_to_dataframe(link, fill_in_missing_data, check_for_data_disparity)
  ```
link_to_dataframe() takes 3 arguments:
* __link__ - _this would be the web link to the dataset_
* __fill_in_missing_data__ - _when scraping the provided link, if there in a missing or Null value for salary, the program will make a request to Baseball-Reference.com to find the value there. Set to True or False_
* __check_for_data_disparity__ - _the salary of every player in the dataset will be compared to the listed value on Baseball-Reference.com, a flag will be raised if they are significantly different. Set to True or False_

The function returns a dataframe object

__warning__: enabling fill_in_missing_data or check_for_data_disparity significantly slows down runtime


  ```sh
  check_salary_disparity(player_name, player_year, player_original_salary)
  ```
check_salary_disparity() takes 3 arguments:
* __player_name__ - _format: <Lastname, Firstname>_
* __player_year__ - _format: int_
* __player_original_salary__ - _this would be the value from our dataset, which will be checked against Baseball-Reference.com, format: int_

The function will return True if the value for salary is significantly greater between the given dataset and Baseball-Reference.com.

  ```sh
  find_salary(player_name, player_year)
  ```
find_salary() takes 2 arguments:
* __player_name__ - _format: <Lastname, Firstname>_
* __player_year__ - _format: int_

The function will return the listed salary of the player on Baseball-Reference.com for the given year.



### get_player_data.py

The main purpose of this file is to find the respective Baseball-Reference.com page for a given player and scrape the data we desire.

  ```sh
  get_player_page(find_player_name, current_year)
  ```
get_player_page() takes 2 arguments:
* __find_player_name__ - _format: <Lastname, Firstname>_
* __current_year__ - _format: int_

The function returns the link to the player's Baseball-Reference.com page

  ```sh
  extract_data_from_link(link, current_year)
  ```
extract_data_from_link() takes 2 arguments:
* __link__ - _link to player's baseball-reference.com page_
* __current_year__ - _format: int_

The function scrapes data from the website and returns it in JSON format

 ```sh
  get_stats_from_name(player_name, current_year)
  ```
get_stats_from_name() takes 2 arguments:
* __player_name__ - _format: <Lastname, Firstname>_
* __current_year__ - _format: int_

The function returns the player's statistics in JSON format


### dataframe_functions.py

The main purpose of this file is to provide functions which preform operations on a pandas dataframe

  ```sh
  sort_by_salary(df)
  ```
sort_by_salary() takes 1 argument:
* __df__ - _pandas dataframe_

The function returns the dataframe but sorted by salary


  ```sh
  average_salary(df)
  ```
average_salary() takes 1 argument:
* __df__ - _pandas dataframe_

The function returns the average salary of all players in the dataframe


  ```sh
  nth_largest(df, n)
  ```
nth_largest() takes 1 argument:
* __df__ - _pandas dataframe_

The function returns the dataframe but shortened to only the top n values

### plotter.py

The main purpose of this file is to provide visualization functions for the dataframe

  ```sh
  salary_war_plot(df)
  ```
salary_war_plot() takes 1 argument:
* __df__ - _pandas dataframe_

The function returns a matplotlib scatter plot of player's salary vs war

  ```sh
  salary_position_plot(df)
  ```
salary_position_plot() takes 1 argument:
* __df__ - _pandas dataframe_

The function returns a matplotlib bar graph of the defensive positions that appear in the dataframe


  ```sh
  salary_histogram(df)
  ```
salary_position_plot() takes 1 argument:
* __df__ - _pandas dataframe_

The function returns matplotlib histogram of the salaries within the dataframe