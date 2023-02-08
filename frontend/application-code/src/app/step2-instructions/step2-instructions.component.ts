import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { LoaderService } from '../services/loader.service';

@Component({
  selector: 'app-step2-instructions',
  templateUrl: './step2-instructions.component.html',
  styleUrls: ['./step2-instructions.component.scss'],
})
export class Step2InstructionsComponent implements OnInit {
  constructor(private router: Router, private loader: LoaderService) {}

  ngOnInit(): void {}

  isLoading: Subject<boolean> = this.loader.isLoading;

  OnSubmit() {
    this.router.navigate(['/app']);
  }
}
