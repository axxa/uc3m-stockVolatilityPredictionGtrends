import { StatisticData } from './statisticData.model';

export class TrendData {
  data: GoogleData[];
  statisticData: StatisticData;
}

export interface GoogleData {
  id: string;
  date: string;
  trendCount: number;
  symbol: string;
}
