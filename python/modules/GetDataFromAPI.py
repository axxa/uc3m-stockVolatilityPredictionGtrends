import requests
import pandas as pd
import numpy as np
from datetime import datetime

from constants.CONSTANTS import CONSTANTS


def replace_blanks(string_):
    return string_.replace(' ', '+')


def format_date_fromtimestamp(x) -> datetime:
    return datetime.fromtimestamp(int(x)).replace(hour=0)


def format_date_string(x) -> datetime:
    return np.datetime64(x).astype(datetime).replace(hour=0)


def request_service(request_string) -> []:
    response = requests.get(request_string, verify=False)
    return response.json()


class GetDataFromAPI:
    def __init__(self, trend_word: str, stock: str):
        self.trend_word = trend_word
        self.stock = stock

    def request_transform_trend_data(self, start_date, end_date) -> pd.core.frame.DataFrame:
        trend_word_api_call = replace_blanks(self.trend_word)
        response_json = request_service(CONSTANTS.googleTrendsAPIMethodURL + trend_word_api_call + '/' +
                                        start_date + '/' + end_date)
        if len(response_json['gtrendsdata']) > 0:
            response_df = pd.DataFrame(response_json['gtrendsdata'])\
              .drop(['formattedTime', 'formattedAxisTime', 'formattedValue', 'hasData'], axis=1)
            response_df['time'] = response_df['time'].apply(format_date_fromtimestamp)
            response_df = response_df.rename(columns={"time": "date"}, errors="raise")
        else:
            response_df = None
        return response_df

    def request_transform_finance_data(self, start_date, end_date):
        response_json = request_service(CONSTANTS.yahooFinanceAPIMethodURL + self.stock + '/' +
                                        start_date + '/' + end_date)
        if len(response_json['stockdata']) > 0:
            response_df = pd.DataFrame(response_json['stockdata'])\
                .drop(['symbol', 'open', 'close', 'volume', 'low', 'high'], axis=1)
            response_df['date'] = response_df['date'].apply(format_date_string)
        else:
            response_df = None
        return response_df
