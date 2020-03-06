from enum import Enum
import csv


class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from supported output formatting options.
    """

    def __init__(self):
        # TODO: How can we use the OutputFormat in the NEOWriter?
        self.formats = OutputFormat.list()

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """

        if format == self.formats[0]:
            print(data)

            return True

        elif format == self.formats[1]:
            
            fp_open = open('data/results.csv', 'w', newline='')
            writer = csv.DictWriter(fp_open, fieldnames=['id', 'name', 'diameter_min_km', 'orbits', 'orbit_dates'])
            writer.writeheader()

            for neo_object in data:
                writer.writerow({'id': neo_object.id, 'name': neo_object.name, \
                                'diameter_min_km': neo_object.diameter_min_km, \
                                'orbits': [orbit.neo_name for orbit in neo_object.orbits], \
                                'orbit_dates': [orbit.close_approach_date for orbit in neo_object.orbits]  })
            return True

        else:
            return False
                