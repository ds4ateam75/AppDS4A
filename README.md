# ABURRAPP Dashboard

## Table of contents
* [About this app](#About-this-app)
* [Motivation](#Motivation)
* [Technologies](#Technologies)
* [How to run this app](#How-to-run-this-app)
* [How to use](#How-to-use)
* [Resources](#Resources)
* [Credits](#Credits)

## About this app

ABURRAPP is a web application that is used to visualize passenger load data in the public transport service of Valle de Aburrá.
With this application, the load can be seen in different hour and day ranges. 

The application has two main approaches:
  1. A view of historic data from the Valle de Aburrá load with actual loads of the streets of Valle de Aburrá. 
  2. A prediction of the load in the streets divided in three categories: low, medium and high load.
  
## Motivation

This project was created to help the AMVA to provide optimal approaches to the current mobility problems of the Valle de Aburrá. With this application, the hot spots of traffic load can be seen easily, which tend to be a problem in Colombia. With its improvements, it can be used to approach other cities with much larger mobility issues. 
  
## Technologies
The project is created with:
* Python version: 3.7.6
* Amazon EC2
* Amazon RDS
 
## How to run this app

(The following instructions apply to Windows command line.)

To run this app first clone repository and then open a terminal to the app folder.

```
git clone https://github.com/ds4ateam75/AppDS4A.git
cd AppDS4A
```

Create and activate a new virtual environment (recommended) by running
the following:

On Windows

```
virtualenv venv 
\venv\scripts\activate
```

Or if using linux

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

Install the requirements:

```
pip install -r requirements.txt
```
Run the app:

```
python app.py
```
You can run the app on your browser at http://127.0.0.1:8050

## How to use

When opening the app on the browser, the first thing you should do is press the 'proyecto' tab located in the upper left part of the interface and read all about the app.

![alt text](https://github.com/ds4ateam75/AppDS4A/blob/master/assets/pestana_proyecto.png?raw=true)


After reading the information, you should be prepared to use the app. If you want to review the historical data, you should go to the 'DESCRIPCION' tab and first you have to select the day and hour range where you want to see the load, and then navigate through the map in order to see the distribution of passenger load in the Valle de Aburrá.

**Select** the **tab** shown in the **red box**:
![alt text](https://github.com/ds4ateam75/AppDS4A/blob/master/assets/descripcion1.png?raw=true)

**Select** your **day and hour range** in the options shown in the **red box**:
![alt text](https://github.com/ds4ateam75/AppDS4A/blob/master/assets/descripcion2.png?raw=true)

If you want to make a prediction of the load you have to go the 'PREDICCIÓN' tab and select the hour and day from which you want to make it. 

**Select** the **tab** shown in the **red box**:
![alt text](https://github.com/ds4ateam75/AppDS4A/blob/master/assets/prediccion1.png?raw=true)

**Select** your **day and hour range** in the options shown in the **red box**:
![alt text](https://github.com/ds4ateam75/AppDS4A/blob/master/assets/prediccion2.png?raw=true)


## Credits

This application was developed by DS4A Team 75:

* Andrés Rodriguez. linkedIn page: https://www.linkedin.com/in/andguez 
* Julián García. linkedIn page: https://www.linkedin.com/in/julianlgarciap/  
* Ronald Morales. linkedIn page: http://linkedin.com/in/moralesrronald
* Juan Pablo Chica. linkedIn page: https://www.linkedin.com/in/juan-pablo-chica-castrill%C3%B3n-1b482614a/
* Sebastien Lozano. linkedIn page: https://www.linkedin.com/in/sebastienlozanoforero/
* Rafael Machado. linkedIn page: www.linkedin.com/in/rafael-machado-molina
* José Cárdenas. linkedIn page: https://www.linkedin.com/in/josealejandrocardenas
