import logging

import requests


class SomethingWrongError(Exception):
  pass


def _extract_bike_location(bike, lon_abbrev='lon'):
  """
  Standardize the bike location data from GBFS. Some have extra fields,
  and some are missing fields.

  Arguments:
    bike (dict[str, str]): A GBFS bike object as it appears in free_bike_status.json
    lon_abbrev (str): The abbreviation used for `longitude`

  Returns:
    dict[str, str]: A normalized GBFS bike object
  """
  output = {key: bike.get(key) for key in ['bike_id', 'lat', 'is_reserved', 'is_disabled']}
  output['lon'] = bike.get(lon_abbrev)
  return output


def _pull_from_gbfs(url):
  """
  Pull data from a GBFS URL.

  Arguments:
    url (str): The URL of free_bike_status.json

  Returns:
    list[dict[str, str]]: The GBFS position data of bikes
  """
  r = requests.get(url)
  return [_extract_bike_location(bike) for bike in r.json()['data']['bikes']]


def pull_jump():
  data = _pull_from_gbfs('https://dc.jumpmobility.com/opendata/free_bike_status.json')
  logging.info('Got data on %s bikes', len(data))
  return data


def pull_lime():
  r = requests.get('https://lime.bike/api/partners/v1/bikes?region=Washington%20DC%20Proper',
                   headers={'Authorization': 'Bearer limebike-PMc3qGEtAAXqJa'})
  data = [{
    'bike_id': bike['id'],
    'lat': bike['attributes']['latitude'],
    'lon': bike['attributes']['longitude'],
    'is_reserved': None,
    'is_disabled': None
  } for bike in r.json()['data']]
  logging.info('Got data on %s bikes', len(data))
  return data


def pull_ofo():
  payload = {
    'token': 'c902b87e3ce8f9f95f73fe7ee14e81fe',
    'name': 'Washington',
    'lat': 38.894432,
    'lng': -77.013655
  }
  r = requests.post('http://ofo-global.open.ofo.com/api/bike', data=payload)
  data = [_extract_bike_location(bike, lon_abbrev='lng') for bike in r.json()['values']['cars']]
  logging.info('Got data on %d bikes', len(data))
  return data


def pull_spin():
  data = _pull_from_gbfs('https://web.spin.pm/api/gbfs/v1/free_bike_status')
  logging.info('Got data on %d bikes', len(data))
  return data


def for_provider(provider):
  if provider == 'jump':
    return pull_jump
  if provider == 'lime':
    return pull_lime
  if provider == 'ofo':
    return pull_ofo
  if provider == 'spin':
    return pull_spin
