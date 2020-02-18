# Python aplikacija za treniranje i evaluaciju LSTM neuronske mreže

## Preduslovi
- Python3 

### train_nn.py

- Omogućava treniranje neuronske mreže

#### Pokretanje

`python train_nn.py`

#### Opcioni parametri:
- -f broj koji predstavlja naziv direktorijuma u Node/src/dataset u kom je video
nad kojim da se mreža trenira (po default-u se trenira nad svim videima)
- -m path do modela nad kojim će se treniranje nastaviti
- -t broj koliko isečaka za treniranje napraviti po videu
- -e broj epoha treniranja nad pojedinačnim isečkom iz videa
- -r navođenjem ovog parametra će se program beskonačno izvršavati
(po default-u se završi kada obiđe sve potrebne videe)

### test_nn.py

- Omogućava evaluaciju neuronske mreže (tabelirani prikaz prosečnih rezultata za svaku pozu, matrice konfuzije,
odziva, preciznosti, f-mere, mere tačnosti)

#### Pokretanje

`python test_nn.py`

#### obavezni parametri:
- -m path do modela čija evaluacija se vrši

### convert_to_tensorflowJS.py

- Omogućava konverziju iz Keras modela u TensorflowJS model

#### Pokretanje

`python test_nn.py`

#### obavezni parametri:
- -m putanja do modela koji želimo konvertovati
- -nt navođenjem ovog parametra naglašavamo da prosleđeni model nije nastao treniranjem

#### opcioni parametri:
- -o putanja do mesta snimanja konvertovanog modela (po default-u `../AngularApp/src/assets/`)
