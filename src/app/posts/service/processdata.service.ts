import * as ss from 'simple-statistics';

import { StatisticData } from '../../model/statisticData.model';
import { ForecastData } from '../../model/forecastData.model';
import { ForecastClasses } from '../../model/forecastData.model';

import Utils from '../../utils/utils';

export class ProcessDataService {

  constructor() {}
  /**
   * The standard deviation is the square root of the variance. This is also known as the population standard deviation.
   * It's useful for measuring the amount of variation or dispersion in a set of values.
   * @param jsonArray array containing the values
   * @param attr predicate attribute to calculate de standard deviation
   */
  getStandardDeviation(jsonArray: any[], attr: string): number {
    const array = [];
    jsonArray.map(result => {
      array.push(result[attr]);
    });
    return ss.standardDeviation(array);
  }
  getStandardDeviationOv(array: any[]): number {
    return ss.standardDeviation(array);
  }

  /**
   * The mean, also known as average, is the sum of all values over the number of values. This is a measure of
   * central tendency: a method of finding a typical or central value of a set of numbers.
   * @param jsonArray TODO
   * @param attr TODO
   */
  getMean(jsonArray: any[], attr: string): number {
    const array = [];
    jsonArray.map(result => {
      array.push(result[attr]);
    });
    return ss.mean(array);
  }
  getMeanOv(array: any[]): number {
    return ss.mean(array);
  }

  /**
   * The Median Absolute Deviation is a robust measure of statistical dispersion. It is more resilient to outliers than
   * the standard deviation.
   * @param jsonArray TODO
   * @param attr TODO
   */
  getMedianAbsoluteDeviation(jsonArray: any[], attr: string): number {
    const array = [];
    jsonArray.map(result => {
      array.push(result[attr]);
    });
    return ss.medianAbsoluteDeviation(array);
  }
  getMedianAbsoluteDeviationOv(array: any[]): number {
    return ss.medianAbsoluteDeviation(array);
  }
  /**
   * Sample covariance of two datasets: how much do the two datasets move together? x and y are two datasets,
   * represented as arrays of numbers.
   * @param jsonArray1 TODO
   * @param jsonArray2 TODO
   * @param attr1 TODO
   * @param attr2 TODO
   */
  getSampleCovariance(jsonArray1: any[], jsonArray2: any[], attr1: string, attr2: string): number {
    const array1 = [];
    const array2 = [];
    jsonArray1.map(result => {
      array1.push(result[attr1]);
    });
    jsonArray2.map(result => {
      array2.push(result[attr2]);
    });
    return ss.sampleCovariance(array1, array2);
  }

  generateStatisticData(jsonArray: any[], attr: string): StatisticData {
    console.log('generateStatisticData');
    const array = [];
    const statisticData: StatisticData = new StatisticData();
    jsonArray.map(result => {
      array.push(result[attr]);
    });
    statisticData.sigma = this.getStandardDeviationOv(array);
    statisticData.mean = this.getMeanOv(array);
    statisticData.meanPlusSigma = statisticData.mean + statisticData.sigma;
    statisticData.meanMinusSigma = statisticData.mean - statisticData.sigma;
    return statisticData;
  }

  generateBinarySeries(dateValueAttrsContainerArray: any[], dateAttrName: string,
                       valueAttrName: string, positiveTreshold: number,
                       negativeThreshold: number): Map<Date, boolean> {
    const binarySeriesMap = new Map();
    dateValueAttrsContainerArray.map(result => {
      binarySeriesMap.set(result[dateAttrName],
        result[valueAttrName] <= positiveTreshold && result[valueAttrName] >= negativeThreshold ? false : true );
    });
    return binarySeriesMap;
  }

  /**
   * TODO
   * @param useToPredictArray the used array for prediction
   * @param toPredictArray the array to predict
   */
  generateForecast(useToPredictBinarySerie: Map<Date, boolean>, toPredictBinarySerie: Map<Date, boolean>): ForecastData {

    const forecastData = new ForecastData();
    let foreCastClass: ForecastClasses;
    forecastData.binaryForecastSerie = [];
    // tslint:disable-next-line: one-variable-per-declaration
    let tp = 0, tn = 0, fp = 0, fn = 0;
    useToPredictBinarySerie.forEach((trendValue: boolean, key: Date, map: Map<Date, boolean>) => {
      let dateToSearch = new Date(key);
      dateToSearch = Utils.addDays(dateToSearch, 1);
      const strdateToSearch = Utils.formatDate(dateToSearch.toString());
      // console.log('key: ', key, ' dateToSearch: ', dateToSearch, ' strdateToSearch: ', strdateToSearch);
      // @ts-ignore
      const toPredictValue = toPredictBinarySerie.get(strdateToSearch);
      // console.log('comparing trend binary value: ', key, ',', trendValue, ' with:', strdateToSearch, ',', toPredictValue);
      if (toPredictValue != null) {
        if (trendValue === true && toPredictValue === true) {
          foreCastClass = ForecastClasses.TP;
          tp++;
        } else if (trendValue === true && toPredictValue === false) {
          foreCastClass = ForecastClasses.TN;
          tn++;
        } else if (trendValue === false && toPredictValue === true) {
          foreCastClass = ForecastClasses.FP;
          fp++;
        } else if (trendValue === false && toPredictValue === false) {
          foreCastClass = ForecastClasses.FN;
          fn++;
        }
        forecastData.binaryForecastSerie.push(foreCastClass);
        // console.log('result is: ', foreCastClass);
      }
    });

    forecastData.accuracy = (tp + tn) / (tp + tn + fp + fn);
    forecastData.precision = tp / ( tp + fp );
    forecastData.recall = tp / ( tp + tn );

    return forecastData;
  }

}
