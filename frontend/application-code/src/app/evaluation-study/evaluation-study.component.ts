import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
// import { FinalDialogComponent } from '../final-dialog/final-dialog.component';
import { BackendService } from '../services/backend.service';
import { LoaderService } from '../services/loader.service';

@Component({
  selector: 'app-evaluation-study',
  templateUrl: './evaluation-study.component.html',
  styleUrls: ['./evaluation-study.component.scss'],
})
export class EvaluationStudyComponent implements OnInit {
  evaluationData: any;
  hasExperience = true;
  dimensions = [
    { name: 'Easy Wording and Phrasing', selected: false },
    { name: 'Definition of Important Terms', selected: false },
    { name: 'Specification of Desired Solution', selected: false },
    { name: 'Specification of Desired Format of Solution', selected: false },
    { name: 'Specification of Steps to Perform Task', selected: false },
    {
      name: 'Specification of Required Resources to Perform Task',
      selected: false,
    },
    {
      name: 'Statement of Acceptance Criteria for Submissions',
      selected: false,
    },
  ];

  constructor(
    private fb: FormBuilder,
    private backendService: BackendService,
    private loader: LoaderService,
    public dialog: MatDialog,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.evaluationData = this.fb.group({
      experience: ['', []],
      platforms: ['', []],
      most_used_platform: ['', []],
      most_tasks: ['', []],
      q1: ['', [Validators.required]],
      q2: ['', [Validators.required]],
      q3: ['', [Validators.required]],
      q4: ['', [Validators.required]],
      q5: ['', [Validators.required]],
      q6: ['', [Validators.required]],
      q7: ['', [Validators.required]],
      q8: ['', [Validators.required]],
      q9: ['', [Validators.required]],
      q10: ['', [Validators.required]],
      q11: ['', [Validators.required]],
      comment: ['', [Validators.required]],
    });
    this.setValidators();
  }

  isLoading: Subject<boolean> = this.loader.isLoading;

  get experience() {
    return this.evaluationData.get('experience');
  }

  get platforms() {
    return this.evaluationData.get('platforms');
  }

  get most_used_platform() {
    return this.evaluationData.get('most_used_platform');
  }

  get most_tasks() {
    return this.evaluationData.get('most_tasks');
  }

  get q1() {
    return this.evaluationData.get('q1');
  }

  get q2() {
    return this.evaluationData.get('q2');
  }

  get q3() {
    return this.evaluationData.get('q3');
  }

  get q4() {
    return this.evaluationData.get('q4');
  }

  get q5() {
    return this.evaluationData.get('q5');
  }

  get q6() {
    return this.evaluationData.get('q6');
  }

  get q7() {
    return this.evaluationData.get('q7');
  }

  get q8() {
    return this.evaluationData.get('q8');
  }

  get q9() {
    return this.evaluationData.get('q9');
  }

  get q10() {
    return this.evaluationData.get('q10');
  }

  get q11() {
    return this.evaluationData.get('q11');
  }

  get comment() {
    return this.evaluationData.get('comment');
  }

  // openDialog(): void {
  //   const dialogRef = this.dialog.open(FinalDialogComponent, {
  //     width: '400px',
  //   });

  //   dialogRef.afterClosed().subscribe((result) => {
  //     window.close();
  //   });
  // }

  dimensionSelected(index) {
    this.dimensions[index].selected = !this.dimensions[index].selected;
  }

  setValidators() {
    const experienceControl = this.evaluationData.get('experience');
    const platformsControl = this.evaluationData.get('platforms');
    const most_used_platformControl =
      this.evaluationData.get('most_used_platform');
    const most_tasksControl = this.evaluationData.get('most_tasks');

    experienceControl.setValidators([Validators.required]);
    platformsControl.setValidators([Validators.required]);
    most_used_platformControl.setValidators([Validators.required]);
    most_tasksControl.setValidators([Validators.required]);

    experienceControl.updateValueAndValidity();
    platformsControl.updateValueAndValidity();
    most_used_platformControl.updateValueAndValidity();
    most_tasksControl.updateValueAndValidity();
  }

  onSubmit() {
    let selectedDimensions = '';
    for (let i = 0; i < this.dimensions.length; i++) {
      if (this.dimensions[i].selected == true) {
        selectedDimensions += i.toString() + '; ';
      }
    }
    this.evaluationData.value['dimensions'] = selectedDimensions;

    if (this.evaluationData.value['experience'] == '') {
      this.evaluationData.value['experience'] = '0';
    }

    if (this.evaluationData.value['platforms'] == '') {
      this.evaluationData.value['platforms'] = 'None';
    }

    if (this.evaluationData.value['most_used_platform'] == '') {
      this.evaluationData.value['most_used_platform'] = 'None';
    }

    if (this.evaluationData.value['most_tasks'] == '') {
      this.evaluationData.value['most_tasks'] = '0';
    }

    this.backendService
      .submitEvaluationData(this.evaluationData.value)
      .subscribe(
        (response: any) => {
          response = JSON.parse(response);
          if (response.success) {
            this.router.navigate(['/exit']);
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
