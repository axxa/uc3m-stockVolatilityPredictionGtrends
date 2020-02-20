import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { GtrendData } from '../model/gtrendData.model';
import { YfinanceData } from '../model/yfinanceData.model';
import { StatisticData } from '../model/statisticData.model';

import { ExtractDataService } from '../posts/service/extractdata.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.component.css']
})
export class ChartComponent implements OnInit, OnDestroy {

  private postsSub: Subscription;
  private gtrendData: GtrendData = new GtrendData();
  private yfinanceData: YfinanceData = new YfinanceData();
  private statisticData: StatisticData;
  /*private openSigma: number;
  private openMean: number;
  private openMeanPlusSigma: number;*/

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
      label: 'Mean + sigma',
      fill: false,
    },
    {
      data: [],
      label: 'Mean - sigma',
      fill: false,
    },
    {
      data: [],
      label: 'Mean',
      fill: false,
    }
  ];

  public chartData2 = [
    {
      data: [],
      label: 'Stock open price'
    },
    {
      data: [],
      label: 'Mean + sigma',
      fill: false,
    },
    {
      data: [],
      label: 'Mean - sigma',
      fill: false,
    },
    {
      data: [],
      label: 'Mean',
      fill: false,
    }
  ];

  constructor(public postsService: ExtractDataService) {}

  ngOnInit(): void {
    this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: any) => {
        this.gtrendData = posts.trendPosts;
        this.yfinanceData = posts.financePosts;

        //this.statisticData = posts.statisticData;
        this.graphChart();
      });
  }

  ngOnDestroy(): void {
    this.postsSub.unsubscribe();
  }

  graphChart() {
    this.gtrendData.data.map(mydata => {
      this.chartData[0].data.push( mydata.value );
      this.chartData[1].data.push( this.gtrendData.statisticData.meanPlusSigma );
      this.chartData[2].data.push( this.gtrendData.statisticData.mean - this.gtrendData.statisticData.sigma );
      this.chartData[3].data.push( this.gtrendData.statisticData.mean );
    });
    this.gtrendData.data.map(mydata => { this.chartLabels.push( mydata.date ); });

    this.yfinanceData.data.map(mydata => {
        this.chartData2[0].data.push( mydata.open );
        this.chartData2[1].data.push( this.yfinanceData.statisticData.meanPlusSigma );
        this.chartData2[2].data.push( this.yfinanceData.statisticData.mean - this.yfinanceData.statisticData.sigma );
        this.chartData2[3].data.push( this.yfinanceData.statisticData.mean );
      });
    this.yfinanceData.data.map(mydata => { this.chartLabels2.push( mydata.date ); });
  }

}
