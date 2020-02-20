import { StatisticData } from './statisticData.model';

export class GtrendData {
  data: GoogleTrendData[];
  statisticData: StatisticData;
}

export interface GoogleTrendData {
  id: string;
  date: string;
  value: number;
  symbol: string;
}
