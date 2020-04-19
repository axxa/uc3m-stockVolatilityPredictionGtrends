import numpy as np
import pandas as pd


def merge_binary_time_series(left_df, right_df, date_column_name):
    return pd.merge(left_df, right_df, on=date_column_name, how='left').fillna(0)


def calculate_return(data_array: np.array):
    arr = np.zeros_like(data_array)
    for idx in range(data_array.shape[0]):
        if idx != 0:
            arr[idx] = float(data_array[idx] / data_array[idx - 1]) - 1
    return arr


class ProcessData:

    def __init__(self, context=''):
        self.context = context
        self.std: float = 0
        self.mean: float = 0
        self.mean_plus_std: float = 0
        self.mean_minus_std: float = 0
        self.binary_serie_df: pd.DataFrame()
        self.normalized_: np.array
        self.normalized_df: pd.DataFrame()
        # self.norm_binary_serie_df: pd.DataFrame()

    def generate_statistic_data(self, data_array: np.array):
        self.std = np.std(data_array)
        self.mean = np.mean(data_array)
        self.mean_plus_std = self.mean + self.std
        self.mean_minus_std = self.mean - self.std
        self.normalize(data_array)

    def generate_binary_series(self, data_array: np.array, discard_first):
        arr_auxiliar = np.arange(0, data_array.size)
        binary_serie = np.zeros((data_array.size,), dtype=int)
        idx_binary_series = arr_auxiliar[(data_array > self.mean_plus_std) | (data_array < self.mean_minus_std)]
        for idx in idx_binary_series:
            binary_serie[idx] = 1
        if discard_first:
            binary_serie[0] = 0
        # normalized binary series
        norm_binary_serie = np.zeros((data_array.size,), dtype=int)
        idx_norm_binary_series = arr_auxiliar[(self.normalized_ > self.mean_plus_std) |
                                              (self.normalized_ < self.mean_minus_std)]
        for idx in idx_norm_binary_series:
            norm_binary_serie[idx] = 1
        if discard_first:
            norm_binary_serie[0] = 0
        self.binary_serie_df = pd.DataFrame(binary_serie, columns=['binary_' + self.context])
        # self.norm_binary_serie_df = pd.DataFrame(binary_serie, columns=["norm_binary_" + self.context])

    def normalize(self, data_array: np.array):
        f = lambda x: (x - self.mean) / self.std
        self.normalized_ = f(data_array)
        self.normalized_df = pd.DataFrame(self.normalized_, columns=['norm_' + self.context])


