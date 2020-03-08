"use strict";

const DatePipe = require('dateformat');

class Utils {
  //static datePipe = new DatePipe('en-US');

  static formatDate(date) {
    const formattedDate = DatePipe(new Date(date), 'yyyy/mm/dd') ;
    return formattedDate;
  }

  static addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }
}

module.exports = Utils;
