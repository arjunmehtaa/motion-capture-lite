const int enableInPin = 12;
const int enableOutPin = 2;
const int ledOutPins[] = {14, 12, 13, 15};

const int ledActiveTimePeriod = 5000; // match this to timePeriod of TAG
const int transitionDelayTimePeriod = 2000;

const int numLeds = 4;
const int numTransitionDelays = 2; // Assuming we delay once after enable input and once after all location LEDs are done projecting
const int totalMeasurementTime = (numLeds * ledActiveTimePeriod) + (numTransitionDelays * transitionDelayTimePeriod);
bool startReading = false;

void setup() {
  Serial.begin(9600);
  // pinMode(enableInPin, INPUT);
  // pinMode(enableOutPin, OUTPUT);
  for(int i  = 0; i < numLeds; i++) {
    pinMode(ledOutPins[i], OUTPUT);
  }
}

unsigned long measurementStartTime;
unsigned long ledStartTime;
int i;

void turnOneLEDOn(int p) {
  Serial.print("Turn on ");
  Serial.println(p);
  for (int i = 0; i < numLeds; i++) {
    if (i == p) {
      digitalWrite(ledOutPins[i], HIGH);
    } else {
      digitalWrite(ledOutPins[i], LOW);
    }
  }
}

void loop() {
  
  if(!startReading) { // digitalRead(enableInPin) == HIGH
    delay(transitionDelayTimePeriod);
    startReading = true;
    measurementStartTime = millis();
    ledStartTime = millis();
    i = 0;
    turnOneLEDOn(0);
  }
  if(startReading) {
    unsigned long currentMillis = millis();
    if((currentMillis - ledStartTime) >= ledActiveTimePeriod) {
      // digitalWrite(ledOutPins[i], LOW);
      i += 1;
      if(i == numLeds - 1) {
        delay(transitionDelayTimePeriod);
      }
      if(i < numLeds) {
        turnOneLEDOn(i);
      }
      ledStartTime = currentMillis;
    }
    if((currentMillis - measurementStartTime) >= (totalMeasurementTime)) {
      startReading = false;
      i = 0;
      turnOneLEDOn(-1); // turn off all LEDs
    }
  }
}
