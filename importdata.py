import csv

from pymongo import MongoClient

DB_NAME = 'worldHappiness'
FIG_COLLECTION_NAME = 'fig'
TABLE_COLLECTION_NAME = 'table'
FIG_DATA_FILENAME = 'back_end/resources/world-happiness-fig-2024.csv'
TABLE_DATA_FILENAME = 'back_end/resources/world-happiness-table-2024.csv'

mongo = MongoClient(port=27017)


def load_csv_into_mongo(filename, db_name, collection_name):
    """Load data from a CSV file into a mongo collection."""
    clear_mongo_collection(db_name, collection_name)
    insert_into_mongo(load_csv_data(filename), db_name, collection_name)


def load_csv_data(filename):
    """Load data from a CSV file into a list of dicts.
    
    Insures that numeric fields are converted to numeric types as needed.  In
    particular, it converts 'year' field values to `int` and other non-text
    fields to `float`.
    
    """
    with open(filename, 'r', encoding='utf-8-sig') as fig_data_file:
        reader = csv.reader(fig_data_file)
        raw_data = list(reader)
        header, rows = raw_data[0], raw_data[1:]
        data = [
            {key: value for key, value in zip(header, row)}
            for row in rows
        ]
    parsed_data = []
    for row in data:
        parsed_row = {}
        for key, value in row.items():
            try:
                if key == 'year':
                    value = int(value)
                else:
                    value = float(value)
            except:
                pass
            parsed_row[key] = value
        parsed_data.append(parsed_row)
    return parsed_data


def clear_mongo_collection(db_name, collection_name):
    """Clear out a mongo collection."""
    db = mongo[db_name]
    collection = db[collection_name]
    collection.delete_many({})


def insert_into_mongo(data, db_name, collection_name):
    """Insert data into a mongo collection."""
    db = mongo[db_name]
    collection = db[collection_name]
    collection.insert_many(data)


def import_data():
    """Import CSV files into our mongo database collections."""
    load_csv_into_mongo(FIG_DATA_FILENAME, DB_NAME, FIG_COLLECTION_NAME)
    load_csv_into_mongo(TABLE_DATA_FILENAME, DB_NAME, TABLE_COLLECTION_NAME)


if __name__ == '__main__':
    import_data()
