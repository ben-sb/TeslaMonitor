from classes.cars import Car
from datetime import datetime
import requests
import random
import time

class Monitor:

    def __init__(self, model, condition, delay_in_seconds):
        self.model = model
        self.condition = condition
        self.delay = delay_in_seconds
        self.api_url = "https://www.tesla.com/api.php"
        self.query_params = {
            'm': 'tesla_cpo_marketing_tool',
            'a': 'inventory_search',
            'query': self.build_query()
        }
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://www.tesla.com/en_GB/inventory/new/' + self.model,
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }
        self.cars = []


    def log(self, msg):
        print('[{}]: {}'.format(datetime.now(), msg))


    def build_query(self):
        longitude = (-1 * random.randint(10000, 30000))/10000
        latitude = random.randint(500000, 560000)/10000

        return '{"query":{"model":"' + self.model + '","condition":"' + self.condition + '","options":{},' \
               '"arrangeby":"Price","order":"asc","market":"GB",' \
               '"language":"en","super_region":"europe",' \
               '"lng":' + str(longitude) + ',"lat":' + str(latitude) + ',"zip":"B16","range":0},'\
               '"offset":0,"count":50,"outsideOffset":0,"outsideSearch":false}'


    def load_inventory(self, count):
        try:
            response = requests.get(self.api_url, params=self.query_params, headers=self.headers).json()
            results = response['results']

            # check results is actually a list, if
            # it is a dict then no cars available
            if type(results) != list:
                self.log('No cars loaded')
                return

            new_cars = 0
            cars_list = []
            for result in results:
                trim = result['TrimName']
                paint = result['PAINT'][0]
                interior = result['INTERIOR'][0] if type(result['INTERIOR']) == list else "NO COLOUR"
                price = result['Price']

                car = Car(trim, paint, interior, price)
                cars_list.append(car)
                if car not in self.cars:
                    if count > 0:
                        self.alert_new_car(car)
                    new_cars += 1

            # update the cars list, we replace rather than just
            # adding new cars found in case any cars are removed
            self.cars = cars_list

            msg = 'Loaded {} cars'.format(new_cars) if count == 0 else 'Found {} new cars'.format(new_cars)
            self.log(msg)
        except:
            self.log('Error loading inventory')


    def alert_new_car(self, car):
        self.log('New car found: {}'.format(car))


    def run(self):
        count = 0
        while True:
            self.load_inventory(count)
            count += 1
            time.sleep(self.delay)

