"""A database encapsulating collections of near-Earth objects and their close approaches."""
class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`."""
        self._neos = {}
        self._approaches = approaches
        self._neo_names = {}

        for neo in neos:
            self._neos[neo.designation] = neo
            if neo.name:
                self._neo_names.setdefault(neo.name, []).append(neo)

        for approach in self._approaches:
            for neo in self._neos.values():
                if neo.designation == approach._designation:
                    approach.neo = neo
                    neo.approaches.append(approach)
                    break

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.
        """
        return self._neos.get(designation, None)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.
        """
        for neo in self._neos.values():
            if neo.name == name:
                return neo
        return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.
        """
        for approach in self._approaches:
            if all(filter(approach)for filter in filters):
                yield approach
