import requests
import pandas as pd
import numpy as np
from datetime import datetime

from constants.CONSTANTS import CONSTANTS


class GetDataFromAPI:
    def __init__(self, trend_word: str, stock: str):
        self.trend_word = trend_word
        self.stock = stock

    def format_date_fromtimestamp(self, x) -> datetime:
      return datetime.fromtimestamp(int(x)).replace(hour=0)

    def format_date_string(self, x) -> datetime:
      return np.datetime64(x).astype(datetime).replace(hour=0)

    def request_service(self, request_string) -> []:
        response = requests.get(request_string, verify=False)
        return response.json()

    def request_transform_trend_data(self, start_date, end_date) -> pd.core.frame.DataFrame:
        response_json =self.request_service(CONSTANTS.googleTrendsAPIMethodURL + self.trend_word + '/' +
                                            start_date + '/' + end_date)

        response_df = pd.DataFrame(response_json['gtrendsdata']) \
          .drop(['formattedTime', 'formattedAxisTime', 'formattedValue', 'hasData', 'symbol'], axis=1)
        response_df['time'] = response_df['time'].apply(self.format_date_fromtimestamp)
        response_df = response_df.rename(columns={"time": "date"}, errors="raise")
        return response_df

    def request_transform_finance_data(self, start_date, end_date):
        response_json =self.request_service(CONSTANTS.yahooFinanceAPIMethodURL + self.stock + '/' +
                                            start_date + '/' + end_date)
        response_df = pd.DataFrame(response_json['stockdata'])\
          .drop(['symbol', 'open', 'close', 'volume', 'low', 'high'], axis=1)
        response_df['date'] = response_df['date'].apply(self.format_date_string)
        return response_df
