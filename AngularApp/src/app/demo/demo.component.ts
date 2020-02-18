import { Component, OnInit } from '@angular/core';
import {Observable, Subject} from 'rxjs';
import {WebcamImage} from 'ngx-webcam';
import * as tf from '@tensorflow/tfjs';
import * as posenet from '@tensorflow-models/posenet';
import {FeatureExtractorService} from './feature-extractor.service';

const POSES = ['BEZ_POZE', 'DIGNUTA_RUKA', 'ISPRUZENA_RUKA_1', 'ISPRUZENA_RUKA_2', 'ISPRUZENA_RUKA_3',
  'ISPRUZENA_RUKA_4', 'POVECAJ_BRZINU', 'PRIDJI_BLIZE', 'SMANJI_BRZINU', 'STAJACA_POZA_1',
  'STAJACA_POZA_2', 'ZAUSTAVI_VOZILO']

@Component({
  selector: 'app-demo',
  templateUrl: './demo.component.html',
  styleUrls: ['./demo.component.scss']
})
export class DemoComponent implements OnInit {

  private net: any;
  private model: any;
  public showWebcam = true;
  private trigger: Subject<void> = new Subject<void>();
  private webcamImage: Subject<WebcamImage> = new Subject<WebcamImage>();
  private imageScaleFactor = 0.75;
  private outputStride = 16;
  public predictedPose = 'BEZ POZE';
  private frameCount = 0;
  public fps = 0;
  public predictions = new Array<number>(12);

  constructor(private featureExtractorService: FeatureExtractorService) { }

  ngOnInit() {
    tf.loadLayersModel('/assets/model.json').then(model => {
      this.model = model;
      posenet.load().then(pn => {
        this.net = pn;
        this.webcamImage.asObservable().subscribe(image => {
          this.processImage(image);
        });
        this.triggerSnapshot();
      });
    });
    setInterval(() => {
      this.fps = this.frameCount;
      this.frameCount = 0;
    }, 1000);
  }

  public triggerSnapshot(): void {
    if (this.showWebcam) { this.trigger.next(); }
  }

  public handleImage(webcamImage: WebcamImage): void {
    // tslint:disable-next-line:no-console
    this.webcamImage.next(webcamImage);
  }

  public get triggerObservable(): Observable<void> {
    return this.trigger.asObservable();
  }

  public toggleWebcam(): void {
    this.showWebcam = !this.showWebcam;
    this.triggerSnapshot();
    console.log('triggered');
  }

  private async processImage(image: WebcamImage) {
    this.net.estimateSinglePose(image.imageData, this.imageScaleFactor, false, this.outputStride).then(async pose => {
      const features = this.featureExtractorService.extract_features_from_pose(pose);
      const prediction = this.model.predict(tf.tensor(features).as3D(1, 1, 20));
      this.predictions = (await prediction.array())[0][0];
      this.predictedPose = POSES[this.predictions.indexOf(Math.max(...this.predictions))];
      this.frameCount += 1;
      this.triggerSnapshot();
    });
  }

  public resetLSTMState() {
    this.model.resetStates();
  }

}
