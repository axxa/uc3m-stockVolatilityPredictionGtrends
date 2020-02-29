import { StatisticData } from './statisticData.model';

// P: positive
// N: negative
// TP: true positive
// FP: false positive
// FN: false negative
// TN: true negative
export class ForecastData {
  binaryForecastSerie: ForecastClasses[];
  /**
   * accuracy: Aciertos totales
   * (TP + TN) / (Total)
   */
  accuracy: number;
  /**
   * precision: Cuantos de los que predigo son correctos
   * TP / ( TP + FP )
   */
  precision: number;
  /**
   * recall: Ratio de verdaderos positivos
   * Cuantos de los que deberia predecir estoy prediciendo?
   * TP / P
   */
  recall: number;


}

export enum ForecastClasses {
  TP = 'true_positive',
  FP = 'false_positive',
  TN = 'true_negative',
  FN = 'false_negative',
}
