import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Subject } from 'rxjs';
import { BackendService } from '../services/backend.service';
import { LoaderService } from '../services/loader.service';
import { tasks } from '../TaskScenarios';

@Component({
  selector: 'app-input-form',
  templateUrl: './input-form.component.html',
  styleUrls: ['./input-form.component.scss'],
})
export class InputFormComponent implements OnInit {
  taskData: any;
  initialTaskTitle = '';
  initialTaskDescription = '';
  scenarioDescription: String;
  submitChecked = false;
  finish = false;
  iterations = 0;
  category;

  constructor(
    private fb: FormBuilder,
    private backendService: BackendService,
    private loader: LoaderService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.taskData = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
    });

    this.taskData.patchValue({
      title: this.backendService.taskTitle,
    });

    this.taskData.patchValue({
      description: this.backendService.taskDescription,
    });
    this.scenarioDescription =
      tasks[this.backendService.scenario].scenario +
      ' Make all necessary assumptions.';
    this.category = this.backendService.category;
  }

  isLoading: Subject<boolean> = this.loader.isLoading;

  onSubmit() {
    this.iterations += 1;
    this.backendService.submitTaskData(this.taskData.value);
  }

  get title() {
    return this.taskData.get('title');
  }

  get description() {
    return this.taskData.get('description');
  }

  evaluationForm() {
    if (this.iterations === 0) {
      alert(
        'You should improve your task description clarity using the tool in iterations. Please close this popup, then unselect the checkbox and click the Evaluate Clarity button.'
      );
    } else {
      this.router.navigate(['/evaluation']);
    }
  }
}
