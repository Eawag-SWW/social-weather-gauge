from io import StringIO
from datetime import date
import requests
import pandas as pd


def get_rain(wunderground_place_id, begin: date, end: date):

    params = {
        'place': wunderground_place_id
        'begin': begin.strftime('%Y/%m/%d')
        ...
    }


    url = '''http://www.wunderground.com/history/airport/{place}/ \
    {begin}/CustomHistory.html?dayend={dayend}&monthend={monthend&yearend={yearend} \
    &MR=1&format=1'''.format(params)

    url = '''http://www.wunderground.com/history/airport/EGLL/ \
    2015/8/25/CustomHistory.html?dayend=2&monthend=9&yearend=2015 \
    &req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&MR=1&format=1'''
    response = requests.get(url)
    html = response.text
    csv = html.replace('<br />', '')
    frame = pd.DataFrame.from_csv(StringIO(csv))

    return  frame['Precipitationmm']


if __name__ == '__main__':
    begin = date(2015, 8, 25)
    end = date(2015, 9, 2)
    precipitation = get_rain('EGLL', begin, 'x')
    print(precipitation)
