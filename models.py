"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
from datetime import datetime

class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **kwargs):
        """Create a new NearEarthObject.

        A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = kwargs['designation']
        self.name = kwargs['name']
        self.diameter = float(kwargs['diameter'])
        self.hazardous = bool(kwargs['hazardous'])

        if (kwargs['name'] == ''):
            self.name == None
        if (kwargs['diameter'] == ''):
            self.diameter == float('nan')


        # Create an empty initial collection of linked approaches. -----> DONE
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        name = self.name
        return (name)

    def __str__(self):
        """Return `str(self)`."""
        return f"A NearEarthObject ...{self.name}, diameter = {self.diameter}, is it hazardous? {self.hazardous}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """Return serialized data for current object."""
        return {
            'designation': self.designation,
            'name': self.name,
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` will encapsulate information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def serialize(self):
        """Return serialized data for current object."""
        return {
            'datetime_utc': self.time_str, 
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': self.neo.serialize()  
        }
    def __init__(self, **kwargs):
        """Create a new initialization for an approach object. Maps read values to the following keywords.

        Designation, distance, velocity, and converts the time.
        """
        self._designation = kwargs['designation']
        self.distance = kwargs['distance']
        self.velocity = kwargs['velocity']

        if kwargs['distance'] == '':
            self.distance == float('nan')
        if kwargs['velocity'] == '':
            self.velocity == float('nan')
        try:
    # Parse the time string using datetime.strptime
            self.time = cd_to_datetime(kwargs['time'])  # Use the cd_to_datetime function for this attribute.
        except ValueError as e:
    # Handle the case where the time string is not in the correct format
            self.time = None

    @property
    def time_str(self):
        """Convert a date time object into a string to be used for the other methods in the project, especially when querying the database."""
        return datetime_to_str(self.time)
        
    
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        name = self.name
        return (name)
        

    def __str__(self):
        """Return the human readable values of the close approach object."""
        return f"A CloseApproach ...designation = {self._designation}, distance = {self.distance}, velocity= {self.velocity}"

    def __repr__(self):
        """Return the computer readable string version of the close approach object. ."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
