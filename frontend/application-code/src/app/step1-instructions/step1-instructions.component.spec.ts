import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Step1InstructionsComponent } from './step1-instructions.component';

describe('Step1InstructionsComponent', () => {
  let component: Step1InstructionsComponent;
  let fixture: ComponentFixture<Step1InstructionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Step1InstructionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Step1InstructionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
