import argparse
import logging

from flask import Flask, abort, jsonify, request, make_response
from flask_cors import CORS
from pymongo import MongoClient

from util import *


FLASK_JSON_SORT_KEYS = False
DEFAULT_FLASK_PORT = 5000
DEFAULT_MONGO_PORT = 27017
DEFAULT_MONGO_HOST = 'localhost'
DEFAULT_MONGO_DB = 'worldHappiness'

logger = logging.getLogger()
app = Flask(__name__)
mongo = MongoClient(f'mongodb://{DEFAULT_MONGO_HOST}:{DEFAULT_MONGO_PORT}/')


@app.route('/api/years')
def get_years():
    """Get sorted years from the mongo worldHappiness table collection."""
    try:
        db = mongo[DEFAULT_MONGO_DB]
        collection = db['table']
        years = sorted(collection.distinct('year'))
        response = jsonify(years)
        return response
    except Exception as e:
        logger.exception(f'Error getting years.')
        abort(500)


@app.route('/api/country')
def get_countries():
    """Get sorted countries from the mongo worldHappiness collections."""
    countries = set()    
    try:
        db = mongo[DEFAULT_MONGO_DB]
        for collection_name in ('fig', 'table'):
            collection = db[collection_name]
            countries.update(collection.distinct('Country name'))
        countries = sorted(countries)
        response = jsonify(countries)
        return response
    except Exception as e:
        logger.exception(f'Error getting countries.')
        abort(500)


@app.route('/api/country/location')
def get_country_locations():
    """Get country locations from CSV file."""
    locations_filename = 'resources/country_coordinates.csv'
    try:
        location_data = load_utf8_csv(locations_filename)
        locations = {
            loc['Country name']: (loc['latitude'], loc['longitude'])
            for loc in location_data
        }
        return jsonify(locations)
    except Exception as e:
        logger.exception(f'Error getting country locations.')
        abort(500)


@app.route('/api/country/geojson')
def get_country_borders():
    """Get country borders from a GeoJSON file."""
    geojson_filename = 'resources/countries.geo.json'
    try:
        with open(geojson_filename, 'r', encoding='utf-8-sig') as geojson_file:
            geojson = geojson_file.read()
        response = make_response(geojson)
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        logger.exception(f'Error getting country borders.')
        abort(500)


@app.route('/api/table')
def get_table_collection():
    """Get the table collection from mongo."""
    try:
        db = mongo[DEFAULT_MONGO_DB]
        collection = db['table']
        table = list(collection.find({}, {'_id': 0}))
        response = jsonify(table)
        return response
    except Exception as e:
        logger.exception(f'Error getting table collection.')
        abort(500)


@app.route('/api/table/year/<int:year>')
def get_table_for_year(year):
    """Get values from the table collection from mongo for a year."""
    try:
        db = mongo[DEFAULT_MONGO_DB]
        collection = db['table']
        table = list(collection.find({'year': year}, {'_id': 0}))
        response = jsonify(table)
        return response
    except Exception as e:
        logger.exception(f'Error getting table values for year {year}.')
        abort(500)


def init_logging():
    """Initialize logging."""
    logging.basicConfig(level=logging.DEBUG)


def run_flask_app(opts):
    """Initialize the flask app"""
    app.json.sort_keys = FLASK_JSON_SORT_KEYS
    CORS(app, resources={r'/api/*': {'origins': opts.flask_cors_origin}})
    app.run(debug=True, port=opts.flask_port)


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port', '--flask-port',
        type=int,
        dest='flask_port',
        default=DEFAULT_FLASK_PORT,
    )
    parser.add_argument(
        '--flask-cors-origin', '--cors-origin',
        type=str,
        dest='flask_cors_origin',
        default='*',
    )
    
    return parser.parse_args()


def main():
    """Set up and run the flask service."""
    init_logging()
    opts = get_opts()
    run_flask_app(opts)

    return 0


if __name__ == "__main__":
    exit(main())
