

```python
import csv
import pandas
import sqlalchemy as sql
import pandas as pd
import sqlite3
import numpy as np
```


```python
#Read in csv files
measure_pd = pd.read_csv("clean_hawaii_measurements.csv")
station_pd = pd.read_csv("hawaii_stations.csv")
```


```python
#Save for testing purposes
len(measure_pd.index)
```




    18103




```python
#Save for testing purposes
len(station_pd.index)
```




    9




```python
#SQLite doesn't like int64 or int32 or int8.  Decided to use 'Float' and deal with it in pandas later, as needed
measure_pd.dtypes
```




    station     object
    date        object
    prcp       float64
    tobs         int64
    dtype: object




```python
#Create SQLite database
conn = sqlite3.connect("hawaii.sqlite")
```


```python
# Import SQL Alchemy
from sqlalchemy import create_engine

# Import and establish Base for which classes will be constructed 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Import modules to declare columns and column data types
from sqlalchemy import Column, Integer, String, Float

# Create Station and Measurement classes
# ----------------------------------
class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    date = Column(String(255))
    prcp = Column(Float)
    tobs = Column(Float)

# Create Database Connection
# ----------------------------------
# Establish Connection to SQLite
engine = create_engine("sqlite:///hawaii.sqlite")
conn2 = engine.connect()
# Create both the Station and Measurement tables within the database
Base.metadata.create_all(conn2)
```


```python
# To push the objects made and query the server we use a Session object
from sqlalchemy.orm import Session
session = Session(bind=engine)

# Create specific instances of the Station class
# ----------------------------------
# Create new stations from values in hawaii_stations.csv
for x in range(len(station_pd)):
    station = Station(
        id = x,
        station = station_pd.iloc[x]["station"],
        name = station_pd.iloc[x]["name"],
        latitude = station_pd.iloc[x]["latitude"],
        longitude = station_pd.iloc[x]["longitude"],
        elevation = station_pd.iloc[x]["elevation"])
    # Add station(x) to the current session
    session.add(station)
    # Commit object to the database
    session.commit()
    
# Create specific instances of the Measurement class
# ----------------------------------
# Create new stations from values in clean_hawaii_measurements.csv
for x in range(len(measure_pd)):
    measurement = Measurement(
        id = x,
        station = measure_pd.iloc[x]["station"],
        date = measure_pd.iloc[x]["date"],
        prcp = measure_pd.iloc[x]["prcp"],
        tobs = measure_pd.iloc[x]["tobs"])
    # Add measurement(x) to the current session
    session.add(measurement)
    # Commit object to the database
    session.commit()
```


```python
# Query the database, see if we got all the values from the csv
station_list = session.query(Station)
counter_s = 0
for station in station_list:
    counter_s = counter_s + 1
print(counter_s)
```

    9
    


```python
# Query the database, see if we got all the values from the csv
measurement_list = session.query(Measurement)
counter_m = 0
for measurement in measurement_list:
    counter_m = counter_m + 1
print(counter_m)
```

    18103
    
