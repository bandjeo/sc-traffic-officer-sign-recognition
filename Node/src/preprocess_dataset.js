const fs = require('fs');
require('@tensorflow/tfjs-node-gpu');
const posenet = require('@tensorflow-models/posenet');

const tf = require('@tensorflow/tfjs');
const SCORE_TRESHOLD = 0.5;
const {
    createCanvas, Image
} = require('canvas');
const imageScaleFactor = 0.5;
const outputStride = 16;
const flipHorizontal = false;
const images_fps = 10;

const directory = './dataset/6/'


module.exports.load_images = async (images_path, labels_path) => {
    return new Promise((resolve, reject) => {
        fs.readdir(images_path, function(err, files) {
            if (err) reject(err);
            resolve(files);
        })
    }) 
}

module.exports.get_image_pose = async (image_path, folder_path, net) => {
    const img = new Image();
    img.src = folder_path + image_path;
    const canvas = createCanvas(img.width, img.height);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const pose = await net.estimateSinglePose(canvas, imageScaleFactor, flipHorizontal, outputStride);
    return pose;
}

module.exports.load_labels = async (labels_path) => {
    var labels = JSON.parse(fs.readFileSync(labels_path))
    labels = labels.data.labels.sort((a, b) => a.time - b.time)
    return (function*() {
        for (let label of labels) yield label;
    })()
}

module.exports.extract_features_from_pose = (pose) => {
    const features = [];
    // if keypoint score is lower than threshold, ignore keypoint
    const keypoints = pose.keypoints.map(kp => {
        if (kp.score < SCORE_TRESHOLD) kp.position = null;
        return kp;
    });

    const unit = calculate_unit(keypoints);
    if (unit == -1) {
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
    for(let vector of vectors) {
        if (!vector[0] || !vector[1]) {
            features.push(0);
            features.push(0);
        } else {
            const [pos, intensity] = calculate_vector_intensity(...vector)
            const angle = get_angle(pos);
            features.push(intensity/unit);
            features.push(angle);
        }
    }
    return features;
}

module.exports.create_output_objects = (poses, labels_iterator) => {
    current_label = labels_iterator.next();
    next_label = labels_iterator.next();
    return poses.map((pose, i) => {
        let features = this.extract_features_from_pose(pose);
        if (i * 0.1 > next_label.value.time && !current_label.done) {
            current_label = next_label;
            if (!next_label.done) next_label = labels_iterator.next();
        }
        return {
            features,
            label: current_label.value.label
        }
    })
}

const calculate_unit = (keypoints) => {
    if (keypoints[5].score < SCORE_TRESHOLD && keypoints[6].score < SCORE_TRESHOLD) {
        return -1;
    }
    let shoulder_position;
    if (keypoints[5].score >= keypoints[6].score) {
        shoulder_position = keypoints[5].position;
    } else {
        shoulder_position = keypoints[6].position;
    }
    if (keypoints[0].score > SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[0].position.y;
    } else if (keypoints[3].score > SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[3].position.y;
    }else if (keypoints[4].score > SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[4].position.y;
    }else if (keypoints[1].score > SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[1].position.y;
    }else if (keypoints[2].score > SCORE_TRESHOLD) {
        return shoulder_position.y - keypoints[2].position.y;
    } else {
        return (shoulder_position.y - keypoints[10].position.y) * 2;
    } 
}

// 0 nose
// 1 leftEye
// 2 rightEye
// 3 leftEar
// 4 rightEar
// 5 leftShoulder
// 6 rightShoulder
// 7 leftElbow
// 8 rightElbow
// 9 leftWrist
// 10 rightWrist
// 11 leftHip
// 12 rightHip
// 13 leftKnee
// 14 rightKnee
// 15 leftAnkle
// 16 rightAnkle


const calculate_vector_intensity = (pos1, pos2) => {
    pos = {
        x: pos2.x - pos1.x,
        y: pos2.y - pos1.y
    }
    intensity = Math.sqrt(Math.pow(pos.x, 2) + Math.pow(pos.y, 2))
    return [pos, intensity]
}

const get_angle = (pos) => {
    let angle = Math.atan2(pos.y, pos.x) + 1.5707963267948966
    return angle < 0 ? angle + 6.283185307179586 : angle
}

module.exports.write_output = (filepath, output) => {
    fs.writeFile(filepath, JSON.stringify(output), (err) => {
        if (err) console.log(err);
    })
}


(async function(mod) {
    let start = new Date();
    fs.truncate(`${directory}output.json`, 0, function(){console.log('file truncated')})
    const net = await posenet.load();
    const labels_iterator = await mod.load_labels(`${directory}labels.aucvl`);
    const image_paths = await mod.load_images(`${directory}images`);
    var stream = fs.createWriteStream(`${directory}output.csv`, {flags:'a'});
    let current_label = labels_iterator.next();
    let next_label = labels_iterator.next();
    let labels_done = false;
    for (let i in image_paths) {
        let ip = image_paths[i];
        try {
            console.log('estimating pose for', ip);
            if (i * 0.1 > next_label.value.time && !labels_done) {
                let next = labels_iterator.next();
                if (next.done) {
                    current_label = next_label;
                    labels_done = true;
                }
                else {
                    current_label = next_label;
                    next_label = next;
                }
                console.log('next label', next_label);
            }
            const pose = await mod.get_image_pose(ip, `${directory}images/`, net);
            const features = mod.extract_features_from_pose(pose);
            stream.write(`${current_label.value.label},${features.join(',')}\n`);
        } catch (e) {
            console.log('ERROR estimating pose for', ip, e)
        }
    }
    stream.end();
    console.log('DONE');
    let end = new Date() - start;
    console.log('time elapsed: ', end/1000, 'seconds');
})(this)



