from datetime import datetime

import requests
import json


class Place:
    def __init__(self, name, place_id, country):
        self.name = name
        self.place_id = place_id
        self.country = country

    @classmethod
    def from_dict(cls, data):
        name = data['PlaceName']
        city_id = data['CityId']
        country = data['CountryName']
        return cls(name, city_id, country)


class Flight:
    def __init__(self, **kwargs):
        self.price = kwargs['price']
        self.direct = kwargs['direct']
        self.origin = kwargs['origin']
        self.dest = kwargs['dest']
        self.arrival = kwargs['arrival']
        self.carrier = kwargs['carrier']

    @property
    def arrival_date(self):
        return self.arrival.strftime('%d-%m-%Y')

    @property
    def arrival_time(self):
        return self.arrival.strftime('%H:%M:%S')

    @classmethod
    def from_dict(cls, data):
        for quote in data['Quotes']:
            carrier_id = quote['OutboundLeg']['CarrierIds'][0]
            origin_id = quote['OutboundLeg']['OriginId']
            dest_id = quote['OutboundLeg']['DestinationId']
            carrier_name = next(carrier['Name'] for carrier in data['Carriers']
                                if carrier['CarrierId'] == carrier_id)
            origin = next(place for place in data['Places'] if place['PlaceId'] == origin_id)
            dest = next(place for place in data['Places'] if place['PlaceId'] == dest_id)
            flight = {
                'price': quote['MinPrice'],
                'direct': quote['Direct'],
                'arrival': datetime.strptime(quote['OutboundLeg']['DepartureDate'], '%Y-%m-%dT%H:%M:%S'),
                'carrier':  carrier_name,
                'origin': Place(name=origin['Name'], place_id=origin['IataCode'], country=origin['CountryName']),
                'dest': Place(name=dest['Name'], place_id=dest['IataCode'], country=dest['CountryName']),
            }
            yield cls(**flight)


# Подтягиваем чувствительные данные из переменных окружения
# assert 'RAPIDAPI_KEY' in os.environ, 'Environment variable RAPIDAPI_KEY is not exist'
# RAPIDAPI_KEY = os.environ['RAPIDAPI_KEY']
RAPIDAPI_HOST = 'skyscanner-skyscanner-flight-search-v1.p.rapidapi.com'
COUNTRY = 'RU'
CURRENCY = 'RUB'
LOCALE = 'ru-RU'

HEADERS = {
    'x-rapidapi-key': 'a00f87e656mshad49d643dd93889p1d9ecbjsn0a7e7b2276a6',
    'x-rapidapi-host': RAPIDAPI_HOST
    }


def get_city(city):
    url = f'https://{RAPIDAPI_HOST}/apiservices/autosuggest/v1.0/{COUNTRY}/{CURRENCY}/{LOCALE}/'

    querystring = {'query': city}
    response = requests.request('GET', url, headers=HEADERS, params=querystring)
    places_info = json.loads(response.text)
    if places_info.get('Places'):
        return Place.from_dict(places_info['Places'][0])
    return None


def get_flight(origin_place, dest_place, date):
    origin_id = origin_place.place_id
    dest_id = dest_place.place_id
    url = f'https://{RAPIDAPI_HOST}/apiservices/browsedates/v1.0/{COUNTRY}/{CURRENCY}/{LOCALE}/' \
          f'{origin_id}/{dest_id}/{date}'
    response = requests.request('GET', url, headers=HEADERS)
    raw_flights = json.loads(response.text)
    if raw_flights.get('Quotes'):
        return next(Flight.from_dict(raw_flights))
    return None


def get_dates(origin_place, dest_place, date):
    origin_id = origin_place.place_id
    dest_id = dest_place.place_id
    url = f'https://{RAPIDAPI_HOST}/apiservices/browsedates/v1.0/{COUNTRY}/{CURRENCY}/{LOCALE}/' \
          f'{origin_id}/{dest_id}/{date}'
    response = requests.request('GET', url, headers=HEADERS)
    raw_flights = json.loads(response.text)
    if raw_flights.get('Quotes'):
        return [quote['OutboundLeg']['DepartureDate'][:10] for quote in raw_flights['Quotes']]
    return None
