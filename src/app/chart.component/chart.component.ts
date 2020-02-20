import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { TrendData } from '../model/gtrendData.model';
import { FinanceData } from '../model/yfinanceData.model';
import { StatisticData } from '../model/statisticData.model';

import { ExtractDataService } from '../posts/service/extractdata.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.component.css']
})
export class ChartComponent implements OnInit, OnDestroy {

  private postsSub: Subscription;
  private gtrendData: TrendData = new TrendData();
  private yfinanceData: FinanceData = new FinanceData();

  public chartLabels = [];
  public chartType = 'line';
  public chartLegend = true;

  public chartLabels2 = [];
  public chartType2 = 'line';
  public chartLegend2 = true;

  public chartOptions = {
    scaleShowVerticalLines: false,
    responsive: true,

    scales: {
      xAxes: [{
          afterTickToLabelConversion(data) {
              const xLabels = data.ticks;
              xLabels.forEach((labels, i) => {
                  if (i % 2 === 0) {
                      xLabels[i] = '';
                  }
              });
          }
      }]
  }

  };

  public trendsChartData = [
    {
      data: [],
      label: 'Mean +/- sigma',
      fill: false,
      borderColor: '#ed0c5e',
    },
    {
      data: [],
      label: 'Search count',
      // backgroundColor: '#4dc9f6',
      fill: true,
    },
    {
      data: [],
      label: 'Mean +/- sigma',
      fill: false,
      borderColor: '#ed0c5e',
    },
    {
      data: [],
      label: 'Mean',
      borderColor: '#68de2c',
      fill: false,
    }
  ];

  public financeChartData = [
    {
      data: [],
      label: 'Mean +/- sigma',
      fill: false,
      borderColor: '#ed0c5e',
    },
    {
      data: [],
      label: 'Stock open price',
      fill: true,
    },
    {
      data: [],
      label: 'Mean +/- sigma',
      fill: false,
      borderColor: '#ed0c5e',
    },
    {
      data: [],
      label: 'Mean',
      fill: false,
      borderColor: '#68de2c',
    }
  ];

  constructor(public postsService: ExtractDataService) {}

  ngOnInit(): void {
    this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: any) => {
        this.gtrendData = posts.trendPosts;
        this.yfinanceData = posts.financePosts;
        this.graphChart();
      });
  }

  ngOnDestroy(): void {
    this.postsSub.unsubscribe();
  }

  graphChart() {
    this.gtrendData.data.map(mydata => {
      this.trendsChartData[1].data.push( mydata.trendCount );
      this.trendsChartData[0].data.push( this.gtrendData.statisticData.meanPlusSigma );
      this.trendsChartData[2].data.push( this.gtrendData.statisticData.meanMinusSigma );
      this.trendsChartData[3].data.push( this.gtrendData.statisticData.mean );
    });
    this.gtrendData.data.map(mydata => { this.chartLabels.push( mydata.date ); });

    this.yfinanceData.data.map(mydata => {
        this.financeChartData[1].data.push( mydata.open );
        this.financeChartData[0].data.push( this.yfinanceData.statisticData.meanPlusSigma );
        this.financeChartData[2].data.push( this.yfinanceData.statisticData.meanMinusSigma );
        this.financeChartData[3].data.push( this.yfinanceData.statisticData.mean );
      });
    this.yfinanceData.data.map(mydata => { this.chartLabels2.push( mydata.date ); });
  }

}
