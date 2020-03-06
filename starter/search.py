from collections import namedtuple
from enum import Enum

from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath

import operator
from collections import defaultdict


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?

        self.return_object = kwargs.get('return_object')
        self.date = kwargs.get('date')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')        
        self.number = kwargs.get('number')
        self.filter = kwargs.get('filter')
        

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        if self.date:
            date_search = Query.DateSearch(DateSearch.equals, self.date)
        else:
            date_search = Query.DateSearch(DateSearch.between, [
                self.start_date, self.end_date])

        return_object = Query.ReturnObjects.get(self.return_object)

        # Initialize filters to None for case of no filters
        filters=[]

        if self.filter:
            # Create Filter Object if filter is enabled
            options = Filter.create_filter_options(self.filter)

            for key, val in options.items():
                for each_filter in val:
                    filter_properties = each_filter.split(":")
                    # Append each filter
                    filters.append(Filter(filter_properties[0], key, filter_properties[1], filter_properties[2]))

        return Query.Selectors(date_search, self.number, filters, return_object)


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # Create a dict of filter name to the NearEarthObject or OrbitalPath property
        'diameter': 'diameter_min_km',
        'distance': 'miss_distance_kilometers',
        'is_hazardous': 'is_potentially_hazardous_asteroid'
    }

    Operators = {
        #Create a dict of operator symbol to an Operators method, see README Task 3 for hint

        "=": operator.eq,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        filter_dict = defaultdict(list)

        for each_filter in filter_options:
            filter_name = each_filter.split(':')[0]  

            if hasattr(NearEarthObject(), Filter.Options.get(filter_name)):
                filter_dict['NearEarthObject'].append(each_filter)

            elif hasattr(OrbitPath(), Filter.Options.get(filter_name)):
                filter_dict['OrbitPath'].append(each_filter)

        return filter_dict


    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results


        filtered_neos = []

        for neo in results:
            
            field = Filter.Options.get(self.field)
            operation = Filter.Operators.get(self.operation)
            value = getattr(neo, field)

            try:
                if operation(value, self.value):
                    filtered_neos.append(neo)
            except:
                if operation(str(value), str(self.value)):
                    filtered_neos.append(neo)

        return filtered_neos


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # Instance variable can we use to connect DateSearch 
        self.obj_date = dict(db.obj_date)
        self.obj_name = dict(db.obj_name)
        self.date_search = None

    def get_objects(self, query):
   
        #Date Search Filter

        self.date_search = query.date_search.type
        dates = query.date_search.values
        
        neos = []

        for key, value in self.obj_date.items():
            
            if self.date_search == DateSearch.equals:            
                if key == dates:
                    neos.extend(value)

            elif self.date_search == DateSearch.between:
                if key >= dates[0] and key <= dates[1]:
                    neos.extend(value)

        # Distance Filter

        distance_filter = None
        orbits = []

        for each_filter in query.filters:

            if each_filter.field == 'distance':
                distance_filter = each_filter
                continue

            neos = each_filter.apply(neos)
        
        for neo in neos:
            orbits.extend(neo.orbits)


        filtered_orbits = orbits
        filtered_neos = neos

        if distance_filter:
            filtered_orbits = distance_filter.apply(orbits)
            filtered_neos = [self.obj_name.get(orbit.neo_name) for orbit in filtered_orbits]

        filtered_neos = list(set(filtered_neos))
        filtered_orbits = list(set(filtered_orbits))

        filter_number = int(query.number)

        if query.return_object == OrbitPath:
            return filtered_orbits[:filter_number ]

        return filtered_neos[: filter_number]