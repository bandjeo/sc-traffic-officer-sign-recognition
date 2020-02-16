require('@tensorflow/tfjs-node-gpu');
const tf = require('@tensorflow/tfjs')
const posenet = require('@tensorflow-models/posenet');
const {
    createCanvas, Image
} = require('canvas');
const imageScaleFactor = 0.5;
const outputStride = 16;
const flipHorizontal = false;


(async () => {
    try {
        const net = await posenet.load();
        const img = new Image();
        img.src = './poza.jpg';
        const canvas = createCanvas(img.width, img.height);
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        const pose = await net.estimateSinglePose(canvas, imageScaleFactor, flipHorizontal, outputStride);
        console.log(pose);
        console.log(pose.keypoints);
    }
    catch (e) {
        console.log(e);
    }
})()