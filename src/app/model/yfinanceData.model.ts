import { StatisticData } from './statisticData.model';

export class YfinanceData {
  data: YahooFinanceData[];
  statisticData: StatisticData;
}

export interface YahooFinanceData {
  id: string;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  symbol: string;
  statisticData: StatisticData;
}
