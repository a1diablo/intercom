# intercom

Take home test for intercom job application

Python version tested: Python 3.8.0

Run the below command to run with default options

```
python nearby_customers.py
```

Run this to run the tests

```
python -m unittest
```

Full options:
```
usage: nearby_customers.py [-h][--config config] [--customers CUSTOMERS]

Find nearby customers from office

optional arguments:
-h, --help show this help message and exit
--config CONFIG Path of the config file to be used.
--customers CUSTOMERS Path of the customers file to be used.
```

Sample config.json already checked in

```
{
  "office_location": "53.339428, -6.257664",
  "match_radius_km": "100"
}
```

Sample customers.txt and output.txt are added to the repository
