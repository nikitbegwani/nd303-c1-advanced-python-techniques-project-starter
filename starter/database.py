from models import OrbitPath, NearEarthObject
import csv


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.

        self.filename = filename
        
        self.obj_name = {}
        self.obj_date = {}


    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.

        # TODO: Where will the data be stored?

        fp_open = open(filename, 'r')

        obj_data = csv.DictReader(fp_open)

        for entry in obj_data:
            orbit_path = OrbitPath(**entry)

            if self.obj_name.get(entry['name'], None) is None:
                self.obj_name[entry['name']] = NearEarthObject(**entry)

            if self.obj_date.get(entry['close_approach_date'], None) is None:
                self.obj_date[entry['close_approach_date']] = []

            neo = self.obj_name.get(entry['name'], None)            
            neo.update_orbits(orbit_path)

            self.obj_date[entry['close_approach_date']].append(neo)

        return None