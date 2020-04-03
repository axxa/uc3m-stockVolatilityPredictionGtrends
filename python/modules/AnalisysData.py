import pandas as pd
import numpy as np
import math

from sklearn.metrics import f1_score
import sklearn.metrics as skl
from sklearn.metrics import roc_curve, auc
from sklearn import datasets, metrics, model_selection, svm
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier

import matplotlib.pyplot as plt
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
def roc_curve(data, target):
    X = data
    y = target
    print(y.shape)
    n_classes = y.shape[0]

    # Add noisy features to make the problem harder
    random_state = np.random.RandomState(0)
    #n_samples, n_features = X.shape
    #X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

    # shuffle and split training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5,
                                                        random_state=0)

    # Learn to predict each class against the other
    classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True,
                                             random_state=random_state))
    y_score = classifier.fit(X_train, y_train).decision_function(X_test)

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
      fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
      roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    # plot

    plt.figure()
    lw = 2
    plt.plot(fpr[2], tpr[2], color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc[2])
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()



def generate_metrics(binary_trend_arr, binary_finance_arr):

    ##################################
    # ############## evaluar el valor predictivo de la serie
    # ############## evaluar el valor predictivo de la serie
    ##################################
    y_true = binary_finance_arr
    y_pred = binary_trend_arr[:-1]

    trend_cero_count = np.count_nonzero(y_pred == 0)
    trend_uno_count = np.count_nonzero(y_pred == 1)
    finance_cero_count = np.count_nonzero(y_true == 0)
    finance_uno_count = np.count_nonzero(y_true == 1)

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
    # fpr, tpr, thresholds = skl.roc_curve(y_true, y_pred)
    # print(skl.roc_auc_score(y_true, y_pred))
    # print(f'skl.auc(fpr, tpr): {skl.auc(fpr, tpr)}')
    print(f'accuracy: {round(accuracy, 4)}\n'
          f'precision: {round(precision, 4)}\n'
          f'recall: {round(recall, 4)}\n'
          f'f1: {round(f1, 4)}'
          )

    pred_df = pd.DataFrame([[accuracy, precision, recall,
                             trend_cero_count, trend_uno_count,
                             finance_cero_count, finance_uno_count]],
                           columns=['accuracy', 'precision', 'recall',
                                    'trend_ceros', 'trend_unos',
                                    'finance_ceros', 'finance_unos'])

    pred2_df = pd.DataFrame([[sensitivity, specificity, g_mean, f1]],
                            columns=['sensitivity', 'specificity', 'g_mean', 'f1'])

    pred3_df = pd.DataFrame([[trend_cero_count, trend_uno_count,
                             finance_cero_count, finance_uno_count]],
                            columns=['trend_ceros', 'trend_unos',
                                     'finance_ceros', 'finance_unos'])

    matriz_confusion_df = pd.DataFrame([
      ['positiva', tp, fp],
      ['negativa', fn, tn]],
      columns=['', 'positiva', 'negativa'])

    roc_curve(y_true, y_pred)

    return matriz_confusion_df, pred_df, pred2_df, pred3_df


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
    metrics_ = list(generate_metrics(binary_trend_arr, binary_finance_arr))
    metrics_.append(statistic_df)

    writer = pd.ExcelWriter('resultados' + CONSTANTS.EXTENSION_EXCEL, engine='openpyxl')
    df.to_excel(writer, 'data', index=False)

    # UTILS.multiple_dfs([metrics_[0], metrics_[1], statistic_df], 'pred_eval', writer, 1)
    UTILS.multiple_dfs(metrics_, 'pred_eval', writer, 1)

    response_trend_df.to_excel(writer, 'google_trends', index=False)
    response_finance_df.to_excel(writer, 'yahoo_finance', index=False)

    writer.save()
    writer.close()

