import pandas as pd
import os
import sklearn.metrics as skl
import numpy as np

from constants.CONSTANTS import CONSTANTS
from modules.Utils import split_df_by_years


def read_data():
    results_path = CONSTANTS.dax30_results_path
    files = [file for file in os.listdir(results_path)
             if file[-4:] == 'xlsx' and '__REPORT__' not in file]
    print(f'readings files: {files}')
    best_sensitivity = 0
    best_stock_sensitivity = ''
    best_specificity = 0
    best_stock_specificity = ''
    for f in files:
        stock_name = f.split('__')[0]
        f = results_path + f
        y_pred = pd.read_excel(open(f, 'rb'), sheet_name='poda_trend')['binary_trend']
        y_true = pd.read_excel(open(f, 'rb'), sheet_name='poda_finance')['binary_finance']
        if y_pred.shape[0] < y_true.shape[0]:
            y_true = y_true[:-1]
        if y_pred.shape[0] > y_true.shape[0]:
            y_pred = y_pred[:-1]
        try:
            tn, fp, fn, tp = skl.confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
            sentivity = 0 if tp + fn == 0 else tp / (tp + fn)
            if best_sensitivity < sentivity:
                best_sensitivity = sentivity
                best_stock_sensitivity = stock_name
            specificity = 0 if fp + tn == 0 else tp / (fp + tn)
            if best_specificity < specificity:
                best_specificity = specificity
                best_stock_specificity = stock_name
        except Exception as e:
            print(e, f" stock_name: {stock_name}")

    file = [file for file in os.listdir(results_path)
            if file[-4:] == 'xlsx' and '__REPORT__' in file][0]

    report_df = pd.read_excel(open(results_path + file, 'rb'), sheet_name='__REPORT__')
    report_df.rename(columns={report_df.columns[0]: ""}, inplace=True)
    complementary = pd.DataFrame([
      ['best_sensitivity', best_stock_sensitivity, best_sensitivity],
      ['best_specificity', best_stock_specificity, best_specificity]],
      columns=['', 'stock', 'value'])

    report_df = report_df.append(complementary)
    report_df.to_excel(results_path + file)


read_data()
