const int enableInPin = 12;
const int enableOutPin = 2;
const int ledOutPins[] = {12, 13, 15, 0, 16};

const int ledActiveTimePeriod = 1000;
const int transitionDelayTimePeriod = 200;

const int numLeds = sizeof(ledOutPins);
const int numTransitionDelays = 2; // Assuming we delay once after enable input and once after all location LEDs are done projecting
const int totalMeasurementTime = (numLeds * ledActiveTimePeriod) + (numTransitionDelays * transitionDelayTimePeriod);
bool startReading = false;

void setup() {
  pinMode(enableInPin, INPUT);
  pinMode(enableOutPin, OUTPUT);
  for(int i  = 0; i < numLeds; i++) {
    pinMode(ledOutPins[i], OUTPUT);
  }
}

void loop() {
  unsigned long measurementStartTime;
  unsigned long ledStartTime;
  int i;
  if(digitalRead(enableInPin) == HIGH) {
    delay(transitionDelayTimePeriod);
    startReading = true;
    measurementStartTime = millis();
    ledStartTime = millis();
    i = 0;
    digitalWrite(ledOutPins[i], HIGH);
  }
  if(startReading) {
    unsigned long currentMillis = millis();
    if((currentMillis - ledStartTime) >= ledActiveTimePeriod) {
      digitalWrite(ledOutPins[i], LOW);
      if(i == numLeds - 2) {
        delay(transitionDelayTimePeriod);
      }
      i += 1;
      if(i < numLeds) {
        digitalWrite(ledOutPins[i], HIGH);
      }
      ledStartTime = currentMillis;
    }
    if((currentMillis - measurementStartTime) >= (totalMeasurementTime)) {
      startReading = false;
      digitalWrite(enableOutPin, HIGH);
    }
  }
}
