import * as ss from 'simple-statistics';

import { StatisticData } from '../../model/statisticData.model';

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

}
