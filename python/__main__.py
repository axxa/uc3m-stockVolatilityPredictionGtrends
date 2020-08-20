import pandas as pd
import numpy as np
import warnings

from modules.GetDataFromAPI import GetDataFromAPI
import modules.ProcessData as prd
import modules.AnalisysData as mad
import modules.Utils as Utils
from constants.CONSTANTS import CONSTANTS
from modules.ProcessData import fit_trend_binary_series
from modules.global_results import GlobalResults

warnings.filterwarnings('ignore')


def execute(key, value, start_date, end_date):
    stock = key
    trend_word = value
    getDataFromAPI = GetDataFromAPI(trend_word, stock)

    range_date_arr = list(Utils.get_range_dates_by_chunks(start_date, end_date, 180))

    response_trend_df = pd.DataFrame()
    response_finance_df = pd.DataFrame()
    for tuple_ in range_date_arr:
        response_ = extract_data(getDataFromAPI, tuple_[0], tuple_[1])
        if response_ is not None and response_[0] is not None and response_[1] is not None and response_[0].shape[0] > 0 and response_[1].shape[0] > 0:
            response_trend_df = response_trend_df.append(response_[0])
            response_finance_df = response_finance_df.append(response_[1])

    if response_trend_df.shape[0] > 0 and response_finance_df.shape[0] > 0:
        prune_trend_df, prune_finance_df, trend_statistics, finance_statistics, \
          returns_array = process_data(response_trend_df, response_finance_df)

        if prune_trend_df is not None and prune_trend_df.shape[0] > 0 and prune_finance_df.shape[0] > 0:
            mad.report_final(response_trend_df, response_finance_df,
                             prune_trend_df, prune_finance_df,
                             trend_statistics, finance_statistics, stock)
        else:
            print(f'Data not found after pruned for stock {trend_word} between {start_date} and {end_date} '
                  f'trend={response_trend_df.shape[0]} finance={response_finance_df.shape[0]}')

    else:
        print(f'Data not found for stock {trend_word} between {start_date} and {end_date} '
              f'trend={response_trend_df.shape[0]} finance={response_finance_df.shape[0]}')


def extract_data(getDataFromAPI: GetDataFromAPI, start_date, end_date):
    response_trend_df = getDataFromAPI.request_transform_trend_data(start_date, end_date)
    response_finance_df = getDataFromAPI.request_transform_finance_data(start_date, end_date)
    return response_trend_df, response_finance_df


def process_data(response_trend_df: pd.DataFrame(), response_finance_df: pd.DataFrame()):
    # Se podan los  todos los sábados (de todas las series) y domingos (de las series finance).
    # Para esto construye series con los datos de L-V para finance y Domingo-Jueves para trends.
    df = prd.merge_binary_time_series(response_trend_df, response_finance_df, 'date')
    # df = df.loc[df["value"] > 0]
    df = df.reset_index(drop=True)
    response_trend_df = df.drop(['adjClose'], axis=1)
    response_finance_df = df.drop(['value'], axis=1)

    response_trend_df, response_finance_df = prd.prune_row_correspondance_by_value(response_trend_df,
                                                                                   response_finance_df,
                                                                                   'value', 0, 1, 'date')
    response_finance_df, response_trend_df = prd.prune_row_correspondance_by_value(response_finance_df,
                                                                                   response_trend_df,
                                                                                   'adjClose', 0, -1, 'date')

    response_trend_df = prd.prune_day_from_dataframe(response_trend_df, [4, 5])  # Viernes y Sabado
    response_finance_df = prd.prune_day_from_dataframe(response_finance_df, [5, 6])  # Sabado y Domingo

    if response_trend_df.shape[0] == 0 or response_finance_df.shape[0] == 0:
        return None, None, None, None, None

    response_trend_df = fit_trend_binary_series(response_trend_df, response_finance_df)
    trend_statistics = prd.ProcessData('trend', False)
    trend_value_arr = np.array(response_trend_df['value'])
    trend_statistics.generate_statistic_data(trend_value_arr)
    trend_statistics.generate_binary_series(trend_value_arr)
    trend_statistics.normalize(trend_value_arr)
    response_trend_df['binary_' + trend_statistics.context] = \
        trend_statistics.binary_serie_df['binary_' + trend_statistics.context]

    response_trend_df = response_trend_df.join(trend_statistics.normalized_df)

    # -----------------------------------------------------------------------------
    finance_statistics = prd.ProcessData('finance', True)
    return_array = prd.calculate_return(np.array(response_finance_df['adjClose']))

    finance_statistics.generate_statistic_data(return_array)
    finance_statistics.generate_binary_series(return_array)
    response_finance_df['returns'] = return_array
    finance_statistics.normalize(return_array)

    response_finance_df['binary_' + finance_statistics.context] = \
        finance_statistics.binary_serie_df['binary_' + finance_statistics.context]
    response_finance_df['norm_' + finance_statistics.context] = \
        finance_statistics.normalized_df['norm_' + finance_statistics.context]

    return response_trend_df, response_finance_df, trend_statistics, finance_statistics, return_array


if __name__ == '__main__':
    # SP500_STOCK_LIBRARY_1, SP500_STOCK_LIBRARY_2, IBEX_STOCK_LIBRARY, DAX30_STOCK_LIBRARY
    CONSTANTS.LIBRARY = CONSTANTS.IBEX_STOCK_LIBRARY
    CONSTANTS.RESULTS_PATH = CONSTANTS.ibex_results_path

    for key, value in CONSTANTS.LIBRARY.items():
        execute(key, value, CONSTANTS.start_date, CONSTANTS.end_date)

    mad.save_global_results()
