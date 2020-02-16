
const tf = require('@tensorflow/tfjs-node-gpu');









const lstm = tf.layers.lstm({ units: 8, returnSequences: true });

// Create an input with 10 time steps.
const input = tf.input({ shape: [10, 20] });
const output = lstm.apply(input);

console.log(JSON.stringify(output.shape));