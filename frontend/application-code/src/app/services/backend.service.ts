import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ReplaySubject } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class BackendService {
  predictionData = new ReplaySubject(1);
  preditionsCompleted = new ReplaySubject(1);
  sessionStarted = false;
  taskTitle = '';
  taskDescription = '';
  category;
  sessionId;
  lastToolDataId;
  scenario;

  baseURL = 'http://localhost:5000';

  constructor(private http: HttpClient, private router: Router) {}

  submitTaskData(data) {
    data['sessionId'] = this.sessionId;
    const URL = this.baseURL + '/predict';

    this.http.post(URL, data, { responseType: 'json' }).subscribe(
      (response: any) => {
        if (response.success) {
          this.predictionData.next(response);
        } else {
          alert(
            'Something went wrong! Please inform admins with your participant code: ' +
              this.sessionId + ' and try again later.'
          );
          this.router.navigate(['/pre-study']);
        }
      },
      (error) => {
        alert(
          'Something went wrong! Please inform admins with your participant code: ' +
            this.sessionId + ' and try again later.'
        );
        this.router.navigate(['/pre-study']);
      }
    );
  }

  submitSessionData(payload) {
    const URL = this.baseURL + '/session';
    return this.http.post(URL, payload, { responseType: 'json' });
  }

  submitCreatedTask(data) {
    data['sessionId'] = this.sessionId;
    const URL = this.baseURL + '/create-task';
    return this.http.post(URL, data, { responseType: 'json' });
  }

  submitEvaluationData(data) {
    data['sessionId'] = this.sessionId;
    const URL = this.baseURL + '/evaluation';
    return this.http.post(URL, data, { responseType: 'json' });
  }
}
