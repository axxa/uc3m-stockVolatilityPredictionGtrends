import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { GtrendData } from '../gtrendData.model';
import { GtrendService } from '../gtrend.service';

@Component({
  selector: 'app-gtrend-list',
  templateUrl: './gtrend-list.component.html',
  styleUrls: ['./gtrend-list.component.css']
})
export class GtrendListComponent implements OnInit, OnDestroy {
  /*posts = [
    { name: 'First Post', desc : 'This is the first post\s content' },
    { name: 'Second Post', desc : 'This is the second post\s content' },
    { name: 'Third Post', desc : 'This is the third post\s content' }
  ];*/
  posts: GtrendData[] = [];
  private postsSub: Subscription;

  constructor(public postsService: GtrendService) {}

  ngOnInit(): void {
    this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: GtrendData[]) => {
        this.posts = posts;
      });
  }

  ngOnDestroy(): void {
    this.postsSub.unsubscribe();
  }

}
