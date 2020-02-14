import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { Color } from 'ng2-charts';

import { GtrendData } from '../posts/gtrendData.model';
import { GtrendService } from '../posts/gtrend.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.component.css']
})
export class ChartComponent implements OnInit, OnDestroy {

  private postsSub: Subscription;
  private gtrendData: GtrendData[] = [];
  public chartLabels = [];
  public chartType = 'line';
  public chartLegend = true;

  public chartOptions = {
    scaleShowVerticalLines: false,
    responsive: true
  };

  public chartData = [
    {data: [], labels: 'Google trends data'}//,
    //{data: [], labels: 'Google trends data'},
  ];

  constructor(public postsService: GtrendService) {}

  ngOnInit(): void {
    this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: GtrendData[]) => {
        this.gtrendData = posts;
        this.graphChart();
      });
  }

  ngOnDestroy(): void {
    this.postsSub.unsubscribe();
  }

  graphChart() {
    this.gtrendData.map(mydata => { this.chartData[0].data.push( mydata.value[0] ); });
    this.gtrendData.map(mydata => { this.chartLabels.push( mydata.date ); });
  }

}
