## COSC 2790 - Programming IoT - Assignment II - Library Management System

- Team: 3.14
- Members:
    - Nguyen Le Bao Anh (s3616128)
    -
    -
    -
- Github: [Link](https://github.com/usefulmana/piot-a2-lms/tree/master)
- REST API Endpoints: [Link](https://documenter.getpostman.com/view/7194228/SVSDPWbW?version=latest)
- Description: this program will enable two Raspberry Pis to help managing a library. This system will be used to borrowed
, return and maintain the backend information. It will also serve two types of users: library users and library admins.

### Features:
- **Master Pi**
    - Host the Flask REST API to communicate with the library's database.
    - Host a secured web server for admins to add and delete books, as well as viewing daily and weekly statistics.
    - Host the main application where user will be able to search, borrow and return books.
    - Have an option for users to be reminded of the due date via Google Calendar.
    - Features a QR reader for quick return service.
    - A voice recognition feature to search for books.
- **Reception Pi**
    - Host a secured login server where users can login with their emails and passwords or facial recognitions.
    - Communicate with the Master Pi via sockets.
### Package Requirements:
   This project requires Python version >= 3.5.3
- **Master Pi**
    - For Anaconda:
````conda env create -f master_pi_env.yml````

    - For pip: copy & paste the dependencies part of the .yml files to a file name ````requirements.txt```` and then: 
    ````pip install -r requirements.txt````
    - For Rpi: install the following packages
    
    ````
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install lipportaudio-dev
    sudo apt-get install python-dev
    sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
    ````
    - To install the dependencies of the React application:
    ````
    cd <your_directory>/piot-a2/webapp/front-end
    npm install
    ````
- **Reception Pi**
    - For Anaconda:
````conda env create -f reception_pi_env.yml````

    - For pip: copy & paste the dependencies part of the .yml files to a file name ````requirements.txt```` and then: 
    ````pip install -r requirements.txt````
    
### Setting Up
- **Master Pi**
    - This Pi uses a cloud mySQL database (GCP specifically). However, you can use your own local database if you
    wish. 
    - Tutorial on how to set up a GCP mySQL database can be found [here](https://cloud.google.com/sql/docs/mysql/quickstart).
    - Tutorial on how to set up a Pi mysql database can be found [here](https://pimylifeup.com/raspberry-pi-mysql/).
    - Create a config.json file in the **webapp** directory with the following information:
    ````
    {
  "host": "<<Your database's host>>",
  "database": "<<Your database's name>>",
  "password": "<<Your password>>",
  "user": "<<Your username>>",
  "days_to_return_book": <<The number of days that a book can be borrowed for>>,
  "secret_key": "<<Type anything here. Do not leave blank>>"
    }
    ````
    - Get your Pi's IP address by typing ````ifconfig```` in the console.
    - Create another config.json file in the **mainapp** directory with the following information:
    ````
    {
    "host": "<<Your Pi's IP Address>>",
    "port": <<Any port here>>,
    "email": <<Your email address>>,
    "days_to_be_reminded": <<days from due date>>
    }
    ````
    - The above email address in ````config.json```` will be used to send QR codes to users. I recommend turning off any security
    features for this account.
    - To use the Google Calendar service, get your credentials [here](https://developers.google.com/calendar/quickstart/python)
    and then save the ````credentials.json```` in the **mainapp** folder.
- **Reception Pi**
    - Similar to the Master Pi, you can use a local or a cloud database depending on your need.
    - Write down the Master Pi's IP address and port.
### Running the Program
- **Master Pi**
    - To run the Flask REST API & Node Web Server, simply run the master_pi_scheduler.py. It will run these services
    on boot or you can just run them individually.
    - You will have to run the main application manually.
- **Reception Pi**
    - Run the Login.py file to start the program.