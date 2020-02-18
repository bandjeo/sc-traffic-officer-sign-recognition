import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FeatureExtractorService {

  private SCORE_TRESHOLD = 0.5;

  constructor() { }

  public extract_features_from_pose(pose) {
    const features = [];
    // if keypoint score is lower than threshold, ignore keypoint
    const keypoints = pose.keypoints.map(kp => {
      if (kp.score < this.SCORE_TRESHOLD) { kp.position = null; }
      return kp;
    });

    const unit = this.calculate_unit(keypoints);
    if (unit === -1) {
      return new Array(20).fill(0);
    }

    // verctors represent body parts
    const vectors = [
      [keypoints[7].position, keypoints[9].position],
      [keypoints[5].position, keypoints[7].position],
      [keypoints[5].position, keypoints[6].position],
      [keypoints[6].position, keypoints[8].position],
      [keypoints[8].position, keypoints[10].position],
      [keypoints[12].position, keypoints[11].position],
      [keypoints[11].position, keypoints[13].position],
      [keypoints[12].position, keypoints[14].position],
      [keypoints[13].position, keypoints[15].position],
      [keypoints[14].position, keypoints[16].position],
    ];

    // features are vector angles and intencities
    for (const vector of vectors) {
      if (!vector[0] || !vector[1]) {
        features.push(0);
        features.push(0);
      } else {
        // @ts-ignore
        const [pos, intensity] = this.calculate_vector_intensity(...vector);
        const angle = this.get_angle(pos);
        // @ts-ignore
        features.push(intensity / unit);
        features.push(angle);
      }
    }
    return features;
  }

  private calculate_unit(keypoints) {
    try {
      if (keypoints[5].score < this.SCORE_TRESHOLD && keypoints[6].score < this.SCORE_TRESHOLD) {
        return -1;
      }
      // tslint:disable-next-line:variable-name
      let shoulder_position;
      if (keypoints[5].score >= keypoints[6].score) {
        shoulder_position = keypoints[5].position;
      } else {
        shoulder_position = keypoints[6].position;
      }
      if (keypoints[0].score > this.SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[0].position.y;
      } else if (keypoints[3].score > this.SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[3].position.y;
      } else if (keypoints[4].score > this.SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[4].position.y;
      } else if (keypoints[1].score > this.SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[1].position.y;
      } else if (keypoints[2].score > this.SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[2].position.y;
      } else {
        return (shoulder_position.y - keypoints[10].position.y) * 2;
      }
    } catch (e) {
      return -1;
    }
  }

  // tslint:disable-next-line:variable-name
  private calculate_vector_intensity(pos1, pos2) {
    const pos = {
      x: pos2.x - pos1.x,
      y: pos2.y - pos1.y
    };
    const intensity = Math.sqrt(Math.pow(pos.x, 2) + Math.pow(pos.y, 2));
    return [pos, intensity];
  };

  private get_angle(pos) {
    const angle = Math.atan2(pos.y, pos.x) + 1.5707963267948966;
    return angle < 0 ? angle + 6.283185307179586 : angle;
  }

}
