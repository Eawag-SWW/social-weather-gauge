from StringIO import StringIO
import requests
import pandas as pd

def get_rain():
    """

    :rtype : pd.Series
    """
    url = 'http://www.wunderground.com/history/airport/EGLL/2015/8/25/CustomHistory.html?dayend=2&monthend=9&yearend=2015&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&MR=1&format=1'
    response = requests.get(url)
    html = response.text
    csv = html.replace('<br />', '')
    input = StringIO(csv)
    frame = pd.DataFrame.from_csv(input)

    precipitation = frame['Precipitationmm']
    return precipitation



if __name__ == '__main__':
    precipitation = get_rain()
    print precipitation.index
