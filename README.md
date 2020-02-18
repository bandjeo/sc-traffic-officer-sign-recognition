## Tim
Aleksandar Nedaković SW-21/2016
Branislav Anđelić SW-6/2016
## Definicija problema
Prepoznavanje različitih naredbi koje saobraćajni policajac upućuje učesnicima u saobraćaju telesnim gestovima, sa video snimka, u realnom vremenu.

Gestovi se mogu naći [ovde](https://www.autoskolapavlin.com/tag/naredbe-policajca-u-raskrsnici/).
## Skup podataka
Skup podataka predstavljaju snimci osoba koje pokazuju saobraćajne naredbe u različitim okruženjima. Snimci su anotirani oznakama za određeni gest u određenom vremenskom rasponu. Ovaj skup podataka potrebno je samostalno kreirati.
## Metodologija
Metoda za rešavanje ovog problema se deli na dva dela.

Prvi deo je prepoznavanje poze (ili skeleta) osobe na snimku. Za ovaj deo biće korišćeno gotovo rešenje. Primer gotovog rešenja može se naći [ovde](https://www.tensorflow.org/lite/models/pose_estimation/overview).

Drugi deo je prepoznavanje različitih naredbi na osnovu skeleta dobijenog iz prethodnog dela. Izlaz iz prethodnog dela se pretvara u skup vektora koji simuliraju kosti tela, ruku i nogu osobe na snimku, i predstavljaju _feature_-e za LSTM neuronsku mrežu. Zadatak mreže je da kategoriše gestove u saobraćajne naredbe (ili odsustvo istih).

Primer rešenja za kineske naredbe može se naći [ovde](https://github.com/zc402/ChineseTrafficPolicePose)
## Evaluacija
Skup podataka će biti podeljen na trening i test podskupove. Test skup će biti korišćen za validaciju rešenja.

Pošto su nam podjednako značajne i preciznost (ne želimo da se saobraćajna naredba prepozna ako se nije desila) i odziv (ne želimo da se saobraćajna naredba ne prepozna ako se desila), posmatraćemo makro prosek F mera svih klasa. Takođe, pošto nam je bitno i koliko je frejmova snimka tačno klasifikovano u odnosu na ukupan broj frejmova, posmatraćemo i meru tačnosti.
