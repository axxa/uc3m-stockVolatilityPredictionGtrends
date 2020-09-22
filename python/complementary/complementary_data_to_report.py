import pandas as pd
import os

from constants.CONSTANTS import CONSTANTS
from modules.Utils import extract_confusion_matrix, extract_fisher


def read_data():
    results_path = "././" + CONSTANTS.sp500_results_path
    files = [file for file in os.listdir(results_path)
             if file[-4:] == 'xlsx' and '__REPORT__' not in file]
    print(f'readings files: {files}')
    median_sensitivity = 0
    best_sensitivity = 0
    best_stock_sensitivity = ''
    worst_sensitivity = 1
    worst_stock_sensitivity = ''
    median_specificity = 0
    best_specificity = 0
    best_stock_specificity = ''
    worst_specificity = 1
    worst_stock_specificity = ''
    best_odds_ratio = 0
    best_stock_odds_ratio = ''
    median_pvalue = 0
    best_pvalue = 0
    best_stock_pvalue = []
    worst_pvalue = 1
    worst_stock_pvalue = []
    len__ = len(files)
    for f in files:
        stock_name = f.split('__')[0]
        f = results_path + f
        try:
            evaluacion_prediccion_df = pd.read_excel(open(f, 'rb'), sheet_name='evaluacion_prediccion')
            tp, fp, fn, tn = extract_confusion_matrix(evaluacion_prediccion_df)
            odds_ratio, pvalue = extract_fisher(evaluacion_prediccion_df)
            sentivity = 0 if tp + fn == 0 else tp / (tp + fn)
            specificity = 0 if fp + tn == 0 else tp / (fp + tn)

            median_sensitivity += sentivity
            median_specificity += specificity
            median_pvalue += pvalue

            if best_sensitivity < sentivity:
                best_sensitivity = sentivity
                best_stock_sensitivity = stock_name
            if worst_sensitivity > sentivity:
                worst_sensitivity = sentivity
                worst_stock_sensitivity = stock_name
            if best_specificity < specificity:
                best_specificity = specificity
                best_stock_specificity = stock_name
            if worst_specificity > specificity:
                worst_specificity = specificity
                worst_stock_specificity = stock_name
            if odds_ratio != 'inf' and odds_ratio > best_odds_ratio:
                best_odds_ratio = odds_ratio
                best_stock_odds_ratio = stock_name
            if pvalue == best_pvalue:
                best_stock_pvalue.append(stock_name)
            if pvalue == worst_pvalue and pvalue != 1:
                worst_stock_pvalue.append(stock_name)
            if pvalue > best_pvalue:
                best_pvalue = pvalue
                best_stock_pvalue = [stock_name]
            if pvalue < worst_pvalue:
                worst_pvalue = pvalue
                worst_stock_pvalue = [stock_name]

        except Exception as e:
            print(e, f" stock_name: {stock_name}")

    median_sensitivity /= len__
    median_specificity /= len__
    median_pvalue /= len__

    file = [file for file in os.listdir(results_path)
            if file[-4:] == 'xlsx' and '__REPORT__' in file][0]

    report_df = pd.read_excel(open(results_path + file, 'rb'), sheet_name='Sheet1')
    report_df.rename(columns={report_df.columns[0]: ""}, inplace=True)
    complementary = pd.DataFrame([
      ['best_sensitivity', best_stock_sensitivity, best_sensitivity],
      ['best_specificity', best_stock_specificity, best_specificity],
      ['best_odds_ratio', best_stock_odds_ratio, best_odds_ratio],
      ['best_pvalue', best_stock_pvalue, best_pvalue],

      ['worst_sensitivity', worst_stock_sensitivity, worst_sensitivity],
      ['worst_specificity', worst_stock_specificity, worst_specificity],
      ['worst_pvalue', worst_stock_pvalue, worst_pvalue],
      ['median_sensitivity', '', median_sensitivity],
      ['median_specificity', '', median_specificity],
      ['median_pvalue', '', median_pvalue],

    ],
      columns=['', 'stock', 'value'])

    report_df = report_df.append(complementary)
    report_df.to_excel(results_path + file)


read_data()
