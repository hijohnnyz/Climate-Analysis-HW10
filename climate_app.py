# Import dependecies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Create engine and save table references
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask setup
app = Flask(__name__)

# Available routes
@app.route('/')
def home():
    return (
        """<h1>Routes for Climate Analysis</h1><br/>"""
        """<a href="/api/v1.0/stations">List of Stations</a><br/>"""
        """<a href="/api/v1.0/tobs">Temperature Observations</a><br/>"""
        """<a href="/api/v1.0/precipitation">Precipitation</a><br/>"""
        """<a href="/api/v1.0/2017-08-13/2017-08-23">Temperatures in Date Range</a><br/>"""
        )

@app.route('/api/v1.0/precipitation')
def precipitation():
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    pcp = list(np.ravel(precipitation))
    return (jsonify(precipitation))

@app.route('/api/v1.0/stations')
def station():
    station_list = session.query(Measurement.station, Station.name).filter(Measurement.station == Station.station).http://127.0.0.1:5000/group_by(Measurement.station).all()
    stations = list(np.ravel(station_list))
    return (jsonify(stations))

@app.route('/api/v1.0/tobs')
def tobs():
    max_date = session.query(Measurement.date).order_by(Measurement.date).first()
    max_date = max_date[0]
    past_year = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=365)
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= past_year).all()
    temps_list = list(temps)
    return(jsonify(temps_list))

@app.route('/api/v1.0/<start>')
def start(start=None):
    date1 = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    date1_list = list(date1)
    return(jsonify(date1_list))

@app.route('/api/v1.0/<start>/<end>')
def sta_end(start=None, end=None):
    trip = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    trip_list=list(trip)
    return jsonify(trip_list)

if __name__ == "__main__":
    app.run(debug=True)
