import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-exit',
  templateUrl: './exit.component.html',
  styleUrls: ['./exit.component.scss']
})
export class ExitComponent implements OnInit {
  remainingTime = 10;

  constructor() { }

  ngOnInit(): void { }

  onSubmit() {
    window.location.href = 'https://app.prolific.co/submissions/complete?cc=7FB22E97';
  }

}
