#include <Arduino.h>

// Include necessary libraries for the DS18B20 temperature sensor
#include <OneWire.h>
#include <DallasTemperature.h>

/*
 * This Arduino sketch reads data from an AC Voltage Sensor,
 * an AC Current Sensor, and a DS18B20 Temperature Sensor.
 * It then formats the data into a comma-separated string and
 * sends it over the serial port for a Python script to read.
 */

// Define the analog pins for the voltage and current sensors
const int voltageSensorPin = A0;
const int currentSensorPin = A1;

// Define the digital pin for the DS18B20 temperature sensor
const int temperatureSensorPin = 2;

// Setup a one-wire bus for the DS18B20 sensor
OneWire oneWireBus(temperatureSensorPin);

// Pass our one-wire bus reference to the Dallas Temperature sensor library
DallasTemperature sensors(&oneWireBus);

void setup() {
  // Begin serial communication at a baud rate of 9600.
  // The Python script must be configured to use the same baud rate.
  Serial.begin(9600);

  // Start the DS18B20 temperature sensor
  sensors.begin();
}

void loop() {
  // =========================================================================
  // 1. READ SENSOR DATA
  // =========================================================================

  // Read voltage sensor (returns a 0-1023 value from the ADC)
  // Note: The conversion factor here is a placeholder. You will need to calibrate
  // your specific sensor to get an accurate voltage reading.
  int voltageSensorValue = analogRead(voltageSensorPin);
  float voltage = map(voltageSensorValue, 0, 1023, 0, 250); // Map to a reasonable voltage range (e.g., 0-250V)

  // Read current sensor (returns a 0-1023 value from the ADC)
  // Similar to voltage, this is a placeholder. Calibration is crucial.
  int currentSensorValue = analogRead(currentSensorPin);
  float current = map(currentSensorValue, 0, 1023, 0, 100); // Map to a reasonable current range (e.g., 0-100A)

  // Request temperature readings from the DS18B20 sensor
  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0); // Get the temperature of the first device on the bus

  // =========================================================================
  // 2. FORMAT AND SEND DATA
  // =========================================================================

  // Print the formatted string to the serial monitor.
  // The format is "Key:Value,Key:Value,..." which is easy for the Python script to parse.
  Serial.print("Voltage:");
  Serial.print(voltage);
  Serial.print(",Current:");
  Serial.print(current);
  Serial.print(",Temperature:");
  Serial.println(temperature);

  // Wait for 1 second before taking the next reading.
  // This can be adjusted to change the sampling rate.
  delay(1000);
}
