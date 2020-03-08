import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
import { DatePipe } from '@angular/common';

import { TrendData } from '../../model/gtrendData.model';
import { FinanceData } from '../../model/yfinanceData.model';
import { ForecastData } from '../../model/forecastData.model';

import { ProcessDataService } from './processdata.service';

@Injectable({providedIn: 'root'})
export class ExtractDataService {
  private postsUpdated = new Subject<any>();
  private trendPostsUpdated: TrendData = new TrendData();
  private financePostsUpdated: FinanceData = new FinanceData();
  private forecastData: ForecastData = new ForecastData();
  private PROCESSDATASERVICE: ProcessDataService = new ProcessDataService();

  constructor(private http: HttpClient, private datePipe: DatePipe) {}

  getPosts(trendWord: string, stock: string) {
    const trends = this.http
      .get<{gtrendsdata: any, statisticData: any, binarySeries: any}>(
        'http://localhost:3000/volatilitypred/extractTrends/' + trendWord
      )
      .pipe(map((postData) => {
        postData.gtrendsdata = postData.gtrendsdata.map(post => {
          return {
            id: null,
            date: post.formattedTime,
            trendCount: post.value,
            symbol: post.symbol,
          };
        });
        return postData;
      }));

    const finance = this.http
    .get<{stockdata: any, statisticData: any, binarySeries: any}>(
      'http://localhost:3000/volatilitypred/extractFinance/' + stock
    )
    .pipe(map((postData) => {
      postData.stockdata = postData.stockdata.map(post => {
        return {
          id: null,
          date: post.date,
          open: post.open,
          high: post.high,
          low: post.low,
          close: post.close,
          symbol: post.symbol
        };
      });
      return postData;
    }));
    /*
    const data = this.http
    .get<{stockdata: any, statisticData: any, binarySeries: any}>(
      'http://localhost:3000/volatilitypred/extractData/' + stock
    )
    .pipe(map((postData) => {
      return postData;
    }));
    */
    forkJoin([trends, finance]).subscribe(results => {
      this.trendPostsUpdated.data = results[0].gtrendsdata;
      this.trendPostsUpdated.statisticData = results[0].statisticData;
      this.trendPostsUpdated.binarySeries = results[0].binarySeries;

      this.financePostsUpdated.data = results[1].stockdata;
      this.financePostsUpdated.statisticData = results[1].statisticData;
      this.financePostsUpdated.binarySeries = results[1].binarySeries;

      // this.trendPostsUpdated.binarySeries = this.PROCESSDATASERVICE.generateBinarySeries(this.trendPostsUpdated.data,
      //  'date', 'trendCount', this.trendPostsUpdated.statisticData.meanPlusSigma, this.trendPostsUpdated.statisticData.meanMinusSigma);
      // this.financePostsUpdated.binarySeries = this.PROCESSDATASERVICE.generateBinarySeries(this.financePostsUpdated.data,
      // 'date', 'open', this.financePostsUpdated.statisticData.meanPlusSigma, this.financePostsUpdated.statisticData.meanMinusSigma);
      this.forecastData = this.PROCESSDATASERVICE.generateForecast(this.trendPostsUpdated.binarySeries,
        this.financePostsUpdated.binarySeries);
      this.postsUpdated
        .next({
          trendPosts: this.trendPostsUpdated,
          financePosts : this.financePostsUpdated,
          forecastData: this.forecastData
        });
    });
  }

  getPostUpdateListener() {
    return this.postsUpdated.asObservable();
  }

  formatDate(date: string) {
    const formattedDate = this.datePipe.transform(new Date(date), 'yyyy/MM/dd') ;
    return formattedDate;
  }

}
