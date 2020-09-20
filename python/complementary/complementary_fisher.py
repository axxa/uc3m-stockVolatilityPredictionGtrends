"""
Este se desarrollo unicamente para entender el concepto del test de fisher,
y como resultado se obtienen dos valores odds_ratio y pvalue
la idea es evaluar la prediccion positiva vs la prediccion negativa

Null hypothesis
The null hypothesis is that the relative proportions of one variable are independent of the second variable;
in other words, the proportions at one variable are the same for different values of the second variable.
In the C. difficile example, the null hypothesis is that the probability of getting cured is the same whether
you receive a fecal transplant or vancomycin.

When one or both of the row or column totals are unconditioned, the Fisher's exact test is not, strictly speaking,
exact. Instead, it is somewhat conservative, meaning that if the null hypothesis is true, you will get a significant
(P<0.05) P value less than 5% of the time

es decir, q [tp, fp] es independiente de [fn, tn], en otras palabaras se esta evaluando que la prediccion positiva
es independiente de la prediccion negativa tanto como el pvalue marque un valor
"""
import pandas as pd
import os
from scipy.stats import fisher_exact
import itertools

from constants.CONSTANTS import CONSTANTS
from modules.Utils import extract_confusion_matrix, extract_fisher


def compute(comp, df):
    mat = df.loc[comp][['Good', 'Bad']]
    ft = fisher_exact(mat)
    return {'comp': " vs ".join(comp), 'OR': ft[0], 'p': ft[1]}


def read_data():
    results_path = "../" + CONSTANTS.dummy_results_path
    files = [file for file in os.listdir(results_path)
             if file[-4:] == 'xlsx' and '__REPORT__' not in file]
    print(f'readings files: {files}')

    for f in files:
        stock_name = f.split('__')[0]
        f = results_path + f
        evaluacion_prediccion_df = pd.read_excel(open(f, 'rb'), sheet_name='evaluacion_prediccion')
        tp, fp, fn, tn = extract_confusion_matrix(evaluacion_prediccion_df)
        df = pd.DataFrame(index=['prediccion positiva', 'prediccion negativa'],
                          data={'Good': [tp, fp], 'Bad': [fn, tn]})

        test = pd.DataFrame([compute(list(i), df) for i in itertools.combinations(df.index.to_list(), 2)])


read_data()
