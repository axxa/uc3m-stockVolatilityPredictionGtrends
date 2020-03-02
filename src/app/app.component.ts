import { Component } from '@angular/core';

import { ExtractDataService } from './posts/service/extractdata.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  public trendWord: string;

  constructor(public postsService: ExtractDataService) {}

  onFireSearch() {
    this.postsService.getPosts(this.trendWord, this.trendWord);
  }
}
