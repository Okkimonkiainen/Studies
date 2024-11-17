#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <Arduino.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>
// Lisää tämä tiedosto samaan kansioon solmu2.ino:n kanssa
#include "secrets.h"

// Vastaanottajan (solmu 4) MAC-osoite
uint8_t broadcastAddress[]={0xC0, 0x49, 0xEF, 0x08, 0xD4, 0xF8};

// Määritellään lähetettävän viestin rakenne
typedef struct struct_message{
  int id;
  float temp1;
  float temp2;
  int ovi;
} struct_message;

// ESP32 pin GIOP19 kytketään ovisensorin pinneihin 
#define DOOR_SENSOR_PIN  19  

// Muuttuja, jossa on oven tilanne tiedossa (auki vai kiinni)
int currentDoorState; 

// ESP32 GIOP23 pin Kytketään summeriin 
#define BUZZER_PIN 23 

// Määritellään intervalliaika sensoreiden lukemiseen
long interval = 120 * 1000;

// Määritellään SSID, tämän pitää löytyä secrets.h tiedostosta
constexpr char WIFI_SSID[] = SECRET_SSID;

// Funktio, jonka avulla dynaamisesti selvitetään oikea kanava lähettäjän ja vastaanottajan viestienvaihtoon (SOLMU 2--> SOLMU 4)
int32_t getWiFiChannel(const char *ssid) {
  if (int32_t n = WiFi.scanNetworks()) {
      for (uint8_t i=0; i<n; i++) {
          if (!strcmp(ssid, WiFi.SSID(i).c_str())) {
              Serial.println(WiFi.channel());
              return WiFi.channel(i);
          }
      }
  }
  return 0;
}

// Datan lähetyksen yhteydessä tapahtuva takaisinkutsufunktio --> lähettänyt solmu saa vastaaanottavalta
// solmulta takaisin tiedon onko lähetys onnistunut vai ei.
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
  if(status == true){
    //lahetaTiedot();
  }
}

// Asetetaan Board ID (ESP32 Sender #1 = BOARD_ID 1, ESP32 Sender #2 = BOARD_ID 2, etc)
#define BOARD_ID 2

//Lämpötilasensorin asetuksia:
#define ONE_WIRE_BUS 4

// Määritä oneWire-instanssi kommunikoimaan minkä tahansa OneWire-laitteen kanssa (ei vain Maximin/Dallasin lämpötilapiirien kanssa)
OneWire oneWire(ONE_WIRE_BUS);

// Välitä meidän oneWire-viittaus Dallasin lämpötilaan.
DallasTemperature sensors(&oneWire);

// Tähän otetaan ylös lämpötilasensoreiden määrä
// Tarvitaan silloin kun lämpötilasensoreita käytetään sarjassa
int deviceCount = 0;

// Alustetaan ajastimelle tietoja
long now = millis();
long lastTrigger = 0;
boolean startTimer = false;
int edellinenArvo = 0;

// Keskeytysfunktio ovisensorille
// Jos ovi avataan ja stratTimer on false --> asetetaan startTimer arvoon true ja otetaan oven avaus aika ylös. Näitä
// tietoja käytetään silmukassa 
void IRAM_ATTR ISR() {

  if(startTimer == false){
    startTimer = true;
    lastTrigger = millis();
  }
}

//SETUP:
void setup(void)
{
  // Alustetaan serial
  Serial.begin(115200);
  Serial.println("Setup started");

  // ESP-YHDISTÄMINEN:
  WiFi.mode(WIFI_STA);
  int32_t channel = getWiFiChannel(WIFI_SSID);
  esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);

  // Alustetaan ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Kun ESP NOW on alustettu onnistuneesti, rekisteröidään takaisinkutsufunktio, 
  // jotta saadaan tieto lähetyksen onnistumisesta
  esp_now_register_send_cb(OnDataSent);

  // Rekisteröidään sensoriverkon jäsen
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;  
  
  // Lisätään sensoriverkon jäsen        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  // Käynnistetään kirjastot lämpötilasensoreille
  sensors.begin();
  
  // Setup ovisensorille
  pinMode(DOOR_SENSOR_PIN, INPUT_PULLUP);
  // Asetetaan keskeytysfunktio
  attachInterrupt(19, ISR, CHANGE);
  // Setup summerille
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.print("Locating devices...");
  Serial.print("Found ");
  deviceCount = sensors.getDeviceCount();
  Serial.print(deviceCount, DEC);
  Serial.println(" devices.");
  Serial.println("");
  Serial.println("Setup done!");  
  lahetaTiedot();
}

int onkoLahetetty = 0;
void loop(void){

  // Otetaan sen hetkinen aika ylös
  now = millis();

  // Jos startTimer on true ja aikaa on kulunut yli minuutin verran, mennään if lauseeseen
  if(startTimer && (now - lastTrigger > (60*1000))) { // Ajastin 60 s
    
    currentDoorState = digitalRead(DOOR_SENSOR_PIN); // Tarkistetaan onko ovi vielä auki minuutin kuluttua 
  
    if (currentDoorState == HIGH) { // tila vaihtunut: LOW -> HIGH
      Serial.println("OVI ON AUKI");
      tone(BUZZER_PIN, 262); // Laitetaan summeri päälle
      if(onkoLahetetty == 0) { // Jos tietoja ei ole vielä lähetetty, lähetetään ne
        lahetaTiedot();
        onkoLahetetty = 1; // Laitetaan ylös, että tiedot on lähetetty.
      }
    } else if (currentDoorState == LOW) { // tila vaihtunut: HIGH -> LOW eli ovi onkin laitettu kiinni.
      Serial.println("OVI ON KIINNI");
      noTone(BUZZER_PIN); // Laitetaan summeri pois päältä       
      startTimer = false; // Asetetaan ajastin arvoon false
      onkoLahetetty = 0; // Laitetaan ylös, että tietoja ei ole lähetetty.
    }
  }

  // Otetaan sen hetkinen aika ylös.
  // Jos aikaa on kulunut yli 30min, lähetetään tiedot.
  now = millis();

  if(now - lastTrigger > (60*30*1000)) {
    lastTrigger = now;
    lahetaTiedot();    
  }
}

void lahetaTiedot(){

  // Otetaan oven sen hetkinen tila talteen 
  currentDoorState = digitalRead(DOOR_SENSOR_PIN);
  // Määritellään viesti 
  struct_message myData;

  if (currentDoorState == HIGH) { // tila vaihtunut: LOW -> HIGH
    myData.ovi = 1;
  } else if (currentDoorState == LOW) { // tila vaihtunut: HIGH -> LOW
    myData.ovi = 0;
  }

  // Pyydetään lämpötilasensoreilta tietoja  
  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  float temperatureC2 = sensors.getTempCByIndex(1);
   
  // Asetetaan luetut tiedot viestiin 
  myData.id = BOARD_ID;
  myData.temp1 = temperatureC;
  myData.temp2 = temperatureC2;

  //Lähetetään viesti ESP-NOW:n avulla
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(struct_message));
  if (result == ESP_OK) {
    Serial.println("Delivery Success");
  } else {
    Serial.println("Error sending data");
  }  
}
