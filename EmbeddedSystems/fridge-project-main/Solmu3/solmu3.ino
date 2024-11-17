#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <Arduino.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>
// Lisää tämä tiedosto samaan kansioon solmu3.inon kanssa
#include "secrets.h"

// Määrittelyt laitteen nukkumisajalle
#define uS_TO_S_FACTOR 1000000
#define TIME_TO_SLEEP 1800

// vastaanottajan (solmu 4) MAC-osoite
uint8_t broadcastAddress[]={0xC0,0x49,0xEF,0x08,0xD4,0xF8};

// Määritellään lähetettävän viestin rakenne
typedef struct struct_message{
  int id;
  float temp;
  int valo;
} struct_message;

// Määritellään valosensorin pinni
const int phototransistorPin = 33;

// Määritellään ssid, tämän pitää löytyä secrets.h tiedostosta
constexpr char WIFI_SSID[] = SECRET_SSID;

// Funktio, jonka avulla dynaamisesti selvitetään oikea kanava lähettäjän ja vastaanottajan viestienvaihtoon (SOLMU 3--> SOLMU 4)
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
}

// Asetetaan Board ID (ESP32 Sender #1 = BOARD_ID 1, ESP32 Sender #2 = BOARD_ID 2, etc)
#define BOARD_ID 3

//Lämpötilasensorin asetuksia:
const int oneWireBus = 4;

// Määritä oneWire-instanssi kommunikoimaan minkä tahansa OneWire-laitteen kanssa (ei vain Maximin/Dallasin lämpötilapiirien kanssa)
OneWire oneWire(oneWireBus);

// Välitä meidän oneWire-viittaus Dallasin lämpötilaan.
DallasTemperature sensors(&oneWire);

//SETUP:
void setup(void)
{
  // Alustetaan Serial
  Serial.begin(115200);
  Serial.println("Setup started");

  //ESP-YHDISTÄMINEN:
  WiFi.mode(WIFI_STA);
  int32_t channel = getWiFiChannel(WIFI_SSID);
  esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);

  // Alustetaan ESP-NOW:
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }


  // Kun ESP NOW on alustettu onnistuneesti, rekisteröidään takaisinkutsufunktio, 
  // jotta saadaan tieto lähetyksen onnistumisesta
  esp_now_register_send_cb(OnDataSent);

  // Rekisteröidään sensoriverkon jäsen (solmu 4)
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0; // Huom, kanava jota kautta saadaan tieto lähetyksen onnistumisesta on eri kanava kuin se jota kautta mittaukset lähetetään
  peerInfo.encrypt = false;

  // Lisätään sensoriverkon jäsen        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  // Käynnistetään kirjastot lämpötilasensoreille
  sensors.begin();
  
  // Lähetetään tiedot...
  lahetaTiedot();
  delay(1000);

  // ...jonka jälkeen asetetaan nukkuma-aika ja laitetaan laite lepotilaan.
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  esp_deep_sleep_start();
}

void loop(void)
{
}

// Funktio tietojen keräämistä ja lähettämistä varten.
void lahetaTiedot(){
    
  int lightIntensity = analogRead(phototransistorPin);
  Serial.println(lightIntensity);

  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  Serial.print(temperatureC);

  // Määritellään viesti
  struct_message myData;
  // Asetetaan luetut tiedot viestiin
  myData.id = BOARD_ID;
  myData.temp = temperatureC;
  myData.valo = lightIntensity;
  
  //Lähetetään viesti ESP-NOW:n avulla
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(struct_message));
  if (result == ESP_OK) {
    Serial.println("Sent with success");
    float arvotesti=myData.temp;
    Serial.println(arvotesti);
  }
  else {
    Serial.println("Error sending the data");
  }
}
