const int enableInPin = 2;
const int enableOutPin = 16;
const int ledOutPins[] = {12, 13, 14};

const int ledActiveTimePeriod = 5000; // match this to timePeriod of TAG
const int transitionDelayTimePeriod = 2000;

const int numLeds = 3;
const int numTransitionDelays = 1; // Assuming we delay once after enable input and once after all location LEDs are done projecting
const int totalMeasurementTime = (numLeds * ledActiveTimePeriod) + (numTransitionDelays * transitionDelayTimePeriod);
bool startReading = false;

#define KEEP_LED_ON -1 // -1 for normal runtime, 0, 1. 2 for LED 0, 1, 2

void setup() {
  Serial.begin(9600);
  // pinMode(enableInPin, INPUT);
  // pinMode(enableOutPin, OUTPUT);
  for(int i  = 0; i < numLeds; i++) {
    pinMode(ledOutPins[i], OUTPUT);
  }

  pinMode(enableOutPin, OUTPUT);
}

unsigned long measurementStartTime;
unsigned long ledStartTime;
int i;

void turnOneLEDOn(int p) {
  if (KEEP_LED_ON >= 0) {
    p = KEEP_LED_ON;
  }

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
  
  if(!startReading) {
    Serial.println("Sending interrupt"); 
    digitalWrite(enableOutPin, HIGH);
    startReading = true;
    delay(transitionDelayTimePeriod);
    
    startReading = true;
    measurementStartTime = millis();
    ledStartTime = millis();
    i = 0;
    turnOneLEDOn(0);
  }

  if(startReading) {
    digitalWrite(enableOutPin, LOW);
    unsigned long currentMillis = millis();
    if((currentMillis - ledStartTime) >= ledActiveTimePeriod) {
      // digitalWrite(ledOutPins[i], LOW);
      i += 1;
      // if(i == numLeds - 1) {
      //   delay(transitionDelayTimePeriod);
      // }
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
