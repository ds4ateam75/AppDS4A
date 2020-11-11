# AMVAPP Dashboard

## Table of contents
* [About this app](#About-this-app)
* [How to run this app](#How-to-run-this-app)
* [Screenshots](#Screenshots)
* [Resources](#Resources)

## About this app

AMVAPP is a web application that is used to visualize passenger load data in the public transport service of Valle de Aburrá.
With this application, the load can be seen in different hour and day ranges. 

The application has two main approaches:
  1. A view of historic data from the Valle de Aburrá load with actual loads of the streets of Valle de Aburrá. 
  2. A prediction of the load in the streets divided in three categories: low, medium and high load.
 
## How to run this app

(The following instructions apply to Windows command line.)

To run this app first clone repository and then open a terminal to the app folder.

```
git clone https://github.com/plotly/dash-sample-apps.git
cd dash-sample-apps/apps/dash-uber-rides-demo
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


## Screenshots

![demo.png](demo.png)

## Resources

To learn more about Dash, please visit [documentation](https://plot.ly/dash).
