import pandas as pd
import os
import sklearn.metrics as skl
import numpy as np

from constants.CONSTANTS import CONSTANTS
from modules.Utils import split_df_by_years
from modules.Utils import create_plot_from_df


def process_data(y_pred_df, y_true_df, stock_name, path):
    y_preds, year_list = split_df_by_years(y_pred_df, 'date')
    y_trues, year_list = split_df_by_years(y_true_df, 'date')
    precision = []
    # recall = []
    volatility_ratio_of_1 = []
    for y_pred, y_true, years in zip(y_preds, y_trues, year_list):
        y_pred = y_pred['binary_trend']
        y_true = y_true['binary_finance']
        if y_pred.shape[0] < y_true.shape[0]:
            y_true = y_true[:-1]
        if y_pred.shape[0] > y_true.shape[0]:
            y_pred = y_pred[:-1]
        try:
            tn, fp, fn, tp = skl.confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
            precision.append(0 if tp + fp == 0 else tp / (tp + fp))
            volatility_ratio_of_1.append(0 if len(y_true) == 0 else np.count_nonzero(y_true)/len(y_true))
            # recall.append(0 if tp + fn == 0 else tp / (tp + fn))
        except Exception as e:
            print(e, f" stock_name: {stock_name}")

    df = pd.DataFrame({'date': year_list, 'precision': precision, 'volatility_ratio_of_1': volatility_ratio_of_1})

    x_arr = ['date', 'date']
    y_arr = ['precision', 'volatility_ratio_of_1']
    color_arr = ['green', 'purple']

    create_plot_from_df(df, x_arr, y_arr, color_arr, "contraste_" + stock_name, path)


def read_data():
    results_path = CONSTANTS.ibex_results_path
    files = [file for file in os.listdir(results_path)
             if file[-4:] == 'xlsx' and '__REPORT__' not in file]
    print(f'readings files: {files}')
    for f in files:
        stock_name = f.split('__')[0]
        f = results_path + f
        y_pred_df = pd.read_excel(open(f, 'rb'), sheet_name='poda_trend')
        y_true_df = pd.read_excel(open(f, 'rb'), sheet_name='poda_finance')
        process_data(y_pred_df, y_true_df, stock_name, results_path)


read_data()
