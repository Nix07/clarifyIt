import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { BackendService } from '../services/backend.service';
import { LoaderService } from '../services/loader.service';
import { tasks } from '../TaskScenarios';

@Component({
  selector: 'app-create-task',
  templateUrl: './create-task.component.html',
  styleUrls: ['./create-task.component.scss'],
})
export class CreateTaskComponent implements OnInit {
  newTaskData: any;
  taskScenario: String;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private backendService: BackendService,
    private loader: LoaderService
  ) {}

  ngOnInit(): void {
    this.newTaskData = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
    });
    this.taskScenario =
      tasks[this.backendService.scenario].scenario +
      ' Make all necessary assumptions.';
  }

  isLoading: Subject<boolean> = this.loader.isLoading;

  get title() {
    return this.newTaskData.get('title');
  }

  get description() {
    return this.newTaskData.get('description');
  }

  onSubmit() {
    this.backendService.submitCreatedTask(this.newTaskData.value).subscribe(
      (response: any) => {
        response = JSON.parse(response);
        if (response.success) {
          this.backendService.taskTitle = this.newTaskData.value.title;
          this.backendService.taskDescription =
            this.newTaskData.value.description;
          this.router.navigate(['/app']);
        } else {
          alert(
            'Something went wrong! Please inform admins with your participant code: ' +
              this.backendService.sessionId +
              ' and try again later.'
          );
          this.router.navigate(['/pre-study']);
        }
      },
      (error) => {
        alert(
          'Something went wrong! Please inform admins with your participant code: ' +
            this.backendService.sessionId +
            ' and try again later.'
        );
        this.router.navigate(['/pre-study']);
      }
    );
  }
}
