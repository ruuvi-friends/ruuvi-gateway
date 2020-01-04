import dateutil.parser
from collections import defaultdict

class RuuviDatapoint: 
    """
    Encapsulates the data in a standard format in case the API changes
    """
    @classmethod
    def sort_datapoint_list(klass, datapoint_list):
        return sorted(
            datapoint_list, 
            key=lambda x: x.timestamp, 
            reverse=True
        )

    @classmethod
    def group_by_tagid(klass, datapoint_list):
        grouped_tags = defaultdict(list)

        for datapoint in datapoint_list:
            grouped_tags[datapoint.tag_data['tag_id']].append(datapoint)

        return grouped_tags

    def __init__(self, iso_timestamp, tag_data, sender_data, sensor_data):
        # Todo JSON validate the data
        self.iso_timestamp = iso_timestamp
        self.timestamp = dateutil.parser.parse(iso_timestamp)
        self.tag_data = tag_data
        self.sender_data = sender_data
        self.sensor_data = sensor_data