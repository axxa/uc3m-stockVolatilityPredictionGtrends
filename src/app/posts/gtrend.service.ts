import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject } from 'rxjs';
import { map } from 'rxjs/operators';

import { GtrendData } from './gtrendData.model';

@Injectable({providedIn: 'root'})
export class GtrendService {
  private posts: GtrendData[] = [];
  private postsUpdated = new Subject<GtrendData[]>();

  constructor(private http: HttpClient) {}

  getPosts() {
    this.http
      .get<{stockdata: any, gtrendsdata: any}>(
        'http://localhost:3000/volatilitypred/extractdata'
      )
      .pipe(map((postData) => {
        console.log(postData);
        return postData.gtrendsdata.map(post => {
          return {
            id: null,
            date: post.formattedTime,
            value: post.formattedValue
          };
        });
      }))

      .subscribe((transformedPosts) => {
        this.posts = transformedPosts;
        this.postsUpdated.next([...this.posts]);
      });
  }

  getPostUpdateListener() {
    return this.postsUpdated.asObservable();
  }

}
