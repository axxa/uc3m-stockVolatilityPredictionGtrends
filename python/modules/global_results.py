import enum


class SingleData:
    def __init__(self):
        self.label = ''
        self.stock = ''
        self.single_value = 0.0
        self.values = {}


class GlobalResults:
    set_size = 0

    total_precision_weighted = 0.0
    median_precision_weighted = 0.0
    total_precision_binary = 0.0
    median_precision_binary = 0.0
    total_recall_binary = 0.0
    median_recall_binary = 0.0
    total_recall_weighted = 0.0
    median_recall_weighted = 0.0

    richest_data_stock: SingleData = SingleData()
    poorest_data_stock: SingleData = SingleData()
    poorest_data_stock.single_value = 1.0

    best_precision_weighted: SingleData = SingleData()
    worst_precision_weighted: SingleData = SingleData()
    worst_precision_weighted.single_value = 1.0

    best_precision_binary: SingleData = SingleData()
    worst_precision_binary: SingleData = SingleData()
    worst_precision_binary.single_value = 1.0

    best_recall_weighted: SingleData = SingleData()
    worst_recall_weighted: SingleData = SingleData()
    worst_recall_weighted.single_value = 1.0

    best_recall_binary: SingleData = SingleData()
    worst_recall_binary: SingleData = SingleData()
    worst_recall_binary.single_value = 1.0

    best_f1: SingleData = SingleData()
    worst_f1: SingleData = SingleData()

    most_balanced_binary_trend = SingleData()
    less_balanced_binary_trend = SingleData()
    less_balanced_binary_trend.single_value = 365

    most_balanced_binary_finance = SingleData()
    less_balanced_binary_finance = SingleData()
    less_balanced_binary_finance.single_value = 365

    # best_confusion_mat: SingleData = SingleData()
