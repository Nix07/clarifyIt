import { Component, OnInit } from '@angular/core';
import { BackendService } from '../services/backend.service';
import { ExplanationTexts } from './ExplanationTexts';

@Component({
  selector: 'app-clarity-metrics',
  templateUrl: './clarity-metrics.component.html',
  styleUrls: ['./clarity-metrics.component.scss'],
})
export class ClarityMetricsComponent implements OnInit {
  overallClarity = 0;
  overallClarityConfidence = 100;
  overallClarityColor = 'warn';
  overallClarityConfidenceColor = '#60d46475';
  featureTypes = [
    'Easy Wording and Phrasing',
    'Definition of Important Terms',
    'Specification of Desired Solution',
    'Specification of Desired Format of Solution',
    'Specification of Steps to Perform Task',
    'Specification of Required Resources to Perform Task',
    'Statement of Acceptance Criteria for Submissions',
  ];
  featureValues = [];
  featureColors = [];
  imageSrc = '../../assets/images/robot-think2.svg';
  confidenceValues = [];
  confidenceColors = [
    '#60d46475',
    '#60d46475',
    '#60d46475',
    '#60d46475',
    '#60d46475',
    '#60d46475',
    '#60d46475',
  ];
  states = [
    'state1',
    'state3',
    'state4',
    'state5',
    'state6',
    'state7',
    'state8',
    'state9',
  ];
  helperFlags = [
    {
      description: true,
      clearExample: false,
      unclearExample: false,
    },
    {
      description: true,
      clearExample: false,
      unclearExample: false,
    },
    {
      description: true,
      clearExample: false,
      unclearExample: false,
    },
    {
      description: true,
      clearExample: false,
      unclearExample: false,
    },
    {
      description: true,
      clearExample: false,
      unclearExample: false,
    },
    {
      description: true,
      clearExample: false,
      unclearExample: false,
    },
    {
      description: true,
      clearExample: false,
      unclearExample: false,
    },
  ];

  helperTexts = ExplanationTexts;

  constructor(private backendService: BackendService) {
    this.backendService.predictionData.subscribe((data: any) => {
      this.backendService.lastToolDataId = data.id;

      this.featureValues = [];
      this.confidenceValues = [];
      this.states.forEach((state) => {
        this.featureValues.push(data.predictions[state].value);
        this.confidenceValues.push(data.predictions[state].confidence);
      });

      this.overallClarity = this.featureValues[0];
      this.overallClarityConfidence = this.confidenceValues[0];

      this.featureValues = this.featureValues.slice(
        1,
        this.featureValues.length
      );
      this.confidenceValues = this.confidenceValues.slice(
        1,
        this.confidenceValues.length
      );

      this.overallClarityColor =
        this.overallClarity > 70
          ? 'primary'
          : this.overallClarity > 30
          ? 'accent'
          : 'warn';
      this.overallClarityConfidenceColor =
        this.overallClarityConfidence > 70
          ? '#60d46475'
          : this.overallClarityConfidence > 30
          ? '#ffab4094'
          : '#f443366e';

      this.computeFeatureColors();
      this.computeConfidenceColors();
    });
  }

  ngOnInit(): void {
    this.overallClarity = 0;
    this.overallClarityConfidence = 100;
    this.overallClarityColor = 'warn';
    this.featureValues = [0, 0, 0, 0, 0, 0, 0];
    this.confidenceValues = [100, 100, 100, 100, 100, 100, 100];
    this.computeFeatureColors();
    this.computeConfidenceColors();
  }

  computeConfidenceColors() {
    this.confidenceColors = [];
    this.confidenceValues.forEach((element) => {
      const color =
        element > 70 ? '#60d46475' : element > 30 ? '#ffab4094' : '#f443366e';
      this.confidenceColors.push(color);
    });
  }

  computeFeatureColors() {
    this.featureColors = [];
    this.featureValues.forEach((element) => {
      const color = element > 70 ? 'primary' : element > 30 ? 'accent' : 'warn';
      this.featureColors.push(color);
    });
  }

  descriptionClicked(state, elem) {
    this.helperFlags[state] = {
      description: true,
      clearExample: false,
      unclearExample: false,
    };
    elem.expanded = false;
  }

  clearExampleClicked(state, elem) {
    this.helperFlags[state] = {
      description: false,
      clearExample: true,
      unclearExample: false,
    };
    elem.expanded = false;
  }

  unclearExampleClicked(state, elem) {
    this.helperFlags[state] = {
      description: false,
      clearExample: false,
      unclearExample: true,
    };
    elem.expanded = false;
  }
}
