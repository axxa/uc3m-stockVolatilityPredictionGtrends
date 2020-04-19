import pandas as pd
import numpy as np
import datetime

from modules.GetDataFromAPI import GetDataFromAPI
import modules.ProcessData as prd
import modules.AnalisysData as mad
import modules.Utils as UTILS
from constants.CONSTANTS import CONSTANTS


def extract_data(getDataFromAPI: GetDataFromAPI, start_date, end_date):
    response_trend_df = getDataFromAPI.request_transform_trend_data(start_date, end_date)
    response_finance_df = getDataFromAPI.request_transform_finance_data(start_date, end_date)
    return response_trend_df, response_finance_df


def process_data(response_trend_df, response_finance_df):
    trend_statistics = prd.ProcessData('trend')
    trend_value_arr = np.array(response_trend_df['value'])
    trend_statistics.generate_statistic_data(trend_value_arr)
    trend_statistics.generate_binary_series(trend_value_arr, False)
    trend_statistics.normalize(trend_value_arr)
    response_trend_df = response_trend_df.join(trend_statistics.binary_serie_df)
    # response_trend_df = response_trend_df.join(trend_statistics.norm_binary_serie_df)
    response_trend_df = response_trend_df.join(trend_statistics.normalized_df)

    finance_statistics = prd.ProcessData('finance')
    return_array = prd.calculate_return(np.array(response_finance_df['adjClose']))

    finance_statistics.generate_statistic_data(return_array)
    finance_statistics.generate_binary_series(return_array, True)
    response_finance_df['returns'] = return_array

    response_finance_df = response_finance_df.join(finance_statistics.binary_serie_df)
    # response_finance_df = response_finance_df.join(finance_statistics.norm_binary_serie_df)
    response_finance_df = response_finance_df.join(finance_statistics.normalized_df)

    return prd.merge_binary_time_series(response_trend_df, response_finance_df, 'date'), \
        trend_statistics, finance_statistics, return_array


if __name__ == '__main__':
    start_date = '2011-01-01'
    end_date = '2011-12-31'
    # print('empieza proceso: ' + datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
    # CASE 1 : BBVA ------------------------------------------------------------
    getDataFromAPI = GetDataFromAPI('BBVA', 'BBVA')
    if UTILS.check_date_range_by_days(start_date, end_date) > 180:
        # print(f'{UTILS.check_date_range_by_days(start_date, end_date)} dias')
        range_date_arr = list(UTILS.get_range_dates_by_chunks(start_date, end_date, 180))
        df = pd.DataFrame()
        response_trend_df = pd.DataFrame()
        response_finance_df = pd.DataFrame()
        for tuple_ in range_date_arr:
            response_ = extract_data(getDataFromAPI, tuple_[0], tuple_[1])
            response_trend_df = response_trend_df.append(response_[0])
            response_finance_df = response_finance_df.append(response_[1])
        process_data_ = process_data(response_trend_df, response_finance_df)
        df = process_data_[0]
        trend_statistics = process_data_[1]
        finance_statistics = process_data_[2]
        returns_array = process_data_[3]  # variacion de precios de cierre
    else:
        response_ = extract_data(getDataFromAPI, start_date, end_date)
        response_trend_df = response_[0]
        response_finance_df = response_[1]
        process_data_ = process_data(response_[0], response_[1])
        df = process_data_[0]
        trend_statistics = process_data_[1]
        finance_statistics = process_data_[2]
        returns_array = process_data_[3]

    mad.report_final(response_trend_df, response_finance_df, df, trend_statistics, finance_statistics)
    # print('termina proceso: ' + datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
