import numpy as np
import pandas as pd

import modules.Utils as UTILS

def merge_binary_time_series(left_df, right_df, date_column_name):
    return pd.merge(left_df, right_df, on=date_column_name, how='left').fillna(0)


class ProcessData:

    def __init__(self):
        self.std: float = 0
        self.mean: float = 0
        self.mean_plus_std: float = 0
        self.mean_minus_std: float = 0
        self.binary_serie_df: pd.DataFrame()

    def generate_statistic_data(self, data_array: np.array):
        self.std = np.std(data_array)
        self.mean = np.mean(data_array)
        self.mean_plus_std = self.mean + self.std
        self.mean_minus_std = self.mean - self.std

    def generate_binary_series(self, data_array: np.array, column_name):
        arr_auxiliar = np.arange(0, data_array.size)
        binary_serie = np.zeros((data_array.size,), dtype=int)
        idx_binary_series = arr_auxiliar[(data_array > self.mean_plus_std) | (data_array < self.mean_minus_std)]
        for idx in idx_binary_series:
            binary_serie[idx] = 1
        self.binary_serie_df = pd.DataFrame(binary_serie, columns=[column_name])

