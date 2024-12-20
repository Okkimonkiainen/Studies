
# Opintojen aikana suoritettuja projekteja ja muutamia kurssitehtäviä. 
## 1. Cloud Computing: SOA and Cloud Computing 
Kurssilla käytettiin:
- Java
- JavaScript
- HTML ja CSS
- AWS, Heroku...
  
Koostuu useammista tehtävistä, jotka on tehty Javalla. Tehtävät käsittelevät SOAa, SOAPia, RESTful Web-palveluita, pilvilaskentaa ja web-palveluiden hallintaa. 
Jokaiselle tehtävälle on tehty PowerPoint-esitys. Kurssi suoritettiin englanniksi.\
[Tehtävässä 6](https://github.com/Okkimonkiainen/Studies/tree/main/CloudComputing/Task6) käytettiin AWS:ää lääketietokannan teossa ja käytössä.

## 2. Deeplearning: Syväoppimisen perusteet
Loppuprojektissa käytettiin:
- Python, tensorflow
- Kaggle
  
Projektissa tehtiin malli, joka luokittelee kudosnäytteet joko syöpäkudokseksi tai normaaliksi kudokseksi (binääriluokittelu).
Suurien tiedostokokojen takia, projekti on katsottavissa [GitLabissa](https://gitlab.jyu.fi/tuomtryu/loppuprojekti_ties4141).

## 3. Embedded systems: Sulautetut järjestelmät -loppuprojekti
Loppuprojektissa käytettiin:
- C++
- Python, flask
- CSS
- SQL
- PythonAnywhere
- Gmail

PÄIVITYKSESSÄ OLEVA VERSIO NÄHTÄVISSÄ: [MedicineStorage](https://github.com/Okkimonkiainen/MedicineStorage)
Projektissa tehtiin järjestelmä, jonka avulla lääkehuoneen tilan olosuhteita voidaan valvoa. Huoneeseen sijoitettiin neljä ESP32-alustaa (4 solmua), joista yksi keräsi kaikilta solmuilta saadut tiedot ja
lähetti ne eteenpäin tietyin aikavälein PythonAnywheressä olleelle web-palvelimelle. Sensoreista kerätty data tallennettiin PythonAnywheressä sijaitsevaan tietokantaan. Projektissa tehtiin käyttöliittymä, jossa
 käyttäjältä vaadittiin salasana ja käyttäjätunnus lääkehuoneen eri tilojen olosuhteiden tarkastelemiseksi. Käyttäjä pystyi tarkastelemaan lääkehuoneen eri alueiden olosuhteita ja hän sai reaaliaikaisesti tiedon poikkeavista arvoista käyttöliittymään, jolloin käyttäjän tuli kuitata poikkeava-arvo. Poikkeavien arvojen kuittaus tallennettiin tietokantaan. Hälytys poikkeavasta arvosta lähetettiin myös käyttäjän sähköpostiin.\
Koska mittaukset ja kuittaukset tallennettiin tietokantaan käyttäjä pystyi myös tarkastelemaan aikaisempien päivien mittauksia hakutoiminnon avulla ja käyttäjän sähköpostiin voitiin lähettää
joka päivä klo 7.00 kooste edellisen päivän mittausarvoista ja poikkeavista arvoista.
Loppuprojektin käyttöliittymästä ja toiminnasta on kuvia [projektin loppuraportissa](https://github.com/Okkimonkiainen/Studies/blob/main/EmbeddedSystems/fridge-project-main/Sensoriverkkoprojekti___Loppuraportti.pdf).

## 4. Object-oriented programming (OOP): Olio-ohjelmointi
Kurssilla käytettiin:
- Java

Harjoitustyönä tehtiin urheilupäiväkirja-sovellus, jossa käyttäjä voi lisätä ja tarkastella suorituksiaan.
Harjoitustyön tavoitteita ja kuvia sille tehdystä käyttöliittymästä voidaan tarkastella [harjoitustyön raportista](https://github.com/Okkimonkiainen/Studies/blob/main/OOP/olioraportti_tuomisto_rauma.pdf). 

## 5. Programming 2: Ohjelmointi 2 -loppuprojekti
Loppuprojektissa käytettiin:
- C#

Harjoitustyönä tehtiin sovellus, jonka avulla voidaan tallentaa, muokata, poistaa ja tarkastella yrityksen henkilöstön tietoja.
Henkilöstön tiedot tallentuvat myös erilliseen tiedostoon tietokoneelle. \
Harjoitustyön tavoitteita ja käyttöliittymän kuvia ja toimintaa voidaan tarkastella [harjoitustyön raportista](https://github.com/Okkimonkiainen/Studies/blob/main/Programming2/Harjoitustyo/Ohjelmointi2_raportti.pdf).

## 6. WebJS: Web-käyttöliittymien teko
Kurssilla käytettiin:
- JavaScript
- HTML ja CSS

### 6.1. Tehtävä 3 Tulospalvelu:
Tehtävässä voidaan lisätä uusi joukkue ja sen jäsenet. Jäsen-kenttiä muodostuu lisää, jos jäsen1 ja jäsen2 -kentissä on syöte.
Luotu joukkue sijoitetaan joukkuelistaan aakkosjärjestyksen mukaisesti. Listassa jo olevien joukkueiden tietoja voidaan myös muokata,
klikkaamalla joukkueiden nimiä. Tehtävässä voidaan lisätä myös uusia leimaustapoja, joka lisätään leimaustapa-listaan aakkosjärjestyksen mukaisesti. 
[Tarkastele tehtävää 3](http://users.jyu.fi/~tuomtryu/TIEA2120/VT3/pohja.xhtml)

### 6.2. Tehtävä 4 Animaatiot:
Tehtävässä on kokeiltu erilaisten visuaalisten elementtien käyttöä. Käyttäjä voi lisätä reunaa kiertäviä pingviinejä vasemman yläreunan painonapin avulla tai
piilottaa näytöllä liikkuva elementtejä vasemman alareunan valintaruutujen avulla. 
Vasemman alareunan valintaruutujen skrolleri-ruutu ei ole käytössä. Oikean yläreunan palkin avulla, voidaan muuttaa kulmastakulmaan kulkevien väripalkkien paksuutta.\
[Tarkastele tehtävää 4](http://users.jyu.fi/~tuomtryu/TIEA2120/VT4/pohja.xhtml)

### 6.3. Tehtävä 5 Kartta (Huom! Kaikki ominaisuudet eivät enää toimi):
*(lähdetiedostoihin tullut muutoksia, joiden takia kartalle ei piirry joukkueiden kulkemia matkoja)*
Tehtävässä pystyi siirtämään joukkueiden nimiä Kartalle-ruutuun, jolloin kyseisen joukkueen kulkema matka piirrettiin kartalle. \
[Tarkastele tehtävää 5: HUOM! Matkat eivät enää piirry kartalle!](http://users.jyu.fi/~tuomtryu/TIEA2120/VT5/pohja.html)



