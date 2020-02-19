import * as ss from 'simple-statistics';

export class ProcessDataService {

  constructor() {}
  /**
   * The standard deviation is the square root of the variance. This is also known as the population standard deviation.
   * It's useful for measuring the amount of variation or dispersion in a set of values.
   * @param jsonArray array containing the values
   * @param attr predicate attribute to calculate de standard deviation
   */
  getStandardDeviation(jsonArray: any[], attr: string): number {
    console.log('getStandardDeviation');
    const array = [];
    jsonArray.map(result => {
      array.push(result[attr]);
    });
    return ss.standardDeviation(array);
  }

  /**
   * The Median Absolute Deviation is a robust measure of statistical dispersion. It is more resilient to outliers than
   * the standard deviation.
   * @param jsonArray TODO
   * @param attr TODO
   */
  getMedianAbsoluteDeviation(jsonArray: any[], attr: string): number {
    console.log('getMedianAbsoluteDeviation');
    const array = [];
    jsonArray.map(result => {
      array.push(result[attr]);
    });
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
    console.log('getSampleCovariance');
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

}
