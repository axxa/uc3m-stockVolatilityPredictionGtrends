import pandas as pd
import numpy as np
import math
from datetime import datetime

import sklearn.metrics as skl
import scipy.stats as stats
import openpyxl

from constants.CONSTANTS import CONSTANTS
import modules.Utils as UTILS

'''
Matriz de confusion
               | Positive Prediction | Negative Prediction
Positive Class | True Positive(TP) | False Negative(FN)
Negative Class | False Positive(FP) | True Negative(TN)

Sensitivity: how well the positive class was predicted
Specificity: how well the negative class was predicted
g-mean: Measures the balance between classification performances
        on both the majority and minority classes
accuracy: Aciertos totales (TP + TN) / (Total) skl.accuracy_score(y_true, y_pred)
precision: Cuantos de los que predigo son correctos TP / ( TP + FP ) skl.precision_score(y_true, y_pred)
recall: Ratio de verdaderos positivos. Cuantos de los que deberia predecir estoy prediciendo? TP / P
  skl.recall_score(y_true, y_pred)

ROC: Receiver Operating Characteristic
  TruePositiveRate = TruePositive / (TruePositive + FalseNegative)
  FalsePositiveRate = FalsePositive / (FalsePositive + TrueNegative)
'''


# MÉTODO 1
# Precision, Recall y F1.
# En los 3 casos, calcular la función (precision, recall o F1), la misma función usando el parámetro "Binary"
#   y una tercera vez usando "Binary y Weighted".
# Es decir, que vas a obtener 3 valores para cada función.
# Probablemente el último (binary, weighted) sea el que mejor nos venga, pero probemos los 3 a ver qué sale
def metricas_metodo1(y_pred, y_true):
    precision_average_binary = skl.precision_score(y_true, y_pred, average='binary')
    precision_weighted_binary = skl.precision_score(y_true, y_pred, average='weighted')

    recall_average_binary = skl.recall_score(y_true, y_pred, average='binary')
    recall_weighted_binary = skl.recall_score(y_true, y_pred, average='weighted')

    f1_average_binary = skl.f1_score(y_true, y_pred, average='binary')
    f1_weighted_binary = skl.f1_score(y_true, y_pred, average='weighted')

    return precision_average_binary, precision_weighted_binary, \
        recall_average_binary, recall_weighted_binary, \
        f1_average_binary, f1_weighted_binary


# MÉTODO 2:
# normalización = ( x – media ) / desviación típica
# Si cov>0 hay dependencia directa (positiva), es decir, a grandes valores de x corresponden grandes valores de y.
# Si cov=0 Una covarianza 0 se interpreta como la no existencia de una relación lineal entre las dos variables.
# Si cov<0 hay dependencia inversa o negativa, es decir, a grandes valores de x corresponden pequeños valores de y.
def metricas_metodo2(normalizada_trend, normalizada_finance):
    # return np.cov(trend_arr, finance_arr)
    return np.cov(normalizada_trend, normalizada_finance, bias=True)[0][1]

# METODO3
# Normalizamos la serie TRENDS.
# Pintamos un histograma donde el ejeX muestre las marcas de los valores normalizados de la serie TRENDS y el ejeY represente la frecuencia de valores "1" de la serie BINARIZADA COTIZACIONES.
# Si todo va bien, veremos un histograma en forma de curva, donde existirán más valores "1" en el extremo del histograma (que corresponden a valores de TRENDS mayores...)
def metricas_metodo3(prune_trend_df, prune_finance_df, trend_statistics, finance_statistics):
    prune_trend_df['mean_plus_std'] = trend_statistics.mean_plus_std
    prune_trend_df['mean_minus_std'] = trend_statistics.mean_minus_std
    prune_trend_df['mean'] = trend_statistics.mean
    x_arr = ['date', 'date', 'date', 'date', 'date']
    y_arr = ['binary_' + trend_statistics.context, 'mean_plus_std', 'mean_minus_std', 'mean', 'value']
    color_arr = ['blue', 'green', 'green', 'green', 'purple']
    UTILS.create_plot_from_df(prune_trend_df, x_arr, y_arr, color_arr, 'prune_trend_df')

    prune_finance_df['mean_plus_std'] = finance_statistics.mean_plus_std
    prune_finance_df['mean_minus_std'] = finance_statistics.mean_minus_std
    prune_finance_df['mean'] = finance_statistics.mean
    x_arr = ['date', 'date', 'date', 'date']
    y_arr = ['mean_plus_std', 'mean_minus_std', 'mean', 'returns']
    color_arr = ['green', 'green', 'green', 'purple']
    UTILS.create_plot_from_df(prune_finance_df.iloc[1:], x_arr, y_arr, color_arr, 'prune_finance_df')


