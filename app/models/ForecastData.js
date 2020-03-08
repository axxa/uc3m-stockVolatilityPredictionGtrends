"use strict";

// P: positive
// N: negative
// TP: true positive
// FP: false positive
// FN: false negative
// TN: true negative
class ForecastData {
  binaryForecastSerie;
  /**
   * accuracy: Aciertos totales
   * (TP + TN) / (Total)
   */
  accuracy;
  /**
   * precision: Cuantos de los que predigo son correctos
   * TP / ( TP + FP )
   */
  precision;
  /**
   * recall: Ratio de verdaderos positivos
   * Cuantos de los que deberia predecir estoy prediciendo?
   * TP / P
   */
  recall;

}

module.exports = ForecastData;
