from io import StringIO
from datetime import date

import requests
import pandas as pd

from apis import Query


class WundergroundQuery(Query):
    def __init__(self, place_id: str, begin: date, end: date):
        self.place_id = place_id
        self.begin = begin
        self.end = end


def get_rain(query: WundergroundQuery):

    params = {
        'place': query.place_id,
        'begin': query.begin.strftime('%Y/%-m/%-d'),
        'dayend': query.end.strftime('%-d'),
        'monthend': query.end.strftime('%-m'),
        'yearend': query.end.strftime('%Y')
    }

    url = '''http://www.wunderground.com/history/airport/{place}/ \
        {begin}/CustomHistory.html?dayend={dayend}&monthend={monthend}&yearend={yearend} \
        &MR=1&format=1'''.format(**params)

    return _get_rain_from_url(url)


def _get_rain_from_url(url: str):
    response = requests.get(url)
    html = response.text
    csv = html.replace('<br />', '')
    frame = pd.DataFrame.from_csv(StringIO(csv))
    return frame['Precipitationmm']


