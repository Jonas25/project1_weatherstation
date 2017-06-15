#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10
#define ONE_WIRE_BUS 3

Adafruit_BME280 bme;
OneWire ourWire(ONE_WIRE_BUS);
DallasTemperature sensors(&ourWire);

unsigned long delayTime;

void setup() {
    Serial.begin(9600);
    sensors.begin();
    
    pinMode(13, OUTPUT);
    
    bool status;
    
    status = bme.begin();
    if (!status) {
        Serial.println("error");
        while (1);
    }
    
    delayTime = 10000;
    
    delay(100);
}


void loop() {
  char c;
  printValues();
  c = Serial.read();
  if(c == 49) {
    Serial.println("Received");
  }
  if(c != 49) {
    printValues();
  }
  delay(delayTime);
}

void printValues() {
    sensors.requestTemperatures();
    String ext_temp = String(sensors.getTempCByIndex(0));
    Serial.println("3,"+String(bme.readTemperature())+",4,"+String(bme.readHumidity())+",5,"+String(bme.readPressure() / 100.0F)+",6,"+String(ext_temp));
}
