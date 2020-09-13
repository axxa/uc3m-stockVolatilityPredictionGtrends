import pandas as pd
import os
import sklearn.metrics as skl

from constants.CONSTANTS import CONSTANTS
from modules.Utils import split_df_by_years
from modules.Utils import create_plot_from_df


def process_data(y_pred_df, y_true_df, stock_name, path):
    y_preds, year_list = split_df_by_years(y_pred_df, 'date')
    y_trues, year_list = split_df_by_years(y_true_df, 'date')
    precision = []
    recall = []
    for y_pred, y_true, years in zip(y_preds, y_trues, year_list):
        y_pred = y_pred['binary_trend']
        y_true = y_true['binary_finance']
        tn, fp, fn, tp = skl.confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        precision.append(0 if tp + fp == 0 else tp / (tp + fp))
        recall.append(0 if tp + fn == 0 else tp / (tp + fn))

    df = pd.DataFrame({'date': year_list, 'precision': precision, 'recall': recall})

    x_arr = ['date', 'date']
    y_arr = ['precision', 'recall']
    color_arr = ['green', 'purple']

    create_plot_from_df(df, x_arr, y_arr, color_arr, "contraste_" + stock_name, path)

    # metricas_metodo5(y_pred['binary_trend'], y_true['binary_finance'], stock_name)


def read_data():
    files = [file for file in os.listdir(CONSTANTS.index_results_path)
             if file[-4:] == 'xlsx' and '__REPORT__' not in file]
    print(f'readings file: {files}')
    for f in files:
        stock_name = f.split('__')[0]
        f = CONSTANTS.index_results_path + f
        y_pred_df = pd.read_excel(open(f, 'rb'), sheet_name='poda_trend')
        y_true_df = pd.read_excel(open(f, 'rb'), sheet_name='poda_finance')
        process_data(y_pred_df, y_true_df, stock_name, CONSTANTS.index_results_path)

    #  tn, fp, fn, tp = skl.confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

read_data()
