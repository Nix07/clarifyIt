import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PreStudyComponent } from './pre-study.component';

describe('PreStudyComponent', () => {
  let component: PreStudyComponent;
  let fixture: ComponentFixture<PreStudyComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PreStudyComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PreStudyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
