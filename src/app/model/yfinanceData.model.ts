import { StatisticData } from './statisticData.model';

export class FinanceData {
  data: YahooData[];
  statisticData: StatisticData;
  binarySeries: Map<Date, boolean>;
}

export interface YahooData {
  id: string;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  symbol: string;
  statisticData: StatisticData;
}
