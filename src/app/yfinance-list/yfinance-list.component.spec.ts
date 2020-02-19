import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { YfinanceListComponent } from './yfinance-list.component';

describe('YfinanceListComponent', () => {
  let component: YfinanceListComponent;
  let fixture: ComponentFixture<YfinanceListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ YfinanceListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(YfinanceListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
