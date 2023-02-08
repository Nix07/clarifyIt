import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { LoaderService } from '../services/loader.service';

@Component({
  selector: 'app-tool',
  templateUrl: './tool.component.html',
  styleUrls: ['./tool.component.scss'],
})
export class ToolComponent implements OnInit {
  rating: number = 1;
  starCount: number = 5;
  showEvaluationForm = false;
  textLengthFlag = false;

  constructor(
    private loader: LoaderService,
    private router: Router
  ) { }

  ngOnInit(): void { }

  isLoading: Subject<boolean> = this.loader.isLoading;

  evaluationForm() {
    this.router.navigate(['/evaluation']);
  }
}
