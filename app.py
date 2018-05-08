#Design a Flask app based on the queries in Climate Analysis

################################################
#Import dependencies
################################################
import datetime 
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Map Station class
Stations = Base.classes.stations

# Map Measurement class
Measures = Base.classes.measurements

# create a session
session = Session(engine)

#################################################
#Set a few useful variables
#################################################
#Find last record (most recent date) in data
last_record = session.query(Measures.date).order_by(Measures.date.desc()).first()

#Datetime doesn't like a "result", do something to make it a string and clean it up
date = str(last_record).split("'")[1]

#Determine one year (12 months) from last record
last_date = datetime.datetime.strptime(date, "%Y-%m-%d")
last = last_date - datetime.timedelta(days=364)
last_year = last.strftime("%Y-%m-%d")

#################################################
#Flask set-up
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """All available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>...accepts date in mm-dd-yyyy format<br/>"
        f"/api/v1.0/<start>/<end>...accepts date in mm-dd-yyyy format<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of date and precipitation observations from the last year"""

#Database setup (would not run outside of def)
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    #Map Station class
    Stations = Base.classes.stations
    #Map Measurement class
    Measures = Base.classes.measurements

    #Create a session
    session = Session(engine)

    #Query database
    data = session.query(Measures.date, Measures.prcp).\
    filter(Measures.date >= last_year).all()
    
    # Convert list of tuples into a dictionary, then into JSON
    
    all_prcp = []
    for x in range(len(data)):
        prcp_dict = {}
        prcp_dict["date"] = str(data[x]).split(",")[0].split("(")[1]
        prcp_dict["prcp"] = str(data[x]).split(",")[1].split(")")[0]
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of weather stations"""
    #Database setup (would not run outside of def)
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    #Map Station class
    Stations = Base.classes.stations
    #Map Measurement class
    Measures = Base.classes.measurements

    #Create a session
    session = Session(engine)

    #Query all passengers
    results = session.query(Measures.station).distinct().all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations from the past year"""
    #Database setup (would not run outside of def)
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    #Map Station class
    Stations = Base.classes.stations
    #Map Measurement class
    Measures = Base.classes.measurements

    #Create a session
    session = Session(engine)

    #Query all passengers
    data = session.query(Measures.date, Measures.tobs).\
    filter(Measures.date >= last_year).all()

    # Convert list of tuples into a dictionary, then into JSON
    all_tobs = []
    for x in range(len(data)):
        tobs_dict = {}
        tobs_dict["date"] = str(data[x]).split(",")[0].split("(")[1]
        tobs_dict["prcp"] = str(data[x]).split(",")[1].split(")")[0]
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")

def start_date(start):

    #Database setup (would not run outside of def)
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    #Map Station class
    Stations = Base.classes.stations
    #Map Measurement class
    Measures = Base.classes.measurements

    #Create a session
    session = Session(engine)

    #Set variables
    start_month = (start).split("-")[0]
    start_day = (start).split("-")[1]
    start_year = (start).split("-")[2]
    start_date = start_year+"-"+start_month+"-"+start_day

    #Set parameters to return avg, min, and max temps from SQLite query 
    sel = [Measures.date, 
       func.avg(Measures.tobs), 
       func.max(Measures.tobs), 
       func.min(Measures.tobs),]
    
    #Query database for data on dates greater than start date
    data = session.query(*sel).\
    filter(func.strftime(Measures.date) >= start_date).all()

    # Convert list of tuples into a dictionary, then into JSON
    all_normals = []
    for x in range(len(data)):
        norms_dict = {}
        norms_dict["date"] = "All dates from "+(start)
        norms_dict["avg"] = str(data[x]).split(",")[1]
        norms_dict["min"] = str(data[x]).split(",")[2]
        norms_dict["max"] = str(data[x]).split(",")[3].split(")")[0]
        all_normals.append(norms_dict)

    return jsonify(all_normals)

@app.route("/api/v1.0/<start>/<end>")

def between_date(start,end):

    #Database setup (would not run outside of def)
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    #Map Station class
    Stations = Base.classes.stations
    #Map Measurement class
    Measures = Base.classes.measurements

    #Create a session
    session = Session(engine)

    #Set variables
    start_month = (start).split("-")[0]
    start_day = (start).split("-")[1]
    start_year = (start).split("-")[2]
    start_date = start_year+"-"+start_month+"-"+start_day

    end_month = (end).split("-")[0]
    end_day = (end).split("-")[1]
    end_year = (end).split("-")[2]
    end_date = start_year+"-"+start_month+"-"+start_day

    #Set parameters to return avg, min, and max temps from SQLite query 
    sel = [Measures.date, 
       func.avg(Measures.tobs), 
       func.max(Measures.tobs), 
       func.min(Measures.tobs),]
    
    #Query database for data on dates greater than start date
    data = session.query(*sel).\
    filter(func.strftime(Measures.date) >= start_date).\
    filter(func.strftime(Measures.date) <= end_date).all()

    # Convert list of tuples into a dictionary, then into JSON
    all_normals = []
    for x in range(len(data)):
        norms_dict = {}
        norms_dict["date"] = "All dates from "+(start)+" to "+(end)
        norms_dict["avg"] = str(data[x]).split(",")[1]
        norms_dict["min"] = str(data[x]).split(",")[2]
        norms_dict["max"] = str(data[x]).split(",")[3].split(")")[0]
        all_normals.append(norms_dict)

    return jsonify(all_normals)

if __name__ == "__main__":
    app.run(debug=True)