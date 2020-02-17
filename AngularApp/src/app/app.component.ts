import { Component } from '@angular/core';
import * as tf from '@tensorflow/tfjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  private model;

  async ngOnInit() {
    try {
      this.model = await tf.loadLayersModel('../convertedModels/model.json');
    }
    catch (e) {
      console.log(e);
    }
  }

}
