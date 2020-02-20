import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { YfinanceData } from '../model/yfinanceData.model';
import { ExtractDataService } from '../posts/service/extractdata.service';

@Component({
  selector: 'app-yfinance-list',
  templateUrl: './yfinance-list.component.html',
  styleUrls: ['./yfinance-list.component.css']
})
export class YfinanceListComponent implements OnInit, OnDestroy {

  posts: YfinanceData = new YfinanceData();
  private postsSub: Subscription;

  constructor(public postsService: ExtractDataService) {}

  ngOnInit(): void {
    /*this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: any) => {
        this.posts = posts.financePosts.data;
      });*/
  }

  ngOnDestroy(): void {
    this.postsSub.unsubscribe();
  }

}
