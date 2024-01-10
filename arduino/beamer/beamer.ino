const int interruptIn = 2;
const int interruptOut = 16;
const int ledOutPins[] = {12, 13, 14};

const int ledActiveTimePeriod = 1000; // match this to timePeriod of TAG
const int transitionDelayTimePeriod = 50;

const int numLeds = 3;
const int numTransitionDelays = 1; // Assuming we delay once after enable input and once after all location LEDs are done projecting
const int totalMeasurementTime = (numLeds * ledActiveTimePeriod) + (numTransitionDelays * transitionDelayTimePeriod);
bool startReading = false;

#define KEEP_LED_ON -1

int count;
bool trigger;

void IRAM_ATTR ISR() {
  count++;
  Serial.println(count);
  if (count % 2 == 0) {
    digitalWrite(0, HIGH);
  } else {
    digitalWrite(0, LOW);
  }
  trigger = true;
}

void setup() {
  Serial.begin(9600);

  count = 0;
  trigger = false;
  attachInterrupt(digitalPinToInterrupt(interruptIn), ISR, CHANGE);

  pinMode(interruptOut, OUTPUT);
  pinMode(0, OUTPUT);

  for(int i  = 0; i < numLeds; i++) {
    pinMode(ledOutPins[i], OUTPUT);
  }
}

unsigned long measurementStartTime;
unsigned long ledStartTime;
int i;

void turnOneLEDOn(int p) {
  if (KEEP_LED_ON >= 0) {
    p = KEEP_LED_ON;
  }

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
  
  if(!startReading && trigger) { // digitalRead(enableInPin) == HIGH
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
      trigger = false;
      i = 0;
      turnOneLEDOn(-1); // turn off all LEDs
      if (count % 2 == 0) {
        digitalWrite(interruptOut, HIGH);
      } else {
        digitalWrite(interruptOut, LOW);
      }

    }
  }
}