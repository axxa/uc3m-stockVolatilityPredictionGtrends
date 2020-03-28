import pandas as pd
import numpy as np

from constants.CONSTANTS import CONSTANTS

def forecast_data(binary_trend_arr, binary_finance_arr):
  # P: positive
  # N: negative
  # TP: true positive
  # FP: false positive
  # FN: false negative
  # TN: true negative
  tp = 0
  fp = 0
  tn = 0
  fn = 0
  for idx in range(binary_finance_arr.shape[0]):
    if binary_trend_arr[idx] == 1 and binary_finance_arr[idx] == 1:
      tp += 1
    elif binary_trend_arr[idx] == 1 and binary_finance_arr[idx] == 0:
      tn += 1
    elif binary_trend_arr[idx] == 0 and binary_finance_arr[idx] == 1:
      fp += 1
    elif binary_trend_arr[idx] == 0 and binary_finance_arr[idx] == 0:
      fn += 1

  '''
  accuracy: Aciertos totales
  (TP + TN) / (Total)
  '''
  accuracy = (tp + tn) / (tp + tn + fp + fn);
  '''
  precision: Cuantos de los que predigo son correctos
  TP / ( TP + FP )
  '''
  precision = tp / (tp + fp);
  '''
  recall: Ratio de verdaderos positivos
  Cuantos de los que deberia predecir estoy prediciendo?
  TP / P
  '''
  recall = tp / (tp + tn);

  print(f'accuracy: {round(accuracy * 100, 2)}\n'
        f'precision: {round(precision * 100, 2)}\n'
        f'recall: {round(recall * 100, 2)}\n')


def report_final(response_trend_df, response_finance_df, df, trend_statistics, finance_statistics):
    df = df.sort_values(by='date')
    df.reset_index(inplace=True)
    if 'axisNote' in df.columns:
      df = df.drop(['index', 'axisNote'], axis=1)
    else:
      df = df.drop(['index'], axis=1)

    statistics_df = pd.DataFrame({"trend_mean": [],
                                  "trend_std": [],
                                  "finance_mean": [],
                                  "finance_std": []})
    df = df.append(statistics_df, ignore_index=False)
    df.iloc[[0], [5]] = trend_statistics.mean
    df.iloc[[0], [6]] = trend_statistics.std
    df.iloc[[0], [7]] = finance_statistics.mean
    df.iloc[[0], [8]] = finance_statistics.std

    binary_trend_arr = np.array(df['binary_trend'])
    binary_finance_arr = np.array(df['binary_finance'].iloc[1:])
    forecast_data(binary_trend_arr, binary_finance_arr)

    df.to_excel('data' + CONSTANTS.EXTENSION_EXCEL)
    response_trend_df.to_excel('response_trend_df' + CONSTANTS.EXTENSION_EXCEL)
    response_finance_df.to_excel('response_finance_df' + CONSTANTS.EXTENSION_EXCEL)
