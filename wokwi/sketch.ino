const int sensorPin = A0;

float adcToVoltage(int adcValue) {
  return adcValue * (5.0 / 1023.0);
}

String classifyVoltage(float voltage) {
  if (voltage >= 4.0) {
    return "FAIL";
  }
  if (voltage >= 3.0) {
    return "WARN";
  }
  return "NORMAL";
}

void setup() {
  Serial.begin(9600);
  delay(1000);
  Serial.println("time_ms,adc_value,voltage,status");
}

void loop() {
  unsigned long timeMs = millis();
  int adcValue = analogRead(sensorPin);
  float voltage = adcToVoltage(adcValue);
  String status = classifyVoltage(voltage);

  Serial.print(timeMs);
  Serial.print(",");
  Serial.print(adcValue);
  Serial.print(",");
  Serial.print(voltage, 3);
  Serial.print(",");
  Serial.println(status);

  delay(1000);
}
