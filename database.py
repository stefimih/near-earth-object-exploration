"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

class NEODatabase:
    """A database of near-Earth objects and their close approaches."""

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # Create lookup dictionaries for designations and names.
        self._neos_by_designation = {neo.designation: neo for neo in neos}
        self._neos_by_name = {neo.name: neo for neo in neos if neo.name}

        # Link together the NEOs and their close approaches.
        for approach in approaches:
            neo = self._neos_by_designation.get(approach._designation)
            approach.neo = neo
            if neo:
                neo.approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation."""
        return self._neos_by_designation.get(designation)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name."""
        return self._neos_by_name.get(name)

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters."""
        for approach in self._approaches:
            if all(f(approach) for f in filters):
                yield approach
