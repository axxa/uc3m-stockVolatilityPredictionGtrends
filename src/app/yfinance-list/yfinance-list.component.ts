import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { YfinanceData } from '../posts/yfinanceData.model';
import { ExtractDataService } from '../posts/extractdata.service';

@Component({
  selector: 'app-yfinance-list',
  templateUrl: './yfinance-list.component.html',
  styleUrls: ['./yfinance-list.component.css']
})
export class YfinanceListComponent implements OnInit, OnDestroy {

  posts: YfinanceData[] = [];
  private postsSub: Subscription;

  constructor(public postsService: ExtractDataService) {}

  ngOnInit(): void {
    //this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: any) => {
        this.posts = posts.financePosts;
      });
  }

  ngOnDestroy(): void {
    this.postsSub.unsubscribe();
  }

}
