/*
Sähköpostin lähetys on tehty mukaillen seuraavaa githubin-pohjaa, ESP32 RandomNerdTutorials-ohjeen mukaisesti:
  Rui Santos
  Complete project details at:
   - ESP32: https://RandomNerdTutorials.com/esp32-send-email-smtp-server-arduino-ide/
   - ESP8266: https://RandomNerdTutorials.com/esp8266-nodemcu-send-email-smtp-server-arduino/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files.
  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
  Example adapted from: https://github.com/mobizt/ESP-Mail-Client
*/


#include <Arduino.h>
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <ESP_Mail_Client.h>
#include "secrets.h"

#define WIFI_SSID SECRET_SSID
#define WIFI_PASSWORD SECRET_PASS

#define SMTP_HOST "smtp.gmail.com"
#define SMTP_PORT 465

/* Viestin lähettäjän kirjautumistiedot: secrets.h-tiedostosta tietojen luku*/
#define AUTHOR_EMAIL SECRET_AUTHOR_EMAIL
#define AUTHOR_PASSWORD SECRET_AUTHOR_PASSWORD

/* Viestin vastaanottajan sähköposti: secrets.h tiedostosta tietojen luku*/
#define RECIPIENT_EMAIL SECRET_CUSTOMER_EMAIL

/* The SMTP Sessioobjekti, jota käytetään sähköpostin lähettämiseen */
SMTPSession smtp;

/* Callback-funktio, sähköpostin lähetysstatuksen vastaanottamiseen*/
void smtpCallback(SMTP_Status status);

void setup(){
  Serial.begin(115200);
  Serial.println();
  Serial.print("Connecting to AP");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(200);
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /** Sallitaan dubug Serial portin välityksellä
   * none debug or 0
   * basic debug or 1
  */
  smtp.debug(1);

  /* Asetetaan callback-funktio, jotta saadaan lähetystulokset*/
  smtp.callback(smtpCallback);

  /* Session tieto*/
  ESP_Mail_Session session;

  /* Määritetään session asetukset:*/
  session.server.host_name = SMTP_HOST;
  session.server.port = SMTP_PORT;
  session.login.email = AUTHOR_EMAIL;
  session.login.password = AUTHOR_PASSWORD;
  session.login.user_domain = "";

  /* Viestiluokka */
  SMTP_Message message;

  /* Viestin luominen: */
  message.sender.name = "ESP lähettäjän nimi";
  message.sender.email = AUTHOR_EMAIL;
  message.subject = "ESP Testi viesti";
  message.addRecipient("Asiakas", RECIPIENT_EMAIL);

  /*HTML viesti*/
  String htmlMsg = "<div style=\"color:#2f4468;\"><h1>Moi Maailma!</h1><p>- Lähetetty ESP32-alustasta</p></div>";
  message.html.content = htmlMsg.c_str();
  message.html.content = htmlMsg.c_str();
  message.text.charSet = "utf-8";
  message.html.transfer_encoding = Content_Transfer_Encoding::enc_7bit;

  /*
  //Voisi myös lähettää: a raw text message:
  String textMsg = "Hello World! - Sent from ESP board";
  message.text.content = textMsg.c_str();
  message.text.charSet = "us-ascii";
  message.text.transfer_encoding = Content_Transfer_Encoding::enc_7bit;
  
  message.priority = esp_mail_smtp_priority::esp_mail_smtp_priority_low;
  message.response.notify = esp_mail_smtp_notify_success | esp_mail_smtp_notify_failure | esp_mail_smtp_notify_delay;*/

  /* Set the custom message header */
  //message.addHeader("Message-ID: <abcde.fghij@gmail.com>");

  /* Yhdistetään sessiolla smtp-serveriin */
  if (!smtp.connect(&session))
    return;

  /* Lähetetään viesti ja suljetaan sessio*/
  if (!MailClient.sendMail(&smtp, &message))
    Serial.println("Error sending Email, ");
    Serial.println(smtp.errorReason());
}

void loop(){

}

/* Callback-funtio sähköpostin lähetysstatuksen saamiseksi*/
void smtpCallback(SMTP_Status status){
  /* Print the current status */
  Serial.println(status.info());

  /* Lähetystulosten tulostus*/
  if (status.success()){
    Serial.println("----------------");
    ESP_MAIL_PRINTF("Message sent success: %d\n", status.completedCount());
    ESP_MAIL_PRINTF("Message sent failled: %d\n", status.failedCount());
    Serial.println("----------------\n");
    struct tm dt;

    for (size_t i = 0; i < smtp.sendingResult.size(); i++){
      SMTP_Result result = smtp.sendingResult.getItem(i);
      time_t ts = (time_t)result.timestamp;
      localtime_r(&ts, &dt);

      ESP_MAIL_PRINTF("Message No: %d\n", i + 1);
      ESP_MAIL_PRINTF("Status: %s\n", result.completed ? "success" : "failed");
      ESP_MAIL_PRINTF("Date/Time: %d/%d/%d %d:%d:%d\n", dt.tm_year + 1900, dt.tm_mon + 1, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec);
      ESP_MAIL_PRINTF("Recipient: %s\n", result.recipients.c_str());
      ESP_MAIL_PRINTF("Subject: %s\n", result.subject.c_str());
    }
    Serial.println("----------------\n");
  }
}