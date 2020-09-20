from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

from constants.CONSTANTS import CONSTANTS


def extract_confusion_matrix(evaluacion_prediccion_df):
    evaluacion_prediccion_df = evaluacion_prediccion_df.loc[:1, 'prediccion positiva': 'prediccion negativa']
    tp = evaluacion_prediccion_df.iloc[0]['prediccion positiva']
    fp = evaluacion_prediccion_df.iloc[1]['prediccion positiva']
    fn = evaluacion_prediccion_df.iloc[0]['prediccion negativa']
    tn = evaluacion_prediccion_df.iloc[1]['prediccion negativa']
    return tp, fp, fn, tn


def extract_fisher(evaluacion_prediccion_df):
    evaluacion_prediccion_df = evaluacion_prediccion_df.loc[7:7, 'prediccion positiva': 'prediccion negativa']
    odds_ratio = evaluacion_prediccion_df.iloc[0]['prediccion positiva']
    pvalue = evaluacion_prediccion_df.iloc[0]['prediccion negativa']
    return odds_ratio, pvalue


def split_df_by_years(dt, date_column_name):
    dt['year'] = dt[date_column_name].dt.year
    return [dt[dt['year'] == y] for y in dt['year'].unique()], dt['year'].unique()


def check_date_range_by_days(start: str, end: str):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    delta = end - start
    return delta.days


def get_range_dates_by_chunks(start: str, end: str, window: int):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")

    i = True
    chunk_final_date = start
    while chunk_final_date < end:
        if chunk_final_date != start:
            start = chunk_final_date + timedelta(days=1)

        chunk_final_date = chunk_final_date + timedelta(days=window)
        if chunk_final_date > end:
            chunk_final_date = end
        yield str(start.strftime("%Y-%m-%d")), str(chunk_final_date.strftime("%Y-%m-%d"))


def multiple_dfs(df_list, sheets, writer, spaces):
    row = 0
    for dataframe in df_list:
        dataframe.to_excel(writer, sheet_name=sheets, startrow=row, startcol=0)
        row = row + len(dataframe.index) + spaces + 1


def create_plot_from_df(df, x_arr, y_arr, color_arr, plot_name, path):
    # gca stands for 'get current axis'
    ax = plt.gca()
    for idx, value in enumerate(x_arr):
        df.plot(kind='line', color=color_arr[idx], x=value, y=y_arr[idx], ax=ax)

    plt.savefig(path + str(plot_name) + '.png')
    plt.clf()
