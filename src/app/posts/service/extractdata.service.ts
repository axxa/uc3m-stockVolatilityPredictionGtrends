import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
import { DatePipe } from '@angular/common';

import { TrendData } from '../../model/gtrendData.model';
import { FinanceData } from '../../model/yfinanceData.model';
import { StatisticData } from '../../model/statisticData.model';

import { ProcessDataService } from './processdata.service';

@Injectable({providedIn: 'root'})
export class ExtractDataService {
  private postsUpdated = new Subject<any>();
  private trendPostsUpdated: TrendData = new TrendData();
  private financePostsUpdated: FinanceData = new FinanceData();
  private PROCESSDATASERVICE: ProcessDataService = new ProcessDataService();

  constructor(private http: HttpClient, private datePipe: DatePipe) {}

  getPosts() {
    const trends = this.http
      .get<{gtrendsdata: any}>(
        'http://localhost:3000/volatilitypred/extractTrends'
      )
      .pipe(map((postData) => {
        return postData.gtrendsdata.map(post => {
          return {
            id: null,
            date: this.formatDate(post.formattedTime),
            trendCount: post.value,
            symbol: post.symbol
          };
        });
      }));

    const finance = this.http
    .get<{stockdata: any}>(
      'http://localhost:3000/volatilitypred/extractFinance'
    )
    .pipe(map((postData) => {
      return postData.stockdata.map(post => {
        return {
          id: null,
          date: this.formatDate(post.date),
          open: post.open,
          high: post.high,
          low: post.low,
          close: post.close,
          symbol: post.symbol
        };
      });
    }));

    forkJoin([trends, finance]).subscribe(results => {
      this.trendPostsUpdated.data = results[0];
      this.financePostsUpdated.data = results[1];
      this.trendPostsUpdated.statisticData = this.PROCESSDATASERVICE.generateStatisticData(this.trendPostsUpdated.data, 'trendCount');
      this.financePostsUpdated.statisticData = this.PROCESSDATASERVICE.generateStatisticData(this.financePostsUpdated.data, 'open');

      this.postsUpdated
        .next({
          trendPosts: this.trendPostsUpdated,
          financePosts : this.financePostsUpdated,
        });
    });
  }

  getPostUpdateListener() {
    return this.postsUpdated.asObservable();
  }

  formatDate(date: string) {
    const formattedDate = this.datePipe.transform(new Date(date), 'yy/MM/dd') ;
    return formattedDate;
  }

}
