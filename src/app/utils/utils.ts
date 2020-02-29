import { DatePipe } from '@angular/common';

export default class Utils {
  static datePipe: DatePipe = new DatePipe('en-US');

  static formatDate(date: string) {
    const formattedDate = this.datePipe.transform(new Date(date), 'yyyy/MM/dd') ;
    return formattedDate;
  }

  static addDays(date: Date, days: number) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }
}
