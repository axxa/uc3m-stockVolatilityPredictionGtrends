import numpy as np
import pandas as pd
import math
from datetime import datetime
from datetime import timedelta


def fit_trend_binary_series(trend_df, finance_df):
    #  Obtener fechas mas proximas de las binarias
    min_true_date = finance_df.date.min()
    max_true_date = finance_df.date.max()
    earliest_trend_date = min_true_date
    aux = 10
    aux2 = 10
    for x in trend_df['date']:
        if 0 < (min_true_date - x).days < aux:
          aux = (min_true_date - x).days
          earliest_trend_date = x
        if 0 < (max_true_date - x).days < aux2:
          aux2 = (max_true_date - x).days
          oldest_trend_date = x

    mask = (trend_df['date'] >= earliest_trend_date) & (trend_df['date'] <= oldest_trend_date)
    trend_df = trend_df.loc[mask]

    return trend_df


def fit_df_series(predecido_df, predictor_df):
    """Se quiere predecir el futuro inmediato por tanto se corre la binaria de finance
    una posicion y/o se acorta la binaria de tendencias una posicion"""
    if predictor_df['date'].iloc[0] == predecido_df['date'].iloc[0] \
      or predictor_df['date'].iloc[0] > predecido_df['date'].iloc[0]:
        predecido_df = predecido_df.iloc[1:]
    if predictor_df.shape[0] > predecido_df.shape[0]:
        predictor_df = predictor_df.iloc[:-1]
    elif predictor_df.shape[0] < predecido_df.shape[0]:
        predecido_df = predecido_df.iloc[:-1]

    return predictor_df, predecido_df


def merge_binary_time_series(left_df, right_df, date_column_name):
    return pd.merge(left_df, right_df, on=date_column_name, how='left').fillna(0)


def calculate_return(data_array: np.array):
    arr = np.zeros_like(data_array)
    for idx in range(data_array.shape[0]):
        arr[idx] = float(data_array[idx] / data_array[idx - 1]) - 1 if data_array[idx - 1] != 0 and idx != 0 else 0

    return arr


def prune_day_from_dataframe(df, days_to_exclude):
    # Quita un dia determinado de un time series data frame
    df["weekday"] = pd.to_datetime(df.date).dt.dayofweek
    for day_to_exclude in days_to_exclude:
        df = df.loc[df["weekday"] != day_to_exclude]
    # df.pop('weekday')
    # df.reset_index(inplace=True)
    df = df.reset_index(drop=True)
    return df


def prune_row_correspondance_by_value(left_df, right_df,
                                      column_name, value, right_correspondance, date_column_name):
    # Selecciono primero los valores que se van a podar en el primer dataframe
    df = left_df.loc[left_df[column_name] == value].copy()
    # Se guarda un array con las fechas que van a servir para podar los datos en el otro array
    df[date_column_name] = df[date_column_name] + timedelta(days=right_correspondance)
    date_np = np.array(df[date_column_name])

    # Borro en el df derecho
    for date_ in date_np:
        right_df = right_df[right_df[date_column_name] != date_]
    right_df = right_df.reset_index(drop=True)
    # Borro en el df izquierdo
    left_df = left_df.loc[left_df[column_name] != value]
    left_df = left_df.reset_index(drop=True)
    return left_df, right_df


class ProcessData:

    def __init__(self, context='', discard_first=False):
        self.context = context
        self.std: float = 0
        self.mean: float = 0
        self.mean_plus_std: float = 0
        self.mean_minus_std: float = 0
        self.binary_serie_df: pd.DataFrame() = None
        self.normalized_: np.array = None
        self.normalized_df: pd.DataFrame() = None
        self.discard_first = discard_first

    def generate_statistic_data(self, data_array: np.array):
        to_norm_arr = data_array
        if self.discard_first:
            data_array = data_array[1:]

        self.std = np.std(data_array)
        self.mean = np.mean(data_array)
        self.mean_plus_std = self.mean + self.std
        self.mean_minus_std = self.mean - self.std
        self.normalize(to_norm_arr)

    def generate_binary_series(self, data_array: np.array):
        arr_auxiliar = np.arange(0, data_array.size)
        binary_serie = np.zeros((data_array.size,), dtype=int)
        idx_binary_series = arr_auxiliar[(data_array > self.mean_plus_std) | (data_array < self.mean_minus_std)]
        for idx in idx_binary_series:
            binary_serie[idx] = 1
        if self.discard_first:
            binary_serie[0] = 0
        # normalized binary series
        norm_binary_serie = np.zeros((data_array.size,), dtype=int)
        idx_norm_binary_series = arr_auxiliar[(self.normalized_ > self.mean_plus_std) |
                                              (self.normalized_ < self.mean_minus_std)]
        for idx in idx_norm_binary_series:
            norm_binary_serie[idx] = 1
        if self.discard_first:
            norm_binary_serie[0] = 0
        self.binary_serie_df = pd.DataFrame(binary_serie, columns=['binary_' + self.context])
        # self.norm_binary_serie_df = pd.DataFrame(binary_serie, columns=["norm_binary_" + self.context])

    def normalize(self, data_array: np.array):
        if self.std != 0:
            f = lambda x: 0 if self.std == 0 else (x - self.mean) / self.std
            self.normalized_ = f(data_array)
        else:
            self.normalized_ = data_array

        if self.discard_first:
            self.normalized_[0] = 0
        self.normalized_df = pd.DataFrame(self.normalized_, columns=['norm_' + self.context])



