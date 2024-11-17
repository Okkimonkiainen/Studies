## Syöpäsolukon tunnistaminen normaalikudoksesta

**Tekijä:** Tiina Tuomisto, tiina.tt.tuomisto@jyu.fi

**Tiivistelmä**: Imusolmukekudoksen syöpäsolukon tunnistaminen normaalista solukosta, Kagglen kilpailun [Histopathologic Cancer Detection](https://www.kaggle.com/competitions/histopathologic-cancer-detection/overview) datasettejä käyttäen.


## Testattu seuraavilla kirjastoilla

- Python 3.9.17
- [Tensorflow 2.9.0](https://www.tensorflow.org/overview/?hl=fi)
- [Pandas  1.5.3](https://pandas.pydata.org/)
- [NumPy 1.25.2](https://numpy.org/)
- [scikit-learn  1.3.0](https://scikit-learn.org/)
- [matplotlib 3.7.1](https://matplotlib.org/)

## Johdanto
[Terveyden ja hyvinvoinnin laitoksen](https://thl.fi/fi/web/kansantaudit/syopa) mukaan syöpään sairastuminen on yleistynyt Suomessa ja siihen sairastuu joka kolmas suomalainen jossakin elämänsä vaiheessa. Syöpäkuolleisuus on kuitenkin vähentynyt tehokkaampien hoitojen ja seulontojen avulla.

Syöpään altistaa erilaiset tekijät, kuten ihmisen genetiikka ja elintavat. Kun ihminen vanhenee, myös elimistön toiminta muuttuu, jolloin riski syövän kehittymiselle myös suurenee. Voidaan siis todeta, että syöpäriski kasvaa ihmisen eliniän noustessa, kun ihmisen omien solujen toiminta ja säätely muuttuu. Syöpä voi alkaa erilaisista kudoksista, jolloin myös syöpää kutsutaan kudospaikan nimen mukaisesti eli puhutaan esimerkiksi rinta-, eturauhas- ja suolistosyövästä. Kehittyneen syövän syöpäsolut voivat metastoitua eli ne voivat tehdä etäpesäkkeitä ihmisen eri kudoksiin, kuten imusolmukkeisiin. 

Tehtävässä pyritään erottamaan normaali imusolmukesolukko, imusolmukkeisiin tunkeutuneista syövän etäpesäkkeistä. Loppuprojektin tekijällä ei ole kokemusta syöpäsolujen tunnistamisesta normaalisolukosta, joten tehtävässä kuvien luokkien oikeellisuutta arvioidaan myös [Comparative Oncology-kirjan](https://www.ncbi.nlm.nih.gov/books/NBK9553/) neuvojen avulla, jossa kerrotaan syöpäsolujen piirteitä:
- Suuri tuma ja sen muoto on poikkeava
- Sytoplasman vähäisyys ja sen voimakas tai vähäinen värikkyys

[Comparative Oncology-kirjan](https://www.ncbi.nlm.nih.gov/books/NBK9553/) mukaan erityisesti solujen tumat ovat merkittäviä solujen pahanlaatuisuuden tarkastelussa. Muutokset esimerkiksi koossa, muodossa ja koossa suhteessa sytoplasmaan ovat merkkejä solun pahanlaatuisuudesta. Pahanlaatuiset solut myös lisääntyvät poikkeavan nopeasti. Tehtävässä pohditaan kuvien luokkien oikeellisuutta esimerkiksi sekaannusmatriisin, f1-scoren ja visuaalisesti tumien avulla. Kuvien luokkia ei pohdita sytoplasman avulla, sillä sen tarkastelu todettiin olevan haasteellisempaa kuin tumien muutosten tarkastelu.




## Tehtävänanto

Työssä tehdään syväoppimismalli, jonka avulla imusolmukkeiden normaalisolukosta voidaan tunnistaa syöpäsolukkoa. Tarkoituksena on luokitella testauksessa käytettävät kuvat, joko syöpä- tai normaalisolukoksi ja tallentaa kuvatiedoston nimi ja sen luokka [submission.csv-tiedostoon](./gs_dnn_ensemble_20231210T1624/submission/submission.csv). Lopuksi tulokset palautetaan Kaggleen arvioitavaksi. 

## Data

Työssä käytetty datasetti saadaan käyttöön osallistumalla [Histopathologic Cancer Detection](https://www.kaggle.com/competitions/histopathologic-cancer-detection/overview)-kilpailuun. Datasetti koostuu opetukseen ja testaukseen käytettävistä kuvista. Molemmille ryhmille on tehty omat csv-tiedostot,train_labels.csv ja sample_submission.csv, jossa vain opetusdatalle, [train_labels.csv](./histopathologic-cancer-detection/train_labels.csv), on annettu kuvien nimien lisäksi myös pohjatotuudet. Molemmissa tiedostoissa on siis paikat kuvan nimelle ja luokalle. 

Opetuksessa käytettäviä kuvia ei olla jaettu erillisiin kansioihin niiden luokkien mukaan eli sen mukaan ovatko ne syöpä- vai normaalisolukkoa, vaan kaikki opetukseen käytettävät kuvat ovat samassa, yhdessä, kansiossa. Testauksessa käytettävien kuvien luokat on tarkoitus tallentaa [submission.csv-tiedostoon](./gs_dnn_ensemble_20231210T1624/submission/submission.csv), kun malli ja ennustukset on saatu valmiiksi.



## Metodologia

Koska tarkoituksena on tunnistaa onko kuvassa syöpäsolukkoa vai normaalisolukkoa, kyseessä on binääriluokitteluongelma. Ennen mallin kehitystä tarkasteltiin opetukseen ja testaamiseen käytettäviä kuvia. Kaikki kuvat olivat samankokoisia 96x96 värillisiä kuvia. Opetusdatassa oli kuitenkin enemmän normaalisolukkoa edustavia kuvia. Normaalisolukkoa oli kuvissa 130908 kappaletta ja syöpäsolukkoa 89117 kappaletta. Koska testidatalle ei ole kerrottu pohjatotuuksia, evaluoinnin helpottamiseksi, alkuperäisestä opetusdatasta jaettiin dataa myös evaluointia varten. Evaluointidataa saatiin tällöin 20 % ja opetusdataan jäi 80 % alkuperäisestä datasta. Koska alkuperäisessä opetusdatassa oli enemmän normaalisolukkoa kuin syöpäsolukkoa, 80 %:n opetusdatasta jätettiin pois normaalisolukkoa niin, että syöpäsolukkokuvien ja normaalisolukkokuvien määrät olivat samat. Kuvat jätettiin värillisiksi. Uusi [opetusdatasetti](./histopathologic-cancer-detection/train_data.csv), [evaluointidatasetti](./histopathologic-cancer-detection/eval_data.csv) ja [testidatasetti](./histopathologic-cancer-detection/test_data.csv) tallennettiin uusiin tiedostoihin ja tiedostossa lukevien kuvien nimien perään lisätiin '.tif'-pääte, kuvien haun helpottamiseksi. 

Opetusdatan kuvia ja niiden pohjatotuuksia tallennettiin havainnollistamaan syöpä- ja normaalisolukkoa (ks. [solukkokuva ja pohjatotuus](./data_pics/gt_examples_traindata.png)). Kuvista huomataan, että normaalisolukon solukuvat ovat siistimmän näköisiä eli esimerkiksi tumien koot ovat samankaltaisia ja tarkkarajaisia, kun taas syöpäsolukossa tumien koot vaihtelevat. 


Mallia rakennettaessa, opetukseen käytettävät kuvat jaettiin opetus- ja validointidataan ja evaluoinnissa käytettiin juuri luotua evaluointidatasettiä. Tehtävään valittiin konvoluutioneuroverkko, CNN, koska se soveltuu hyvin kuvadatan käsittelyyn. Työssä tehtiin ensin yksinkertainen CNN-rakenne (ks. [CNN-malli1](./gs_dnn_ensemble_20231206T1547/model_infos/CNN-1.png), jota testattiin [konfiguraation](./gs_dnn_ensemble_20231206T1547/all_config.txt) avulla. Tällöin oppimistarkkuuksien keskiarvo oli noin 72 % ja validointitarkkuuksien keskiarvo oli noin 70 %. Tällä mallilla opetustarkkuus jämähti epochien puolessa välissä noin 71 %, joten mallin rakennetta muutettiin lisäämällä siihen lisää konvoluutiokerroksia (ks. [CNN-malli2](./gs_dnn_ensemble_20231206T1805/model_infos/CNN-1.png)). Tällä uudella mallilla, [konfiguraatiolla](./gs_dnn_ensemble_20231206T1805/all_config.txt), opetustarkkuuksien keskiarvo oli noin 80 % ja validointitarkkuus noin 78 %. Mallin kerroksia muutettiin vielä enemmän opetustarkkuuden ja validointitarkkuuden parantamiseksi, jolloin saatiin lopullinen malli (ks. [CNN-malli3](./gs_dnn_ensemble_20231210T1624/model_infos/CNN-3.png)). Tämän lisäksi konfiguraatiota muokattiin siten, että suotimien määrä kasvaa enemmän, kun verkossa mennään syvemmälle.

Mallia testatiin erilaisilla konfiguraatioilla, pienillä muutoksilla. Oppimisnopeuden muutokset suuremmaksi kuin 0.001 heikensi oppimistarkkuuksia ja vastaavasti myös suuremman suodinkoon käyttö kuin 3x3 heikensi tarkkuuksia. Tämän takia lopulliseen konfiguraatioon jätettiin suodinkooksi 3. Epochien määrä oli kaikkien mallien konfiguraatioissa pääosin 10 ja toistojen määrä oli tyypillisesti 1, ajankulun vähentämiseksi. Lopullisessa mallissa epochien määrä nostettiin 15, jotta opetustarkkuutta saataisiin suuremmaksi ja malliin lisättiin dropout estämään ylisovittumista ja parantamaan validointitarkkuutta. [Viimeistä CNN-mallia](./gs_dnn_ensemble_20231210T1624/model_infos/CNN-3.png) testattiin siis seuraavanlaisilla [konfiguraatioilla](./param_grid.txt). Malli testattiin siis kuudella eri konfiguraatiolla, joissa erona oli oppimisnopeuden arvot eli 0.001 ja 0.0001 ja dropout-arvot 0.6, 0.5 ja 0.4. Skriptillä kesti noin 6h NVIDIA GeForce GTX 1660 Ti 6GB GPUlla. Tällä mallilla saatiin parhaimmaksi tarkkuudeksi 89.097 %. 

Kun tarkastellaan [opetus- ja validointikäyriä](./gs_dnn_ensemble_20231210T1624/learning_curves.pdf), käyristä huomataan, että ne ovat varsin kohinaisia ja että malleja olisi kannattanut testata useammalla toistolla, jotta oltaisiin saatu parempi käsitys validointi- ja opetusvirheistä ja niiden tarkkuuksista. Validointidataa ei välttämättä ole riittävästi tai sen kuvat eivät edusta niin hyvin treenidatassa nähtyjä kuvia, jolloin kohinaisuus lisääntyy. Kuvista nähdään, että sekä opetus- ja validointivirheet laskevat ja tarkkuudet nousevat. Malli olisi voinut vielä oppia enemmän eli mallin opetusta olisi voinut vielä jatkaa, koska virhekäyriä tarkastelemalla huomataan, että käyrät ovat laskevia, kun taas validointi-ja opetustarkkuudet ovat nousussa. 


## Virheanalyysi
Mallia 3_v1_89.097.hdf5 arvioitiin sekaannusmatriisin, F1-avulla ja manuaalisesti. Sekaannusmatriisin avulla huomataan (ks. [sekaannusmatriisi](./gs_dnn_ensemble_20231210T1624/diagnostic_pics/gt_and_preds_distribution.png)), että evaluointiin käytetyistä kuvista, 68 695 kuvaa on luokiteltu pohjatotuuksien mukaisiin luokkiin ja että 8406 kuvaa luokiteltu väärin. Suhteellisesti syöpäsolukkoa on luokiteltu enemmän väärin, normaalikudokseksi, sekaannusmatriin perusteella.

Valitun mallin suorituskyky evaluointidataa vastaan:

| TP | TN | FN | FP | ACC | PREC | REC | FSCORE
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 25 968 | 42 727 | 2987 | 5419 | 0.89097 | 0.89684 | 0.82735 | 0.86069 |


Evaluointidatassa oli 45714 normaalisolukkokuvaa ja 31387 syöpäsolukkoa. Luokkakohtaisista metriikoista huomataan, että f1-score on parempi luokalla 0 eli normaalisolukolla, arvolla 0.91, kun taas luokalla 1, syöpäsolukolla, arvo on 0.86.  

Virheellisiä ennustuksia esitetään [kuvassa](./gs_dnn_ensemble_20231210T1624/diagnostic_pics/misclassified_examples.png). Kuvista huomataan, että monet kuvat, jotka ovat lähes täysin tyhjiä, ovat ennustettu luokkaan 0 eli normaalisolukoksi, vaikka pohjatotuuksien perusteella kyseessä on syöpäsolukko. Osa pohjatotuuksista ovat myös erikoisia, sillä esimerkiksi viimeinen kuva on lähes tyhjä ja se on luokiteltu syöpäsolukoksi, vaikka kuvan perusteella on hyvin vaikea sanoa, onko kyseessä todella syöpäsolukko. Kuvista voidaan myös huomata, että monissa kuvissa on normaalin näköisiä, tarkkarajaisia ja siistejä tumakuvia, mutta samassa kuvassa voi myös olla epämääräisen muotoisia tumia, jolloin ennustuksen teko voi vaikeutua.




## Tulokset ja jatkotoimenpiteet

Ennustukset tehtiin [Kagglen testidatalle](./histopathologic-cancer-detection/test_data.csv), jossa kuville ei ole olemassa pohjatotuuksia.
Tämän takia ennustusten oikeellisuuden arviointi on haastavaa. Haastavuutta lisää myös se, että on vaikeata arvioida tulosten oikeellisuutta myös visuaalisesti, jos syöpä- ja normaalisolukon tunnistaminen toisistaan ei ole tuttua ja kuten todettiin virheanalyysissä, eräistä kuvista voi olla vaikea erottaa syöpä- ja normaalisolukkoa. Kuvien ja ennustusten visuaalinen tarkastelu voi siis johtaa vääriin tulkintoihin ilman pohjatotuuksia. [Kuvassa](./gs_dnn_ensemble_20231210T1624/unseen_prediction_pics/preds_examples_unseentest.png) nähdään mallin ennustukset kuvakohtaisesti. Jos tarkastellaan kuvia 3 ja 15, kuvien tumat näyttävät tarkkarajaisilta ja saman kokoisilta, jolloin on mahdollista, että nämä ovat luokiteltu oikein normaalisolukoksi. Kuvat, jotka ovat luokiteltu syöpäsolukoksi ovat myös sen näköisiä, että kyseessä voisi olla syöpäsolukkoa, jos tarkastellaan solukon tumien muotoja ja kokoja. Tästä on esimerkkinä kuva 8. Toisaalta joistakin kuvista on vaikeata erottaa onko kuvassa normaalisolukon lisäksi myös syöpäsolukkoa, kuten kuvassa 6, jossa nähdään enimmäkseen siistejä tumarakenteita.

Kun [tulokset](./gs_dnn_ensemble_20231210T1624/submission/submission.csv) palautettiin Kaggleen, julkiseksi pisteeksi saatiin 0.85  ja yksityiseksi pisteeksi 0.77  (ks. [pisteet](./gs_dnn_ensemble_20231210T1624/Kaggle_submission_scores.png)). Pisteytyksen perusteella testidatan ennustuksissa on virheitä ja mallissa olisi siis vielä parantamisen varaa.  

Työssä olisi voinut testata enemmän kuvien muokkausta, esimerkiksi miten mustavalkoisuus olisi vaikuttanut tulosten tarkkuuteen. Tämän lisäksi oltaisiin voitu luoda lisää syöpädataa tai hyödyntää painokertoimia epätasaisen luokkajaon tasapainoittamiseksi ja tarkastella miten nämä olisivat vaikuttaneet tuloksiin.  Tällöin oltaisiin voitu hyödyntää koko opetusdatasetti ja ei olisi tarvinnut jättää opetusdatasta pois normaalisolukkoa. Myös CNN-rakennetta olisi voinut muokata ja testata enemmän erilaisilla syvyyksillä ja tämän takia mallin rakennuskoodista olisi kannattanut tehdä dynaamisempi, jotta erilaisia rakenteita olisi voinut testata kätevämmin. Myös erilaisia konfiguraatioita olisi kannattanut testata enemmän, esimerkiksi epochien määrän suurentaminen vieläkin isommaksi. Mallissa olisi siis vielä parannettavaa. Virheelliset ennustukset syövän tunnistamisessa ovat aina merkittäviä, sillä virheellinen ennuste heikentää potilaan hyvinvointia ja luottamusta terveydenhuoltoon. 