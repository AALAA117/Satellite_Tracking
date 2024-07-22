# Satellite Tracking
An API for satellite Tracking that users can use to retrieve a specific velocity and position of satellite at specific time

the retrieved data can be used in :
### Space Educational Purpose:
- A simulation for satellite orbit propagation that can be used for analysis and visualization for students

- Study the effet of orbit perturbation

### Web Service:
An api service that can be combined with weather service to analyze the satellite performance at specific atmospheric conditions

[Landing Page](https://aalaa117.github.io/sat_tracking/)

[Github](https://github.com/AALAA117/Satellite_Tracking)

[Linkedin](https://www.linkedin.com/in/aalaa-mohammed-927a99281/)

# Installation

### Prerequisites:

- Operating System: Linux
- Python: Version 3.8 or higher
- Git: For cloning the project repository
- MySQL: For database setup

### Steps:
Clone the Repository:
```
git clone https://github.com/AALAA117/Satellite_Tracking
cd Satellite_Tracking
```
Install Dependencies
```
pip install -r requirements.txt
```
Configure MySQL Database
```
cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
```
Run the Application
```
python3 run.py
```
Test the API
```
curl -X GET http://localhost:5005/api/active_sat/FORTE
```
# Usage
The Satellite Tracking Project is designed to track the positions and velocities of satellites based on their Two-Line Element (TLE) data. Below is a guide on how to use the various features of the project.

- Get Active Satellite Data:
  
  GET api/active_sat/TIBA-1
  ```
  curl -X GET http://localhost:5005/api/active_sat/TIBA-1
  ```
- Update Satellite Data:
  
  PUT /api/update_sat/TIBA-1
```
curl -X PUT http://127.0.0.1:5005/api/active_sat/TIBA-1 -H "Content-Type: application/json" -d '{"date_time": "2024-07-10 11:54:03"}'
```
# Contributing

Aalaa Mohammed is the only contributor at this time

# Related projects
Here is a [repo](https://github.com/AALAA117/alx-higher_level_programming) that represents my python skills.

# Licensing
Free to use but please give me credit.
