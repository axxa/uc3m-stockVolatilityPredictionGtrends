import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
import sklearn.metrics as skl
from sklearn import datasets, metrics, model_selection, svm
import matplotlib.pyplot as plt
import openpyxl

from constants.CONSTANTS import CONSTANTS
import modules.Utils as UTILS

def generate_metrics(binary_trend_arr, binary_finance_arr):
    # P: positive
    # N: negative
    # TP: true positive
    # FP: false positive
    # FN: false negative
    # TN: true negative
    ##################################
    # ############## evaluar el valor predictivo de la serie
    # ############## evaluar el valor predictivo de la serie
    ##################################
    y_true = binary_finance_arr
    y_pred = binary_trend_arr[:-1]

    '''
    Matriz de confusion
    '''
    tn, fp, fn, tp = skl.confusion_matrix(y_true, y_pred).ravel()
    '''
    accuracy: Aciertos totales
    (TP + TN) / (Total)
    skl.accuracy_score(y_true, y_pred)
    '''
    accuracy = (tp + tn) / (tn + fp + fn + tp)
    '''
    precision: Cuantos de los que predigo son correctos
    TP / ( TP + FP )
    skl.precision_score(y_true, y_pred)
    '''
    precision = tp / (tp + fp)
    '''
    recall: Ratio de verdaderos positivos
    Cuantos de los que deberia predecir estoy prediciendo?
    TP / P
    skl.recall_score(y_true, y_pred)
    '''
    recall = tp / (tp + fn)

    f1 = 2 * (precision * recall) / (precision + recall)

    ####################################################################
    # mas metricas # f1, gmeans # curva ROC
    # formula estadistica q calcule la significancia: analisis de cola de williams
    # estadistica para dias que sube y dias que baja, cuente 0 y 1 de las binarias
    # frecuencia de 0 y 1 # problema desbalanceado
    # usar otras metricas o balancear: tomar un chunk de dias para mismo numero de 0 y 1--> under sampling, over sampling
    # analisis dependiente del tiempo: almacenar por periodos
    # almacenar matriz de confusion por stock y tiempo
    # almacenar conteo de 0s y 1s por anios
    ####################################################################
    fpr, tpr, thresholds = skl.roc_curve(y_true, y_pred)
    print(skl.roc_auc_score(y_true, y_pred))
    print(f'skl.auc(fpr, tpr): {skl.auc(fpr, tpr)}')
    print(f'accuracy: {round(accuracy, 4)}\n'
          f'precision: {round(precision, 4)}\n'
          f'recall: {round(recall, 4)}\n'
          f'f1: {round(f1, 4)}'
          )

    pred_df = pd.DataFrame([[accuracy, precision, recall, f1]], columns=['accuracy', 'precision', 'recall', 'f1'])
    matriz_confusion_df = pd.DataFrame([
      ['positiva', tp, fp],
      ['negativa', fn, tn]],
      columns=['', 'positiva', 'negativa'])

    return matriz_confusion_df, pred_df


def report_final(response_trend_df, response_finance_df, df, trend_statistics, finance_statistics, close_ratio_variation):
    df = df.sort_values(by='date')
    df.reset_index(inplace=True)
    if 'axisNote' in df.columns:
      df = df.drop(['index', 'axisNote'], axis=1)
    else:
      df = df.drop(['index'], axis=1)


    statistic_df = pd.DataFrame([
      ['finance', finance_statistics.mean, finance_statistics.std],
      ['trend', trend_statistics.mean, trend_statistics.std]],
      columns=['', 'mean', 'std'])

    binary_trend_arr = np.array(df['binary_trend'])
    binary_finance_arr = np.array(df['binary_finance'].iloc[1:])
    metrics_ = generate_metrics(binary_trend_arr, binary_finance_arr)

    writer = pd.ExcelWriter('resultados' + CONSTANTS.EXTENSION_EXCEL, engine='openpyxl')
    df.to_excel(writer, 'data', index=False)

    UTILS.multiple_dfs([metrics_[0], metrics_[1], statistic_df], 'pred_eval', writer, 1)

    response_trend_df.to_excel(writer, 'google_trends', index=False)
    response_finance_df.to_excel(writer, 'yahoo_finance', index=False)

    writer.save()
    writer.close()

