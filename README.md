HOW TO RUN
==========

The application written in Python (tested on 3.7) and uses REDIS and Flask

There are two options for running:
1) Local:
    
    a. Make sure you installed redis-server
    
    b. Make sure you installed the packages in the requrements.txt file

    c. Run on terminal: **python3.7 main.py localhost**

2) Docker:

    a. Make sure you have docker-compose installed

    b. Run on terminal in the application folder: **docker-compose up** 

The folder also contains a json file for using postman to send requests to the Rest API server.