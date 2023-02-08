import { Component, OnInit } from '@angular/core';
import { BackendService } from '../services/backend.service';
import { Router, ActivatedRoute } from '@angular/router';
import { LoaderService } from '../services/loader.service';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-pre-study',
  templateUrl: './pre-study.component.html',
  styleUrls: ['./pre-study.component.scss'],
})
export class PreStudyComponent implements OnInit {
  disableUsage = true;
  accptedPrivacyPolicy = false;
  PROLIFIC_PID: string;
  PROLIFIC_STUDY_ID: string;
  PROLIFIC_SESSION_ID: string;
  education: string;
  options = ['Secondary School', 'High School', 'Undergraduate', 'Graduate', 'Doctoral', 'Other'];

  constructor(
    private backendService: BackendService,
    private router: Router,
    private loader: LoaderService,
    private activatedRoute: ActivatedRoute
  ) {
    this.activatedRoute.queryParams.subscribe(params => {
      this.PROLIFIC_PID = params['PROLIFIC_PID'];
      this.PROLIFIC_STUDY_ID = params['STUDY_ID'];
      this.PROLIFIC_SESSION_ID = params['SESSION_ID'];
    });
  }

  ngOnInit(): void {
    this.backendService.sessionStarted = true;
  }

  isLoading: Subject<boolean> = this.loader.isLoading;

  onSubmit() {
    this.backendService
      .submitSessionData({
        education: this.education[0],
        PROLIFIC_PID: this.PROLIFIC_PID ? this.PROLIFIC_PID : 'NA',
        PROLIFIC_STUDY_ID: this.PROLIFIC_STUDY_ID ? this.PROLIFIC_STUDY_ID : 'NA',
        PROLIFIC_SESSION_ID: this.PROLIFIC_SESSION_ID ? this.PROLIFIC_SESSION_ID : 'NA'
      })
      .subscribe(
        (response: any) => {
          if (response.success) {
            this.backendService.sessionId = response.SESSION_ID;
            this.backendService.category = response.SCENARIO;
            this.backendService.scenario = response.TASK_SCENARIO;
            if (response.SCENARIO === '0') {
              // Outside tool scenario
              this.router.navigate(['/first-instructions']);
            } else {
              // Inside tool senario
              this.router.navigate(['/second-instructions']);
            }
          } else {
            alert(
              'Something went wrong while creating the session! Please inform the admins.'
            );
          }
        },
        (error) => {
          alert(
            'Something went wrong while creating the session! Please inform the admins.'
          );
        }
      );
  }
}
