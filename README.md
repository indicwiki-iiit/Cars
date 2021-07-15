# Cars
We generated articles on cars domain in telugu language which is part of indicwiki project.
## Description
The aim of this project is to generate large number of articles (32,000) on cars which includes various brands of India and US in telugu language. People who want to purchase cars can refer to these wikipedia articles and can get an idea about the specifications of different cars. As these articles include both US and Indian made cars of many brands, this is the best source where people can get to know about different cars before purchasing them. These articles describe about different car specifications like dimensions of car, engine type, wheel material type, torque, horse power etc.
## Installation
Create virtual environment in the project folder using the following commands.

```bash
$ pip install virtualenv
$ virtualenv -p python3.7 venv
```
After the successful creation of virtual environment (venv), clone the repository or download the zip folder of the project and extract it into the project folder.

Activate the virtual environment and headover to install the dependencies by following command.
```bash
$ pip install -r requirements.txt
```
requirements.txt comes along with the Project Directory. 
## Guide to generate articles and corresponding XML files
* Clone the repository into the local system.

* For generating an article, one need the data, render.py, template and genXML.py. Make sure that these files are available.

* Running the genXML.py initialises all the functions necessary for XML generation

* Both the article and the XML file can then be generated by running the main.py file

## Data
Github folder link:
* Indian cars.csv-This is the final dataset which contains the attributes of Indian Cars.
*•	Cars_report.html-This data analysis report is used to check how many unique values are present for every attribute and how many missing values for the attributes.

## Templates

 Github folder link:

* Cars.indian.j2-This template contains the information about Infobox, Introduction, Engine and Performance, Design for Indian Cars.

### Generating XML dump

* Follow the comments of 'render.py' and uncomment necessary lines to generate XML dump.
* Execute 'render.py'  file with the  following command:
- `python3.7 render.py`. 
- We can generate as many number of articles by slicing the ids list.
- This will generate the XML dump for given car ids list, and store them in the xml file 'Cars.xml'.
