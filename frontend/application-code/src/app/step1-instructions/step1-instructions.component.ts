import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { LoaderService } from '../services/loader.service';

@Component({
  selector: 'app-step1-instructions',
  templateUrl: './step1-instructions.component.html',
  styleUrls: ['./step1-instructions.component.scss'],
})
export class Step1InstructionsComponent implements OnInit {
  constructor(private router: Router, private loader: LoaderService) {}

  ngOnInit(): void {}

  isLoading: Subject<boolean> = this.loader.isLoading;

  OnSubmit() {
    this.router.navigate(['/create-task']);
  }
}
