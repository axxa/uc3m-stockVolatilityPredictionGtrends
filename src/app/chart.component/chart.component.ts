import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

import { TrendData } from '../model/gtrendData.model';
import { FinanceData } from '../model/yfinanceData.model';

import { ExtractDataService } from '../posts/service/extractdata.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.component.css']
})
export class ChartComponent implements OnInit, OnDestroy {

  private postsSub: Subscription;
  public gtrendData: TrendData = new TrendData();
  public yfinanceData: FinanceData = new FinanceData();

  public chartLabels = [];
  public binaryChartLabels = [];
  public binaryChartLabelsSet = new Set();
  public chartType = 'line';
  public chartLegend = true;

  public chartLabels2 = [];

  public chartOptions = {
    scaleShowVerticalLines: false,
    responsive: true,
    scales: {
      xAxes: [{
          afterTickToLabelConversion(data) {
              const xLabels = data.ticks;
              xLabels.forEach((labels, i) => {
                  if (i % 10 !== 0) {
                      xLabels[i] = '';
                  }
              });
          }
      }]
    }
  };

  public binaryChartOptions = {
    scaleShowVerticalLines: false,
    responsive: true,
    scales: {
      yAxes: [{
        afterTickToLabelConversion(data) {
          const xLabels = data.ticks;
          xLabels.forEach((labels, i) => {
              // tslint:disable-next-line: triple-equals
              if (labels != 1.0) {
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

  public binaryComparisonChartData = [
    {
      data: [],
      label: 'trendBinary',
      fill: false
    },
    {
      data: [],
      label: 'financeBinary',
      fill: false
    }
  ];

  constructor(public postsService: ExtractDataService) {}

  ngOnInit(): void {
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

    this.gtrendData.binarySeries.forEach((value: boolean, key: Date, map: Map<Date, boolean>) => {
      this.binaryComparisonChartData[0].data.push(value);
      this.binaryChartLabelsSet.add( key );
    });
    this.yfinanceData.binarySeries.forEach((value: boolean, key: Date, map: Map<Date, boolean>) => {
      this.binaryComparisonChartData[1].data.push(value);
      this.binaryChartLabelsSet.add( key );
    });
    this.binaryChartLabels = Array.from(this.binaryChartLabelsSet.values());
  }

}
