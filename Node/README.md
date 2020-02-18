# Node aplikacija za predprocesiranje podataka
- Aplikacija koristi [PoseNet](https://www.tensorflow.org/lite/models/pose_estimation/overview) za predikciju poza, na osnovu kojih izvači *feature* vektor na osnovu relativnih dužina ektremiteta osobe sa snimka i njihovog ugla u odnosu na vertikalnu osu. Rezultat se smešta u csv datoteku koja se može učitati za treniranje LSTM mreže.

## Predulslovi
- Node.js

## Pokretanje
- `npm install`
- `node ./src/preprocess_dataset.js`

## Postupak predprocesiranja
- Označiti delove snimka sa odgovarajućim labelama poze
    - korišćena je [ova aplikacija](https://github.com/devyhia/action-annotation)
- Pre treniranja potrebno je obraditi svaki snimak (za ovo je korišćen [ffmpeg](https://www.ffmpeg.org/)
    - snimci su skalirani na veličinu 512:512 (nije obavezno, smanjuje vreme predprocesiranja)
        - `ffmpeg -i input.mp4 -vf scale="512:512" output.mp4`
    - snimci su pretvoreni u kolekciju slika u PNG formatu, uzimajući svaki deseti frejm
        - `ffmpeg -i inputFile.mp4 -r 10 outputFile_%05d.png`
- u *dataset* direktorijumu za svaki snimak potrebno je napraviti direktorijum čiji je naziv redni broj snimka u skupu podataka
- jedan takav direktorijum ima sledeću strukuturu
```
> [DIRECTORY NAME]
    > Images
        > [PNG IMAGES]
    > labels.aucvl
```
- *Images* direktorijum treba da sadrži slike koje predstavljaju frejm snimka
- *labels.aucvl* je JSON datoteka generisanja od strane alata za labeliranje podataka
    - u njoj je potrebno zameniti naziv snimka sa vrednosti "labels"
- u datoteci *preprocess_dataset.js* potrebno je izmeniti constantu `directory` na putanju do datoteke sa podacima o željenom snimku
- nakon pokretanja aplikacije predprocesirani podaci će se naći u istom direktorijumu, u datoteci *output.csv*