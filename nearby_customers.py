import json
import sys
import argparse
from distance import Distance


class NearbyCustomers:

    def __init__(self, config_path=None, customer_path=None):
        if config_path:
            self.load_config_from_file(config_path)
        if customer_path:
            self.load_customers_from_file(customer_path)

    def load_customers_from_file(self, customer_file):
        try:
            with open(customer_file) as fp:
                customers_data = fp.readlines()
        except FileNotFoundError as ex:
            sys.exit(f'Customer file {customer_file} not found: {ex}')

        self.customers = []
        for customer_json in customers_data:
            try:
                self.customers.append(json.loads(customer_json))
            except ValueError as ex:
                print(f'Invalid customer {customer_json}: {ex}')
                print('Continuing with next customer...')

    def load_config_from_file(self, config_file):
        try:
            with open(config_file) as fp:
                config = json.load(fp)
                self.office_lat, self.office_long = map(
                    lambda x: float(x), config['office_location'].split(','))
                self.match_radius_km = float(
                    config.get('match_radius_km', 100))
        except FileNotFoundError as ex:
            sys.exit(f'Config file {config_file} not found: {ex}')
        except ValueError as ex:
            sys.exit(f'Invalid config from {config_file} detected: {ex}')
        except KeyError as ex:
            sys.exit(
                f'Invalid config from {config_file} detected: Key {ex} is not present')

    def get(self):
        self.nearby_customers = [customer for customer in self.customers
                                 if Distance().calculate_from_coordinates_in_degrees(
                                     self.office_lat, self.office_long,
                                     float(customer['latitude']), float(customer['longitude']))
                                 <= self.match_radius_km]

        self.nearby_customers.sort(key=lambda cust: int(cust['user_id']))
        return self.nearby_customers

    # This is an alternate sample implementation in case the customers file is too big
    # and we want to process customers line by line rather than storing them
    # into one big list which could lead to huge memory consumption.
    def get_for_big_customer_data(self, customer_file):
        self.nearby_customers = []
        with open(customer_file) as fp:
            for customer_json in fp:
                customer = json.loads(customer_json)
                if Distance().calculate_from_coordinates_in_degrees(
                        self.office_lat, self.office_long, float(customer['latitude']), float(customer['longitude'])) <= self.match_radius_km:
                    self.nearby_customers.append(customer)

        self.nearby_customers.sort(key=lambda cust: int(cust['user_id']))
        return self.nearby_customers

    @classmethod
    def show_one(cls, customer):
        print(json.dumps(
            {'name': customer['name'], 'user_id': customer['user_id']}))


parser = argparse.ArgumentParser(
    description='Find nearby customers from office')
parser.add_argument('--config', action='store', default='config.json',
                    help='Path of the config file to be used.')
parser.add_argument('--customers', action='store', default='customers.txt',
                    help='Path of the customers file to be used.')
args = parser.parse_args()

if __name__ == "__main__":
    nearby_customers = NearbyCustomers(args.config, args.customers).get()
    # Comment the above line and uncomment the below line to process big files
    # nearby_customers = NearbyCustomers(args.config).get_for_big_customer_data(args.customers)
    for customer in nearby_customers:
        NearbyCustomers.show_one(customer)
