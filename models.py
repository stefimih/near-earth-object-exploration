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


class NearEarthObject:
    """A near-Earth object (NEO)."""

    def __init__(self, **info):
        """Create a new `NearEarthObject`."""
        self.designation = info.get('designation', '').strip()
        self.name = info.get('name') or None
        self.diameter = float(info.get('diameter', 'nan')) if info.get('diameter') else float('nan')
        self.hazardous = info.get('hazardous', 'N').strip().upper() == 'Y'

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def __str__(self):
        """Return `str(self)`."""
        hazardous_text = "is potentially hazardous" if self.hazardous else "is not potentially hazardous"
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {hazardous_text}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO."""

    def __init__(self, **info):
        """Create a new `CloseApproach`."""
        self._designation = info.get('_designation') or info.get('designation')
        self.time = cd_to_datetime(info.get('time') or info.get('cd'))
        self.distance = float(info.get('distance') or info.get('dist'))
        self.velocity = float(info.get('velocity') or info.get('v_rel'))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (f"On {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance "
                f"of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
