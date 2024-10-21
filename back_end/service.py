import argparse
import csv
import logging

from flask import Flask, abort, jsonify, make_response
from pymongo import MongoClient

from util import *


FLASK_JSON_SORT_KEYS = False

logger = logging.getLogger()
app = Flask(__name__)
app.json.sort_keys = FLASK_JSON_SORT_KEYS


@app.route('/api/country')
def get_countries():
    """Get a list of countries.
    
    Returns:
        A flask response with a list of countries as a flask response containing
        json for th
    data = get_country_locations_from_csv()
    if data:
        return jsonify(sorted(data.keys()))
    else:
        abort(500)


@app.route('/api/country/<country>/location')
def get_country_location(country):
    """Get location of a country as lat/lon coordinates
    
    Gets a data structure with the coordinates for each country, and returns the
    coordinates of the given country as a GeoJSON object with a Point geometry.
    
    Args:
        country_name (str): Name of the country
    
    Returns:
        A flask response containing the country and its location as a GeoJSON
        object.
    
    """
    try:
        locations = get_country_locations_from_csv()
        location = locations.get(country, None)
        if location:
            latitude, longitude = location['latitude'], location['longitude']
            
            response = jsonify(dict(
                country=country,
                latitude=latitude,
                longitude=longitude,
            ))
            
            return response
        else:
            abort(500)
    except Exception as e:
        logger.exception(f'Error getting location for {country=!r}.')
        abort(500)


@memoized  # Memoize this so the CSV is only read once
def get_country_locations_from_csv():
    """Get country locations from a CSV file
    
    Returns:
        A dict mapping country name to a dict with country name, latitude, and
        longitude, for example:
        
        {
            "United States": {
                "country": {
                    "name": "United States"
                },
                "location": {
                    "latitude": 37.0902,
                    "longitude": -95.7129
                }                
            }
        }
    
    """
    csv_filename = 'resources/country-coordinates.csv'
    csv_fields = ('Country name', 'latitude', 'longitude')

    # Load raw data from csv
    csv_data = load_utf8_csv(csv_filename)
    if not csv_data:
        raise RuntimeError(f'Could not get country coords from {csv_filename}')
    
    # Validate expected field names
    for row in csv_data:
        for field in csv_fields:
            assert field in row.keys()
    
    # Rename fields
    csv_data = rename_fields(csv_data, {
        'Country name': 'country',
    })

    # Return a mapping of country names to lat/lon coordinate tuples
    if csv_data:
        country = row['country']
        latitude, longitude = float(row['latitude']), float(row['longitude'])
        country_locations = {
            country: {
                "country": {
                    "name": country,
                },
                "location": {
                    "latitude": latitude,
                    "longitde": longitude,
                },
            }
            for row in csv_data
        }
        return country_locations
    else:
        raise RuntimeError(
            f'Could not get country locations data from {csv_filename}'
        )


def init_logging():
    """Initialize logging."""
    logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    init_logging()
    app.run(debug=True)
