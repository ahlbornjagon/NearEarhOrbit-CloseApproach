"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file."""
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        csv_writer.writerow(fieldnames)
        for approach in results:
            row = [
                approach.time_str,  
                approach.distance,  
                approach.velocity,  
                approach.neo.designation, 
                approach.neo.name or '',  
                approach.neo.diameter or 'nan', 
                approach.neo.hazardous,  
            ]
            csv_writer.writerow(row)

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file."""
    data = [approach.serialize() for approach in results]
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)