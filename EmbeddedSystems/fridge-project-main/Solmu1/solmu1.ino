#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <OneWire.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <Arduino.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>
// Lisää tämä tiedosto samaan kansioon solmu1.inon kanssa
#include "secrets.h"

// Asetetaan Board ID (ESP32 Sender #1 = BOARD_ID 1, ESP32 Sender #2 = BOARD_ID 2, etc)
#define BOARD_ID 1

// Määritellään ssid, tämän pitää löytyä secrets.h tiedostosta
constexpr char WIFI_SSID[] = SECRET_SSID;

// vastaanottajan (solmu 4) MAC-osoite
uint8_t broadcastAddress[]={0xC0, 0x49, 0xEF, 0x08, 0xD4, 0xF8};

// Määritellään ajastimen asetuksia
long now = millis();
long lastTrigger = 0;
boolean startTimer = false;

// BME sensorin määrittelyt
#define BME_SDI 21
#define BME_SCK 22
#define SEALEVELPRESSURE_HPA (1013.25)
Adafruit_BME280 bme; // I2C

// Valosensorin määrittely
const int phototransistorPin = 33;

// Ovisensorin määrittely
#define DOOR_SENSOR_PIN  32

// Muuttuja, johon tallennetaan oven sen hetkinen tilanne
int currentDoorState; 

// Määritellään Solmu 1 viesti joka lähetetään solmu 4:lle
typedef struct struct_message{
  int id;
  float temp;
  int kosteus;
  int ilmanpaine;
  int valo;
  int ovi;
} struct_message;


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

// Keskeytysfunktio ovisensorille
void IRAM_ATTR ISR() {

  if(startTimer == false){
    startTimer = true;
    lastTrigger = millis();
  }

}

// Datan lähetyksen yhteydessä tapahtuva takaisinkutsufunktio --> lähettänyt solmu saa vastaaanottavalta
// solmulta takaisin tiedon onko lähetys onnistunut vai ei.
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
  if(status == true){
   // lahetaTiedot();
  }
}

//SETUP:
void setup(void)
{
  // Alustetaan Serial
  Serial.begin(115200);

  // Odotetaan, että Serial pyörii kuten pitää
  while(!Serial);    

  // Alustetaan BME-sensorin asetukset
  Serial.println(F("BME280 test"));
  Serial.println("Setup started");
  unsigned sta;
  sta = bme.begin(); 

  if (!sta) {
        Serial.println("Could not find a valid BME280 sensor, check wiring, address, sensor ID!");
        Serial.print("SensorID was: 0x"); Serial.println(bme.sensorID(),16);
        Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
        Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
        Serial.print("        ID of 0x60 represents a BME 280.\n");
        Serial.print("        ID of 0x61 represents a BME 680.\n");
        while (1) delay(10);
    }
    
  Serial.println("-- Default Test --");
  Serial.println();

  //ESP-YHDISTÄMINEN:
  WiFi.mode(WIFI_STA);

  // Haetaan kanava, jota käytetään viestien välittämiseen
  int32_t channel = getWiFiChannel(WIFI_SSID);
  
  // Asetetaan tämä kanava
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

  // Setup ovisensorille
  pinMode(DOOR_SENSOR_PIN, INPUT_PULLUP);

  // Lisätään ovisensorille keskeytys
  attachInterrupt(32, ISR, CHANGE);
  Serial.println("Setup done");
  lahetaTiedot();
}

int onkoLahetetty = 0;
void loop(void){

  // Otetaan sen hetkinen aika talteen
  now = millis();

  // Jos startTimer on true ja aikaa on kulunut ajastimen verran (100ms)
  // siirrytään if-lauseeseen
  if(startTimer && (now - lastTrigger > (100))) {
    
    // otetaan viimeisin keskeytysaika talteen
    lastTrigger = now;

    // Luetaan oven tila muuttujaan
    currentDoorState = digitalRead(DOOR_SENSOR_PIN);  

    if (currentDoorState == HIGH) { //tila vaihtunut: LOW -> HIGH
      Serial.println("OVI ON AUKI");
      if(onkoLahetetty == 0){
        lahetaTiedot();
        onkoLahetetty = 1;
      }
    } else if (currentDoorState == LOW) { // tila vaihtunut: HIGH -> LOW
      Serial.println("OVI ON KIINNI");
      startTimer = false;
      onkoLahetetty = 0;
    }
  }

  // Otetaan sen hetkinen aika talteen ja lähetetään tiedot 30 min välein  
  now = millis();

  if(now - lastTrigger > (60*30*1000)) {
    lastTrigger = now;
    lahetaTiedot();    
  }
}

// Funktio tietojen lähettämistä varten
void lahetaTiedot(){
 
  // Otetaan oven tila talteen
  currentDoorState = digitalRead(DOOR_SENSOR_PIN);

  // Määritellään viesti ja asetetaan tiedot muuttujiin
  struct_message myData;

  if (currentDoorState == HIGH) { // tila muuttunut: LOW -> HIGH
    Serial.println("OVI ON AUKI");
    myData.ovi = 1;

  } else if (currentDoorState == LOW) { // tila muuttunut: HIGH -> LOW
    Serial.println("OVI ON KIINNI");
    myData.ovi = 0;
  }

  int valoisuus = analogRead(phototransistorPin);  
  myData.id = BOARD_ID;
  myData.temp = bme.readTemperature();
  myData.ilmanpaine = bme.readPressure() / 100.0F;
  myData.kosteus = bme.readHumidity();
  myData.valo= valoisuus;
  
  Serial.println(myData.temp);
  Serial.println(myData.ilmanpaine);
  Serial.println(myData.kosteus);
  Serial.println(myData.valo);

  // Lähetetään viesti ESP-NOW:n avulla
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(struct_message));
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  } else {
    Serial.println("Error sending the data");
  }
}
