require('@tensorflow/tfjs-node-gpu');
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
        img.src = './ski.jpg';
        const canvas = createCanvas(img.width, img.height);
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        console.log("starting to estimate");
        const pose = await net.estimateSinglePose(canvas, imageScaleFactor, flipHorizontal, outputStride);
        console.log(pose);
    }
    catch (e) {
        console.log(e);
    }
})()