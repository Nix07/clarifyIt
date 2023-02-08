import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app.component';
import { InputFormComponent } from './input-form/input-form.component';
import { ClarityMetricsComponent } from './clarity-metrics/clarity-metrics.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { LoaderInterceptor } from './services/loader.interceptor';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDialogModule } from '@angular/material/dialog';
import { PreStudyComponent } from './pre-study/pre-study.component';
import { AppRoutingModule } from './app-routing.module';
import { ToolComponent } from './tool/tool.component';
import { NgCircleProgressModule } from 'ng-circle-progress';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CreateTaskComponent } from './create-task/create-task.component';
import { EvaluationStudyComponent } from './evaluation-study/evaluation-study.component';
import { Step1InstructionsComponent } from './step1-instructions/step1-instructions.component';
import { Step2InstructionsComponent } from './step2-instructions/step2-instructions.component';
import { ExitComponent } from './exit/exit.component';

@NgModule({
  declarations: [
    AppComponent,
    InputFormComponent,
    ClarityMetricsComponent,
    PreStudyComponent,
    ToolComponent,
    CreateTaskComponent,
    EvaluationStudyComponent,
    Step1InstructionsComponent,
    Step2InstructionsComponent,
    ExitComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    MatCardModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatExpansionModule,
    MatProgressBarModule,
    HttpClientModule,
    MatProgressSpinnerModule,
    AppRoutingModule,
    MatRadioModule,
    MatSelectModule,
    MatIconModule,
    MatSnackBarModule,
    MatButtonToggleModule,
    MatTooltipModule,
    MatCheckboxModule,
    MatDialogModule,
    NgCircleProgressModule.forRoot({}),
    NgbModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: LoaderInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
