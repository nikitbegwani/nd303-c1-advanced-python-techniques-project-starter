class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """

        self.orbits = []
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', 'Name not Found')
        self.diameter_min_km = float(kwargs.get('estimated_diameter_min_kilometers', 0))
        self.is_potentially_hazardous_asteroid = kwargs.get('is_potentially_hazardous_asteroid', False)


    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        # TODO: How do we connect orbits back to the Near Earth Object?

        self.orbits.append(orbit)

    def __repr__(self):
        return f'Object id {self.id} with name {self.name} \
                                    orbits: {[orbit.name for orbit in self.orbits]} \
                                    with orbit_dates:{[orbit.close_approach_date for orbit in self.orbits]}'


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # Instance variables are used for storing on the Near Earth Object!
        self.neo_name = kwargs.get('name', None)
        self.miss_distance_kilometers = float(kwargs.get('miss_distance_kilometers', 0))
        self.close_approach_date = kwargs.get('close_approach_date', None)

    def __repr__(self):
        return f'Object {self.neo_name} missed earth on {self.close_approach_date} \
                                    by {self.miss_distance_kilometers} kms'