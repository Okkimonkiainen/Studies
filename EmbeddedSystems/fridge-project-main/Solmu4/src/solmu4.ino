#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <Arduino.h>
#include <esp_now.h>
#include <HTTPClient.h>
#include "ESPAsyncWebServer.h"
// Lisää secrets.h tiedosto samaan kansioon tämän tiedoston kanssa ja lisää sinne oman kotiverkkosi tiedot
#include "secrets.h"
#include <WiFi.h>

//WiFi:n tiedot:
const char* ssid = SECRET_SSID; //Secret_ssid löytyy secrets.h tiedoststa.
const char* password = SECRET_PASS; // Secret_pass löytyy secrets.h tiedostosta.
const int oneWireBus = 4;

// Määritellään lähettävien (master) laitteiden mac-osoitteet. Näitä käytetään funktiossa, joka ottaa viestit vastaan.
String board3Mac = "c0:49:ef:01:f4:bc";
String board2Mac = "c0:49:ef:08:ce:ac";
String board1Mac = "c0:49:ef:08:db:10";

//oneWire-instanssi: muiden OneWire-laitteiden keskustelua varten:
OneWire oneWire(oneWireBus);

//oneWire-viite annetaan Dallas Temperaturelle:
DallasTemperature sensors(&oneWire);

// Muuttujat ajastinta varten.
long lastTrigger = millis();
long now;

//Booleanin avulla tarkistetaan, että sensorit ovat lähettäneet uudet arvot solmu4:lle
boolean viestivastaanotettu=false;

//ESP-NOW YHTEYS, vastaanottoja:
//viestien rakenne vastaanotettavaa dataa varten:

// Solmu 1:n viesti
typedef struct struct_message_board1{
  int id;
  float temp;
  int kosteus;
  int ilmanpaine;
  int valo;
  int ovi;
} struct_message_board1;

// Solmu 2: viesti
typedef struct struct_message_board2{
  int id;
  float temp1;
  float temp2;
  int ovi;
} struct_message_board2;

// Solmu 3:n viesti
typedef struct struct_message_board3{
  int id;
  float temp;
  int valo;
} struct_message_board3;

struct_message_board1 board1;
struct_message_board2 board2;
struct_message_board3 board3;

// Määritellään palvelimen osoitteen alku. Loppuosa lisätään funktiossa, jossa otetaan viestit vastaan.
String webpalvelinURL="https://laakehuone.eu.pythonanywhere.com/update-sensor?";


//Funktiossa tarkistetaan, miltä solmulta saadaan sensoriarvoja ja tallennetaan ne muuttujiin:
void OnDataRecv(const uint8_t * mac_addr, const uint8_t *incomingData, int len) {

  char macStr[18];
  Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.println(macStr);
  String makki = macStr;

  // If -lauseissa tarkistetaan mitä solmua mac-osoite vastaa ja poimitaan viestistä vastaanotetut tiedot ja lisätään ne URL-osoitteeseen

  if(makki == board1Mac){
    memcpy(&board1, incomingData, sizeof(board1));
    webpalvelinURL = webpalvelinURL + "solmu="+ board1.id + "&lampotila1="+ board1.temp + "&kosteus="+ board1.kosteus + "&ilmanpaine=" + board1.ilmanpaine + "&valo=" + board1.valo + "&ovi=" + board1.ovi;
  }

  if(makki == board2Mac){
    memcpy(&board2, incomingData, sizeof(board2));
    webpalvelinURL = webpalvelinURL + "solmu="+ 2 + "&lampotila1="+ board2.temp1 + "&lampotila2="+ board2.temp2 + "&ovi=" + board2.ovi;  
  }

  if(makki == board3Mac){
    memcpy(&board3, incomingData, sizeof(board3));
    webpalvelinURL = webpalvelinURL + "solmu="+ 3 + "&lampotila1="+ board3.temp + "&valo="+ board3.valo;    
  }

  // Viestivastaanotettu muuttuja asetetaan arvoon "true" --> Silmukassa päästään kutsumaan funktiota, joka tekee HTTP -pyynnön
  viestivastaanotettu=true;
}



//Funktiossa lähetetään kaikilta solmuilta saadut sensoriarvot web-palvelimelle: 
void tietojenLahetys(){

  // Tarkistetaan ensiksi onko yhteys reitittimeen kunnossa.
  if(WiFi.status()== WL_CONNECTED){
    Serial.println("WiFi on yhdistettynä urlia varten");

    // Luodaan HTTP client
    HTTPClient http;

    //Määritellään url, johon tiedot lähetetään, tietokantaan tallentamista varten:

    Serial.println("WEB palvelimen koottu url:");
    Serial.println(webpalvelinURL);
    http.begin(webpalvelinURL);
    //Tehdään pyyntö:
    int httpKoodi=http.GET();
    Serial.println("HTTP-KOODI:");
    Serial.println(httpKoodi);
    //Tarkistetaan vastaanotettu koodi:
    if (httpKoodi>0){
      String payload=http.getString();
    }
    else{
      Serial.println("Virhe HTTP-pyynnön lähettämisessä");
    }
    //Vapautetaan resurssit:
    http.end();
  }else{
    Serial.println("Ei yhteyttä WiFiin");
  }
  // Viestin lähettämisen jälkeen asetetaan URL "perusmuotoon".
  webpalvelinURL = "https://laakehuone.eu.pythonanywhere.com/update-sensor?";
}

void setup(void)
{
  // Käynnistetään serialportti
  Serial.begin(115200);
  Serial.println("Setup started");

  //ESP-NOW:
  //Solmu4:stä tehdään WiFi-asema:
  WiFi.mode(WIFI_STA);

  // Estetään solmu 4:n nukkumaan meneminen
  WiFi.setSleep(false);

  // Luodaan yhteys reitittimeen
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Setting as a Wi-Fi Station..");
  }

  Serial.print("Station IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Wi-Fi Channel: ");
  Serial.println(WiFi.channel());


  //Alustetaan ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  //Vastaanotetaan muilta solmuilta tulevaa sensoridataa:
  esp_now_register_recv_cb(OnDataRecv);
  
  //Käynnistetään kirjasto:
  sensors.begin();

}

void loop(void)
{
  //Tarkistetaan, että muilta solmuilta on vastaanotettu viesti,
  //jotta uudet vastaanotetut tiedot voidaan tallentaa Web-palvelimen tietokantaan:
  if(viestivastaanotettu==true){
    tietojenLahetys();
    // kun viesti on lähetetty, asetetaan viestivastaanotettu arvoon "false"
    viestivastaanotettu=false;
  }
  
  // Solmu 4:n lämpötilan luku, URL:n muodostaminen ja ohjaaminen lähetykseen.

  now = millis();

  // Joissain tapauksissa 30 min on ollut liian pitkä solmulle ja toiminta on häiriintynyt. Lyhennä tarvittessa aikaa esim 60*10*1000.
  if((now - lastTrigger > (60*30*1000))){ 
    lastTrigger = now;
    Serial.print("Requesting temperatures...");
    sensors.requestTemperatures(); 
    webpalvelinURL = webpalvelinURL + "solmu="+ 4 + "&lampotila1="+ sensors.getTempCByIndex(0);
    viestivastaanotettu = true;  
  }
}
