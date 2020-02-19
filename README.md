## Tim
Aleksandar Nedaković SW-21/2016
Branislav Anđelić SW-6/2016

## Pokretanje
- Predprocesiranje: [Node](https://github.com/bandjeo/sc-traffic-officer-sign-recognition/tree/master/Node)
- Treniranje: [Python](https://github.com/bandjeo/sc-traffic-officer-sign-recognition/tree/master/Python)
- Demo: [AngularApp](https://github.com/bandjeo/sc-traffic-officer-sign-recognition/tree/master/AngularApp)

## Definicija problema
Prepoznavanje različitih naredbi koje saobraćajni policajac upućuje učesnicima u saobraćaju telesnim gestovima, sa video snimka, u realnom vremenu.

Gestovi se mogu naći [ovde](https://www.autoskolapavlin.com/tag/naredbe-policajca-u-raskrsnici/).

Primer rešenja za kineske naredbe može se naći [ovde](https://github.com/zc402/ChineseTrafficPolicePose)
## Skup podataka
Skup podataka predstavljaju snimci osoba koje pokazuju saobraćajne naredbe u različitim okruženjima. Snimci su anotirani oznakama za određeni gest u određenom vremenskom rasponu, sa zakašnjenjem od 750 milisekundi od momenta pojavljivanja gesta. Skup podataka sadrži oko 25 minuta snimaka podeljenih na trening i test snimke.
## Metodologija
Metoda za rešavanje ovog problema se deli na dva dela.

Prvi deo je prepoznavanje poze (ili skeleta) osobe na snimku. Za ovaj deo korišćena je [PoseNet](https://www.tensorflow.org/lite/models/pose_estimation/overview) konvoluciona neuronska mreža.

Drugi deo je prepoznavanje različitih naredbi na osnovu skeleta dobijenog iz prethodnog dela. Izlaz iz PoseNet mreže pretvara se u *feature* vektor na osnovu relativne dužine ektremiteta i njihovog ugla u odnosu na vertikalnu osu. Taj vektor je ulaz u LSTM neuronsku mrežu koja za izlaz ima verovatnoće pojavljivanja svake poze za svaki frejm video snimka.

Pre treniranja, snimci su procesirani tako što su pretvoreni u kolekciju slika u PNG formatu, uzimajući 10 frejmova snimka po sekundi. Zatim su pušteni kroz PoseNet mrežu i izvučeni *feature* vektori zajedno sa označenom pozom, za svaki frejm, sačuvani su u _csv_ formatu.

Treniranje LSTM mreže rađeno je nad izlaznim _.csv_ datotekama iz prethodnog koraka. Isečci od nasumično odabranih uzastopnih _N_ frejmova  predstavljaju _batch_ podataka nad kojima se vrši treniranje mreže kroz zadati broj epoha.

Trenirane su različite arhitekture neuronske mreže:
    - jedan LSTM sloj sa 32 jedinice, N = 300
    - jedan LSTM sloj sa 32 jedinice i jedan _dense_ sloj sa 256 jedinica, N = 300
    - jedan LSTM sloj sa 256 jedinica, N = 300
    - jedan LSTM sloj sa 256 jedinica, N = 900
    - jedan LSTM sloj sa 128 jedinica i jedan LSTM sloj sa 64 jedinice, N = 900
    - dva LSTM sloja sa 128 jedinica i jedan LSTM sloj sa 64 jedinice, N = 900

## Evaluacija
Skup podataka podeljen je na trening i test podskupove. Test skup korišćen je za evaluaciju rešenja.

Pošto su nam podjednako značajne i preciznost (ne želimo da se saobraćajna naredba prepozna ako se nije desila) i odziv (ne želimo da se saobraćajna naredba ne prepozna ako se desila), posmatraćemo makro prosek F mera svih klasa. Takođe, pošto nam je bitno i koliko je frejmova snimka tačno klasifikovano u odnosu na ukupan broj frejmova, posmatraćemo i meru tačnosti.

Evaluacije različitih arhitektura se mogu naći u u direktorijumu *Evaluations*.
## Rezultati
Najbolje rezultate imala je arhitektura sa jednim LSTM slojem sa 256 jedinica trenirana nad isečcima snimaka dužine 90 sekundi (N = 900).
    - Makro F-mera: 0.7308
    - Mera tačnosti: 0.7589
    - [Ostale vrednosti](https://github.com/bandjeo/sc-traffic-officer-sign-recognition/blob/master/Evaluations/LSTM256-900f.txt)

## Zaključak
Mreža teško ralikuje slične poze, dok poze sa jedinstvenim karakteristikama lako razaznaje. Ovo može biti posledica premalog skupa podataka. Takodje, za labeliranje skupa podataka nije korišćen alat koji omogućava preciznost na nivou frejma, što dovodi do nekonzistentnosti u skupu podataka.

## Dalja unapređenja
- Proširivanje, veća raznovrsnost i preciznije labeliranje skupa podataka
- Optimizacija hiperparametara
- Isprobavanje drugih mreža za prepoznavanje ljudske poze
