import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import {
  MatInputModule,
  MatCardModule,
  MatButtonModule,
  MatToolbarModule,
  MatExpansionModule,
  MatTabsModule
} from '@angular/material';

import { AppComponent } from './app.component';
//import { PostCreateComponent } from './posts/posts-create/post-create.component';
import { HeaderComponent } from './header/header.component';
//import { PostListComponent } from './posts/post-list/post-list.component';
import { GtrendListComponent } from './posts/gtrend-list/gtrend-list.component';
//import { TabNavComponent } from './tabs/tab.nav.component';

@NgModule({
  declarations: [
    AppComponent,
    //PostCreateComponent,
    HeaderComponent,
    //PostListComponent,
    //TabNavComponent,
    GtrendListComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    BrowserAnimationsModule,
    MatInputModule,
    MatCardModule,
    MatButtonModule,
    MatToolbarModule,
    MatExpansionModule,
    MatTabsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
