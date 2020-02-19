import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
import { DatePipe } from '@angular/common';

import * as ss from 'simple-statistics';

import { GtrendData } from '../posts/gtrendData.model';
import { YfinanceData } from '../posts/yfinanceData.model';
import { ProcessDataService } from '../posts/processdata.service';

@Injectable({providedIn: 'root'})
export class ExtractDataService {
  private postsUpdated = new Subject<any>();
  private trendPostsUpdated: GtrendData[] = [];
  private financePostsUpdated: YfinanceData[] = [];
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
            value: post.formattedValue,
            symbol: post.symbol
          };
        });
      }));

    const finance = this.http
    .get<{stockdata: any}>(
      'http://localhost:3000/volatilitypred/extractFinance'
    )
    .pipe(map((postData) => {
      console.log(postData.stockdata);
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
      this.trendPostsUpdated = results[0];
      this.financePostsUpdated = results[1];
      this.postsUpdated
        .next({
          trendPosts: [...this.trendPostsUpdated],
          financePosts : [...this.financePostsUpdated],
          openSigma: this.PROCESSDATASERVICE.getStandardDeviation(this.financePostsUpdated, 'open')
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
