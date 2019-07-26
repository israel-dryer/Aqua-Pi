# Aqua-Pi

A project to collect, monitor, and report on an Aquaponics setup.

### Data Collection
The **logger_aws.py** module contains the **Logger** class which creates a connection to the **aquapi** PostgreSQL server hosted on AWS. To use this module, you'll need to make sure you first install the package *psycopg2* using the following command:
```
sudo pip3 install psycopg2
```

To run the full data collection package:
- download the files contained in the Data-Collection folder
- change the username and password in main.py
- run the main.py script from your code editor, or by opening command prompt in that directory and typing 
```
python3 main.py
```
