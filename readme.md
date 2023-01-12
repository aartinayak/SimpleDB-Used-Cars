# CSCI_621_USED_CARS
This is a project based dataset of Used Cars and rendering the listings based on the filters. In this project, we have used SimpleDB as our database, Flask for the backend and HTML Jinja Templates and CSS for Frontend. The main motive of the project is to dynamically fetch all the information from the SimpleDB Database and display it with interactive properties. 

## Usability
* Set virtual environment by running the following command in command prompt
> pip install venv (virtual environment name)
> virtual environment name can be of your choice

* Install boto by running the following command in command prompt
> pip install boto

* app.py is the main python file that you will run after installing virtual environment.
* Lib directory contains python libraries
* Static directory has all the images and css files used for UI
* Template directory has all the html files
* pyenv configuration source file contains the environment required for flask.

## Tech Stack:
* HTML Jinja Templates (FrontEnd)
* Flask (Backend)
* SimpleDB (Database)

## Features of the Model:
* Retrieving the data from SimpleDB. 
* Making interactive UI for displaying more details.
* Inserting user data to the database.
* Retrieving the data from the database.
* Other features for searching the used car based on pereferences as:
>Searching by the Linsting ID

>Searching by model name of the car

>Searching with other attributes such as body type, exterior color, transmission, fuel type etc.


## Dependencies:
1. boto.sdb
2. pandas
3. Flask Virtual Enviornment

## Collaborators:
1. Amanraj Lnu 
2. Aarti Nayak
3. Kruthi Nagabhushan
4. Swetna Tribuvan

