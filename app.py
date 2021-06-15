#Flask
from flask import Flask, jsonify
from flask.app import Flask
#sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql.elements import between

#Setup engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)
# Save references to each table
measurements = base.classes.measurement
stations= base.classes.station

#Flask
app = Flask(__name__)

#Routes
#/
@app.route("/")
def Home():
    "Listing All Routes Available for Climate App"
    return(
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start> <br/>'
        f'/api/v1.0/<start>/<end> <br/>'
    )
#/precipitation
@app.route('/api/v1.0/precipitation')
def Precipitation():

    #Engine session
    session = Session(engine)

    #query for precipitation data
        #grab same query as ipynb for the last year of precipitation
    precipitationQuery = session.query(measurements.date, measurements.prcp).filter(measurements.date.between('2016-08-23','2017-08-23'))
    #iterate over rows to convert from query object to dictionary
    precipitationDict = {date: prcp for date, prcp in precipitationQuery}
    return jsonify(precipitationDict)

#/stations
@app.route('/api/v1.0/stations')
def Stations():
    #Engine session
    session = Session(engine)

    #query for stations and us ".all()" to convert query to list format
    stationsQuery = session.query(stations.station).all()

    return jsonify(stationsQuery)

#/tobs
@app.route('/api/v1.0/tobs')
def Tobs():
    #Engine session
    session = Session(engine)

    #Most active station from ipynb
    mostActiveStation = 'USC00511918'

    #Query for most active station
    mostActiveQuery = session.query(measurements.date, measurements.tobs).filter(measurements.date.between('2016-08-23','2017-08-23')).filter(measurements.station == mostActiveStation)
    
    #iterate over rows to convert from query object to dictionary
    mostActiveDict = {date:tobs for date , tobs in mostActiveQuery}

    return jsonify(mostActiveDict)

#/start
@app.route('api/v1.0/temp/<start>')
def Dynamic(start):
    #Engine session
    session = Session(engine)

    #Query for start date summary
    lowestQuery = session.query(func.min(measurements.tobs)).filter(measurements.date >= start).all()
    highestQuery = session.query(func.max(measurements.tobs)).filter(measurements.date >= start).all()
    averageQuery = session.query(func.avg(measurements.tobs)).filter(measurements.date >= start).all()

    #query results to jsonify- able format and return
    summary = {"lowest temp" :lowestQuery[0], "highest temp":highestQuery[0],"average temp": averageQuery[0]}
    return jsonify(summary)

@app.route('api/v1.0/temp/<start>/<end>')
def Dynamic(start, end):
    #Engine session
    session = Session(engine)

    #Query for start and end date summary
    lowestQuery = session.query(func.min(measurements.tobs)).filter(measurements.date.between(start, end)).all()
    highestQuery = session.query(func.max(measurements.tobs)).filter(measurements.date.between(start, end)).all()
    averageQuery = session.query(func.avg(measurements.tobs)).filter(measurements.date.between(start, end)).all()

    #query results to jsonify- able format and return
    summary = {"lowest temp" :lowestQuery[0], "highest temp":highestQuery[0],"average temp": averageQuery[0]}
    return jsonify(summary)
    

if __name__ == '__main__':
    app.run(debug=True)