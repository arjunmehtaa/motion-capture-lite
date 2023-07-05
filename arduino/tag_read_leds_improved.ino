const int synchronizationInPin = A0;
const int analogInPin = A1;

const int timePeriod = 1000;
const int minVoltage = 512;
const int maxVoltage = 1023;
const int timeMargin = 100;
const int voltageMargin = 100;
const int messageLength = 5;

int inputVoltage = 0;
int minThreshold = 0;
int maxThreshold = 0;
int message[messageLength];

void setup() {
  Serial.begin(9600); 
  minThreshold = minVoltage - voltageMargin;
  maxThreshold = maxVoltage + voltageMargin;
}

/*
Assuming readings are taken over entire time periods
LED1 from 0 to T1, 
LED2 from T1 to T2, and so on...
*/
void loop1() {
  bool startReading = false;
  unsigned long messageStartTime;
  unsigned long periodStartTime;
  int i;
  if(digitalRead(synchronizationInPin) == HIGH) {
    startReading = true;
    messageStartTime = millis();
    periodStartTime = millis();
    i = 0;
  }
  if(startReading) {
    unsigned long currentMillis = millis();
    if(message[i] != 1) {
      inputVoltage = analogRead(analogInPin);
      if ((inputVoltage > minThreshold) && (inputVoltage < maxThreshold)) {
        message[i] = 1;
      }
    }
    if((currentMillis - periodStartTime) >= timePeriod) {
      periodStartTime = currentMillis;
      i += 1;
    }
    if((currentMillis - messageStartTime) >= (messageLength * timePeriod)) {
      startReading = false;
      Serial.println(message);
    }
  }
}

/* 
Assuming we take readings once every T/2 seconds
LED1 at T/2
LED2 at T + T/2, and so on...
*/
void loop2() {
  bool startReading = false;
  unsigned long messageStartTime;
  unsigned long previousMillis;
  unsigned long delayPeriod;
  int i;
  if(digitalRead(synchronizationInPin) == HIGH) {
    startReading = true;
    messageStartTime = millis();
    previousMillis = millis();
    delayPeriod = timePeriod / 2;
    i = 0;
  }
  if(startReading) {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= delayPeriod) {
      previousMillis = currentMillis;
      inputVoltage = analogRead(analogInPin);
      if ((inputVoltage > minThreshold) && (inputVoltage < maxThreshold)) {
        message[i] = 1;
      }
      if(i == 0){
        delayPeriod = timePeriod;
      }
      i += 1;
    }
    if((currentMillis - messageStartTime) >= (messageLength * timePeriod)) {
      startReading = false;
      Serial.println(message);
    }
  }
}

/* 
Assuming we take readings from (T/2 - timeMargin) to (T/2 + timeMargin)
LED1 from (T/2 - timeMargin) to (T/2 + timeMargin)
LED2 from ((T + T/2) - timeMargin) to ((T + T/2) + timeMargin), and so on...
*/
void loop3() {
  bool startReading = false;
  unsigned long messageStartTime;
  unsigned long previousMillis;
  unsigned long delayPeriod;
  int i;
  if(digitalRead(synchronizationInPin) == HIGH) {
    startReading = true;
    messageStartTime = millis();
    previousMillis = millis();
    delayPeriod = (timePeriod / 2) - timeMargin;
    i = 0;
  }
  if(startReading) {
    unsigned long currentMillis = millis();
    if((currentMillis - previousMillis) >= delayPeriod) {
      if(message[i] != 1) {
        inputVoltage = analogRead(analogInPin);
        if ((inputVoltage > minThreshold) && (inputVoltage < maxThreshold)) {
          message[i] = 1;
        }
      }
    }
    if((currentMillis - previousMillis) >= (delayPeriod + (2 * timeMargin))) {
      previousMillis = currentMillis;
      if(i == 0) {
        delayPeriod = 2 * ((timePeriod / 2) - timeMargin);
      }
      i += 1;
    }
    if((currentMillis - messageStartTime) >= (messageLength * timePeriod)) {
      startReading = false;
      Serial.println(message);
    }
  }
}
