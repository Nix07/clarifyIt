import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Step2InstructionsComponent } from './step2-instructions.component';

describe('Step2InstructionsComponent', () => {
  let component: Step2InstructionsComponent;
  let fixture: ComponentFixture<Step2InstructionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Step2InstructionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Step2InstructionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
