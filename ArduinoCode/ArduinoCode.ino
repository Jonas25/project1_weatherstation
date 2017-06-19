#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <OneWire.h>
#include "Adafruit_SI1145.h"

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

Adafruit_BME280 bme;
Adafruit_SI1145 uv = Adafruit_SI1145();

unsigned long delayTime;
const int sensorPin = A0;
int sensorValue = 0; 
float sensorVoltage = 0;
float windSpeed = 0;

float voltageConversionConstant = .004882814;
int sensorDelay = 1000;

float voltageMin = .4;
float windSpeedMin = 0;

float voltageMax = 2.0;
float windSpeedMax = 32;

void setup() {
    Serial.begin(9600);
    
    pinMode(13, OUTPUT);
    
    bool status;
    
    status = bme.begin();
    if (!status) {
        Serial.println("error");
        while (1);
    }

    if (! uv.begin()) {
    Serial.println("Didn't find Si1145");
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
    sensorValue = analogRead(sensorPin);
    sensorVoltage = sensorValue * voltageConversionConstant;
    if (sensorVoltage <= voltageMin){
      windSpeed = 0;
    }else {
      windSpeed = (sensorVoltage - voltageMin)*windSpeedMax/(voltageMax - voltageMin);
    }
    float UVindex = uv.readUV();
    UVindex /= 100.0;
    Serial.println("3,"+String(bme.readTemperature())+",4,"+String(bme.readHumidity())+",5,"+String(bme.readPressure() / 100.0F)+",7,"+String(windSpeed*3.6)+",8,"+String(UVindex));
}
