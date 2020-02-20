import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { GtrendData } from '../../model/gtrendData.model';
import { ExtractDataService } from '../service/extractdata.service';

@Component({
  selector: 'app-gtrend-list',
  templateUrl: './gtrend-list.component.html',
  styleUrls: ['./gtrend-list.component.css']
})
export class GtrendListComponent implements OnInit, OnDestroy {
  posts: GtrendData;
  private postsSub: Subscription;

  constructor(public postsService: ExtractDataService) {}

  ngOnInit(): void {
    /*this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: any) => {
        this.posts = posts.trendPosts;
      });*/
  }

  ngOnDestroy(): void {
    //this.postsSub.unsubscribe();
  }

}
