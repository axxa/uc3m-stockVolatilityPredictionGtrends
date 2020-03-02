import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { ForecastData } from '../model/forecastData.model';
import { ExtractDataService } from '../posts/service/extractdata.service';

@Component({
  selector: 'app-forecast-list',
  templateUrl: './forecast-list.component.html',
  styleUrls: ['./forecast-list.component.css']
})
export class ForecastListComponent implements OnInit, OnDestroy {

  posts: ForecastData;
  private postsSub: Subscription;

  constructor(public postsService: ExtractDataService) {}

  ngOnInit(): void {
    // this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: any) => {
          this.posts = posts.forecastData;
      });
  }

  ngOnDestroy(): void {
    this.postsSub.unsubscribe();
  }

}
