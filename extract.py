"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function will extract NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function will extract close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.
"""
import csv
import json
from helpers import cd_to_datetime, datetime_to_str
from models import NearEarthObject, CloseApproach
def load_neos(neo_csv_path):
    """Will Read in near earth data from the supplied csv file. Adds all items to a dictionary, mapping the following values to keywords.
    
    The keyworda are primary designations, name, diameter, and whether it is a threat or not (pha). Function returns these NEO objects
    """
    with open(neo_csv_path, 'r') as file:
        reader = csv.DictReader(file)
        neos= []
        for row in reader:
            designation = row['pdes']
            name = row['name'] if row['name'] else None
            diameter = float(row['diameter']) if row['diameter'] else float('nan')
            hazardous = True if row['pha'] == 'Y' else False
            neo = NearEarthObject(designation=designation, name=name, diameter=diameter, hazardous=hazardous)
            neos.append(neo)
    return neos


def load_approaches(cad_json_path):
    """Read in close approach data from supplied JSON file, stores it in a dictionary linking the following keywords to values.

    Values are designation, time, distance, and velocity. Returns Close approach items.
    """
    with open(cad_json_path, 'r') as file:
        data = json.load(file)
    cas = []
    for approach in data['data']:
        des = approach[0]
        time = (approach[3])
        distance = float(approach[4])
        velocity = float(approach[7])
        ca = CloseApproach(designation=des,
                           time=time,
                           distance=distance,
                           velocity=velocity)
        cas.append(ca)
    return cas
