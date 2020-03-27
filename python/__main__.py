import pandas as pd
import numpy as np

from modules.GetDataFromAPI import GetDataFromAPI
import modules.ProcessData as prd
from constants.CONSTANTS import CONSTANTS


if __name__ == '__main__':
    # CASE 1 : BBVA ------------------------------------------------------------
    getDataFromAPI = GetDataFromAPI('BBVA', 'BBVA')

    response_trend_df = getDataFromAPI.request_transform_trend_data()
    trend_statistics = prd.ProcessData()
    trend_value_arr = np.array(response_trend_df['value'])
    trend_statistics.generate_statistic_data(trend_value_arr)
    trend_statistics.generate_binary_series(trend_value_arr, 'binary_trend')
    response_trend_df = response_trend_df.join(trend_statistics.binary_serie_df)

    response_finance_df = getDataFromAPI.request_transform_finance_data()
    finance_statistics = prd.ProcessData()
    finance_value_arr = np.array(response_finance_df['adjClose'])
    finance_statistics.generate_statistic_data(finance_value_arr)
    finance_statistics.generate_binary_series(finance_value_arr, 'binary_finance')
    response_finance_df = response_finance_df.join(finance_statistics.binary_serie_df)

    #df = pd.merge(response_trend_df, response_finance_df, on='date', how='left').fillna(0)
    df = prd.merge_binary_time_series(response_trend_df, response_finance_df, 'date')
    # print(response_trend_df)
    print('--------------------------------------')
    # print(response_finance_df)
    print('--------------------------------------')
    print(df)
    # ---------------------------------------------------------------------------
