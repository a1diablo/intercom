import unittest
from nearby_customers import NearbyCustomers
from distance import Distance


class NearbyCustomersTestCase(unittest.TestCase):
    def setUp(self):
        self.nearby_customers = NearbyCustomers()

    def test_load_config_from_file(self):
        self.nearby_customers.load_config_from_file('config.json')
        self.assertIsNotNone(self.nearby_customers.match_radius_km)

    def test_load_customers_from_file(self):
        self.nearby_customers.load_customers_from_file('customers.txt')
        self.assertIsNotNone(self.nearby_customers.customers)

    def check_distance(self, near_customers):
        for customer in near_customers:
            self.assertLessEqual(Distance().calculate_from_coordinates_in_degrees(
                self.nearby_customers.office_lat, self.nearby_customers.office_long,
                float(customer['latitude']), float(customer['longitude'])), self.nearby_customers.match_radius_km)

    def test_get(self):
        self.nearby_customers = NearbyCustomers('config.json', 'customers.txt')
        near_customers = self.nearby_customers.get()
        self.check_distance(near_customers)

    def test_get_for_big_customer_data(self):
        self.nearby_customers = NearbyCustomers('config.json')
        near_customers = self.nearby_customers.get_for_big_customer_data(
            'customers.txt')
        self.check_distance(near_customers)


class DistanceTestCase(unittest.TestCase):
    def test_degree_to_radian(self):
        self.assertEqual(Distance().degree_to_radian(180), Distance().pi)

    def test_calculate_from_coordinates_in_degree(self):
        self.assertLessEqual(abs(Distance().calculate_from_coordinates_in_degrees(
            53.339428, -6.257664, 52.986375, -6.043701) - 41.816), 0.1)
