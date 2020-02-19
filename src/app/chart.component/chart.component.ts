import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { GtrendData } from '../posts/gtrendData.model';
import { YfinanceData } from '../posts/yfinanceData.model';
import { ExtractDataService } from '../posts/extractdata.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.component.css']
})
export class ChartComponent implements OnInit, OnDestroy {

  private postsSub: Subscription;
  private gtrendData: GtrendData[] = [];
  private yfinanceData: YfinanceData[] = [];
  private openSigma: number;

  public chartLabels = [];
  public chartType = 'line';
  public chartLegend = true;

  public chartLabels2 = [];
  public chartType2 = 'line';
  public chartLegend2 = true;

  public chartOptions = {
    scaleShowVerticalLines: false,
    responsive: true
  };

  public chartData = [
    {
      data: [],
      label: 'Search count',
      //backgroundColor: '#4dc9f6',
      //borderColor: '#4dc9f6',
      fill: false,
    },
    {
      data: [],
      label: 'Standard deviation+',
      fill: false,
    },
    {
      data: [],
      label: 'Standard deviation-',
      fill: false,
    }
  ];

  public chartData2 = [
    {
      data: [],
      label: 'Stock open price'
    }
  ];

  constructor(public postsService: ExtractDataService) {}

  ngOnInit(): void {
    this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: any) => {
        this.gtrendData = posts.trendPosts;
        this.yfinanceData = posts.financePosts;
        this.openSigma = posts.openSigma;
        this.graphChart();
      });
  }

  ngOnDestroy(): void {
    this.postsSub.unsubscribe();
  }

  graphChart() {
    this.gtrendData.map(mydata =>
    {
      console.log(mydata.value[0]);
      console.log(this.openSigma);
      console.log(mydata.value[0] + this.openSigma);
      this.chartData[0].data.push( mydata.value[0] );
      this.chartData[1].data.push( mydata.value[0] + this.openSigma );
      this.chartData[2].data.push( mydata.value[0] - this.openSigma );
    });
    this.gtrendData.map(mydata => { this.chartLabels.push( mydata.date ); });

    this.yfinanceData.map(mydata => { this.chartData2[0].data.push( mydata.open ); });
    this.yfinanceData.map(mydata => { this.chartLabels2.push( mydata.date ); });
  }

}
