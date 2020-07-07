import math


class Distance:

    def __init__(self):
        self.pi = 3.141592653589793238
        self.radius_of_earth_in_km = 6371

    def degree_to_radian(self, degree):
        return degree * self.pi / 180

    def calculate_from_coordinates_in_degrees(self, lat1, long1, lat2, long2):
        # Computes the distance between two coordinates of earth by calculating
        # the Great Circle Distance (https://en.wikipedia.org/wiki/Great-circle_distance)
        # A special case of Vincenty formula is used which is expected to fairly accurate for all distances

        lat1 = self.degree_to_radian(lat1)
        long1 = self.degree_to_radian(long1)
        lat2 = self.degree_to_radian(lat2)
        long2 = self.degree_to_radian(long2)

        delta_long = abs(long1 - long2)

        central_angle = math.atan(math.sqrt((math.cos(lat2) * math.sin(delta_long)) ** 2 +
                                            (math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_long)) ** 2)
                                  / (math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(delta_long)))

        return self.radius_of_earth_in_km * central_angle
