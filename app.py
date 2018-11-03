import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/start_date<br/>"
        f"----- Example: /api/v1.0/2018-11-01<br/>"
        f"<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"----- Example: /api/v1.0/2018-11-01/2018-11-30<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return a list of all dates and prcp"""
    # Convert the query results to a Dictionary using date as the key and prcp as the value.

    results = session.query(Measurement).all()

    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["Date"] = measurement.date
        measurement_dict["Prcp"] = measurement.prcp

        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():

    """Return a JSON list of stations from the dataset."""

    all_stations = session.query(Station.station).all()

    all_stations_1 = list(np.ravel(all_stations))

    return jsonify(all_stations_1)

@app.route("/api/v1.0/tobs")
def tobs():

    """Return a JSON list of Temperature Observations (tobs) for the previous year."""

    #query for the dates and temperature observations from a year from the last data point.

    temp = session.query(Measurement.tobs).\
                filter(Measurement.date > '2016-08-23').\
                order_by(Measurement.date ).all()


    temps = list(np.ravel(temp))

    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def start(start):

    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
   
    result = []
    Amin = {}

    minimum = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    minimum = list(np.ravel(minimum))
    Amin['min']= minimum[0]

    average = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date).all()
    average = list(np.ravel(average))
    Amin['avg']= average[0]

    maximum = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    maximum = list(np.ravel(maximum))
    Amin['max']= maximum[0]
    
    result.append(Amin)

    
    return jsonify(result)


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()

    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()

    
    result1 = []
    Amin1 = {}

    minimum = session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).all()
    minimum = list(np.ravel(minimum))
    Amin1['min']= minimum[0]

    average = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date.between(start_date, end_date)).all()
    average = list(np.ravel(average))
    Amin1['avg']= average[0]

    maximum = session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).all()
    maximum = list(np.ravel(maximum))
    Amin1['max']= maximum[0]
    
    result1.append(Amin1)
    
    
    return jsonify(result1)


if __name__ == '__main__':
    app.run(debug=True)