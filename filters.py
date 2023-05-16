"""A module to define filters that can be applied by the user to all objects in database."""
import operator
from operator import le, ge, eq

class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""

class AttributeFilter:
    """A class to define the filters used to query certian objects within the databse.
    
    Querying is done based on the attributes defined for each object.
    """
    
    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value
    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get the attributes of the object that we are interested in.
        
        Returns the attributes, or error.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Get the operator and value of the current object."""
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters that we will use to query the entire database of objects.
    
    Check each attribute and appends to an updating list if object fits the criteria.
    """
    filters = []
    if date is not None:
        filters.append(DateFilter(le, date))
        filters.append(DateFilter(ge, date))
    if start_date is not None:
        filters.append(DateFilter(ge, start_date))
    if end_date is not None:
        filters.append(DateFilter(le, end_date))

    if distance_min is not None:
        filters.append(DistanceFilter(ge, distance_min))
    if distance_max is not None:
        filters.append(DistanceFilter(le, distance_max))

    if velocity_min is not None:
        filters.append(VelocityFilter(ge, velocity_min))
    if velocity_max is not None:
        filters.append(VelocityFilter(le, velocity_max))

    if diameter_min is not None:
        filters.append(DiameterFilter(ge, diameter_min))
    if diameter_max is not None:
        filters.append(DiameterFilter(le, diameter_max))

    if hazardous is not None:
        filters.append(HazardousFilter(eq, hazardous))
    
    return (filters)


class DateFilter(AttributeFilter):
    """Class that defines the date filter.
    
    Inherits from Attribute Filter class, filters all data based on date passed in by user.
    """

    @classmethod
    def get(cls, approach):
        """Get attributes for object.
        
        Returns filtered objects.
        """
        return approach.time.date()

class DistanceFilter(AttributeFilter):
    """Class that defines the distance filter.
    
    Inherits from Attribute Filter class, filters all data based on distance passed in by user.
    """

    @classmethod
    def get(cls, approach):
        """Get attributes for object.
        
        Returns filtered objects.
        """
        return approach.distance

class VelocityFilter(AttributeFilter):
    """Class that defines the velocity filter.
    
    Inherits from Attribute Filter class, filters all data based on velocity passed in by user.
    """

    @classmethod
    def get(cls, approach):
        """Get attributes for object.
        
        Returns filtered objects.
        """
        return approach.velocity

class DiameterFilter(AttributeFilter):
    """Class that defines the diameter filter.
    
    Inherits from Attribute Filter class, filters all data based on diamter passed in by user.
    """

    @classmethod
    def get(cls, approach):
        """Get attributes for object.
        
        Returns filtered objects.
        """
        return approach.neo.diameter

class HazardousFilter(AttributeFilter):
    """Class that defines the hazzardous filter.
    
    Inherits from Attribute Filter class, filters all data based on hazardous boolean passed in by user.
    """

    @classmethod
    def get(cls, approach):
        """Get attributes for object.
        
        Returns filtered objects.
        """
        return approach.neo.hazardous

def limit(iterator, n=None):
    """Produce an iterator depending on if none or "n" value is provied to it.
    
    Returns a generated iterator or none.
    """
    if n is None or n<=0:
        for item in iterator:
            yield item
    else:
        count = 0
        for item in iterator:
            if count<n:
                yield item
                count += 1
            else:
                break

    return iterator