# MÉTODO 4:
# Calculamos la matriz de confusión.
# Calculamos la "prueba exacta de Fisher" sobre la matriz de confusión.
def metricas_metodo4(y_pred, y_true):
    tn, fp, fn, tp = skl.confusion_matrix(y_true, y_pred).ravel()
    if (tp + fn) == 0:
        sensitivity = 0
    else:
        sensitivity = tp / (tp + fn)
    if (tp + fn) == 0:
        specificity = 0
    else:
        specificity = tp / (fp + tn)
    g_mean = math.sqrt(sensitivity * specificity)
    accuracy = (tp + tn) / (tn + fp + fn + tp)

    if (tp + fp) == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)

    if (tp + fn) == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)
    if (precision + recall) == 0:
        f1 = 0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    true_positive_rate = sensitivity
    if (fp + tn) == 0:
        false_positive_rate = 0
    else:
        false_positive_rate = fp / (fp + tn)

    # pred_df = pd.DataFrame([[accuracy, precision, recall]], columns=['accuracy', 'precision', 'recall'])

    pred2_df = pd.DataFrame([[sensitivity, specificity, g_mean, f1]],
                            columns=['sensitivity', 'specificity', 'g_mean', 'f1'])

    matriz_confusion_df = pd.DataFrame([
      ['clase positiva', tp, fn],
      ['clase negativa', fp, tn]],
      columns=['', 'prediccion positiva', 'prediccion negativa'])

    oddsratio, pvalue = stats.fisher_exact([[tp, fn], [fp, tn]])

    fisher_results_df = pd.DataFrame([
      ['fisher exact test', oddsratio, pvalue]],
      columns=['', 'oddsratio', 'pvalue'])

    return matriz_confusion_df, pred2_df, fisher_results_df  # ,pred_df


##################################
# Objetivo: evaluar el valor predictivo de la serie
##################################
def generate_metrics(prune_trend_df, prune_finance_df, trend_statistics, finance_statistics):
    binary_trend_arr = np.array(prune_trend_df['binary_' + trend_statistics.context])
    binary_finance_arr = np.array(prune_finance_df['binary_' + finance_statistics.context])
    # Se quiere predecir el futuro inmediato por tanto se corre la binaria de finance
    # una posicion y se acorta la binaria de tendencias una posicion

    if (prune_trend_df['date'].iloc[0] - prune_finance_df['date'].iloc[0]).days == 0:
        y_true = binary_finance_arr[1:]
        y_pred = binary_trend_arr[:-1]
    else:
        y_true = binary_finance_arr
        y_pred = binary_trend_arr

    trend_cero_count = np.count_nonzero(y_pred == 0)
    trend_uno_count = np.count_nonzero(y_pred == 1)
    finance_cero_count = np.count_nonzero(y_true == 0)
    finance_uno_count = np.count_nonzero(y_true == 1)

    pred3_df = pd.DataFrame([[trend_cero_count, trend_uno_count,
                             finance_cero_count, finance_uno_count]],
                            columns=['trend_ceros', 'trend_unos',
                                     'finance_ceros', 'finance_unos'])

    metodo1_res = list(metricas_metodo1(y_pred, y_true))
    metodo2_res = metricas_metodo2(np.array(prune_trend_df['norm_trend']),
                                   np.array(prune_finance_df['norm_finance']))
    metricas_metodo3(prune_trend_df, prune_finance_df, trend_statistics, finance_statistics)
    matriz_confusion_df, pred_df, fisher_df = list(metricas_metodo4(y_pred, y_true))

    metodo1_results_df = pd.DataFrame([
      ['precision', metodo1_res[0],  metodo1_res[1]],
      ['recall', metodo1_res[2], metodo1_res[3]],
      ['f1', metodo1_res[4], metodo1_res[5]]],
      columns=['sklearn.metrics', 'binary', 'weighted'])
    metodo2_results_df = pd.DataFrame([[metodo2_res]],
      columns=['covarianza_normalizadas'])

    return matriz_confusion_df, pred_df, fisher_df, pred3_df, metodo1_results_df, metodo2_results_df


def report_final(response_trend_df, response_finance_df,
                 prune_trend_df, prune_finance_df,
                 trend_statistics, finance_statistics):

    prune_trend_df = prune_trend_df.sort_values(by='date')
    prune_finance_df = prune_finance_df.sort_values(by='date')

    prune_trend_df = prune_trend_df.reset_index(drop=True)
    prune_finance_df = prune_finance_df.reset_index(drop=True)
    #if 'index' in prune_trend_df.columns: prune_trend_df = prune_trend_df.drop(['index'], axis=1)
    #if 'axisNote' in prune_trend_df.columns: prune_trend_df = prune_trend_df.drop(['axisNote'], axis=1)

    statistic_df = pd.DataFrame([
      ['finance', finance_statistics.mean, finance_statistics.std],
      ['trend', trend_statistics.mean, trend_statistics.std]],
      columns=['', 'mean', 'std'])

    metrics_ = list(generate_metrics(prune_trend_df,prune_finance_df,
                                     trend_statistics, finance_statistics))
    metrics_.append(statistic_df)

    writer = pd.ExcelWriter('resultados' + CONSTANTS.EXTENSION_EXCEL, engine='openpyxl')
    prune_trend_df.to_excel(writer, 'poda_trend', index=False)
    prune_finance_df.to_excel(writer, 'poda_finance', index=False)

    # UTILS.multiple_dfs([metrics_[0], metrics_[1], statistic_df], 'pred_eval', writer, 1)
    UTILS.multiple_dfs(metrics_, 'evaluacion_prediccion', writer, 1)

    response_trend_df.to_excel(writer, 'google_trends_ori', index=False)
    response_finance_df.to_excel(writer, 'yahoo_finance_ori', index=False)

    writer.save()
    writer.close()

