import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EvaluationStudyComponent } from './evaluation-study.component';

describe('EvaluationStudyComponent', () => {
  let component: EvaluationStudyComponent;
  let fixture: ComponentFixture<EvaluationStudyComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EvaluationStudyComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EvaluationStudyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
