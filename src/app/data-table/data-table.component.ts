import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable } from '@angular/material/table';
import { DataTableDataSource } from './data-table-datasource';
import { Subscription } from 'rxjs';

import { GtrendData } from '../posts/gtrendData.model';
import { ExtractDataService } from '../posts/extractdata.service';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.css']
})
export class DataTableComponent implements AfterViewInit, OnInit {
  @ViewChild(MatPaginator, {static: false}) paginator: MatPaginator;
  @ViewChild(MatSort, {static: false}) sort: MatSort;
  @ViewChild(MatTable, {static: false}) table: MatTable<GtrendData>;
  dataSource: DataTableDataSource;

  posts: GtrendData[] = [];
  private postsSub: Subscription;

  constructor(public postsService: ExtractDataService) {}

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['date', 'value'];

  ngOnInit() {
    this.dataSource = new DataTableDataSource();

    //this.postsService.getPosts();
    this.postsSub = this.postsService.getPostUpdateListener()
      .subscribe((posts: any) => {
        this.posts = posts.trendPosts;
        this.dataSource.data = this.posts;
      });
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
    this.table.dataSource = this.dataSource;
  }
}
