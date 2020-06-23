#include <DHT.h>

#define SERIAL_BAUD_RATE 115200

#define DHTPIN 4          // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);

  dht.begin();
}

void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readString();

    if (command == "temperature") {
      processTemperature();
    } else if (command == "humidity") {
      processHumidity();
    } else {
      Serial.println("Command " + command + " not supported");
    }
  }

}

void processTemperature() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  if (isnan(t)) {
    Serial.println("Error read temperature");
    return;
  }

  Serial.print(t);
  Serial.println("C");
}

void processHumidity() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();

  if (isnan(h)) {
    Serial.println("Error read humidity");
    return;
  }

  Serial.print(h);
  Serial.println("%");
}
