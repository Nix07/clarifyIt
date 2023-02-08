import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { PreStudyComponent } from './pre-study/pre-study.component';
import { ToolComponent } from './tool/tool.component';
import { RegisterGuard } from './register-guard/register.guard';
import { CreateTaskComponent } from './create-task/create-task.component';
import { EvaluationStudyComponent } from './evaluation-study/evaluation-study.component';
import { Step1InstructionsComponent } from './step1-instructions/step1-instructions.component';
import { Step2InstructionsComponent } from './step2-instructions/step2-instructions.component';
import { ExitComponent } from './exit/exit.component';

const routes: Routes = [
  { path: '', redirectTo: '/pre-study', pathMatch: 'full' },
  { path: 'pre-study', component: PreStudyComponent },
  {
    path: 'app',
    component: ToolComponent,
    canActivate: [RegisterGuard],
  },
  {
    path: 'create-task',
    component: CreateTaskComponent,
    canActivate: [RegisterGuard],
  },
  {
    path: 'evaluation',
    component: EvaluationStudyComponent,
    canActivate: [RegisterGuard],
  },
  {
    path: 'first-instructions',
    component: Step1InstructionsComponent,
    canActivate: [RegisterGuard],
  },
  {
    path: 'second-instructions',
    component: Step2InstructionsComponent,
    canActivate: [RegisterGuard],
  },
  {
    path: 'exit',
    component: ExitComponent,
    canActivate: [RegisterGuard],
  },
  { path: '**', redirectTo: '/pre-study', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
