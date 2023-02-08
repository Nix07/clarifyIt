import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ClarityMetricsComponent } from './clarity-metrics.component';

describe('ClarityMetricsComponent', () => {
  let component: ClarityMetricsComponent;
  let fixture: ComponentFixture<ClarityMetricsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ClarityMetricsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ClarityMetricsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
