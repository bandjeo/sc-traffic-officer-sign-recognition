# Angular Demo Aplikacija
- Aplikacija za demonstriranje prepoznavanje poza u realnom vremenu putem veb kamere. Snimak sa veb kamere se propušta kroz [PoseNet](https://www.tensorflow.org/lite/models/pose_estimation/overview), a zatim kroz istreniranu LSTM mrežu i rezultat predikcije se prikazuje na ekranu.

## Preduslovi
- Node.js

## Pokretanje
- `npm install`
- u assets folderu postaviti model.json i group1-shard1of1.bin na željeni istrenirani model (generisati pomoću convert_to_tensorflowJS)
- `ng serve`
- otvoriti `localhost:4200` u pretraživaču

