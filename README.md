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

![picture](https://github.com/ds4ateam75/AppDS4A/tree/master/assets/pestana_proyecto.png)


After reading the information, you should be prepared to use the app. If you want to review the historical data, you should go to the 'DESCRIPCION' tab and first you have to select the day and hour range where you want to see the load, and then navigate through the map in order to see the distribution of passenger load in the Valle de Aburrá.

#Aquí debería haber otro screenshot de la primera ventana señalando las horas y día.

If you want to make a prediction of the load you have to go the 'PREDICCIÓN' tab and select the hour and day from which you want to make it. 

#Aquí otro screenshot de la segunda ventana (la de predicciones) y señalando dónde se debe poner la hora y día de predicción.


## Credits

This application was developed by DS4A Team 75:

* Andrés Rodriguez. linkedin page: https://www.linkedin.com/in/andguez 
* Julián García. linkedin page:  
* Ronald Morales. e-mail: 
* Juan Chica. e-mail:
* Sebastien Lozano. e-mail: 
* Rafael Machado. e-mail: 
* José Cárdenas. e-mail: jcardenas0719@gmail.com
