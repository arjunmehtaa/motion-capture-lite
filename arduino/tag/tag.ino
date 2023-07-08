const int synchronizationInPin = 14;
const int analogInPin = 12;

const int timePeriod = 1000;
const int minVoltage = 512;
const int maxVoltage = 1023;
const int timeMargin = 100;
const int voltageMargin = 100;
const int messageLength = 5;

int inputVoltage = 0;
int minThreshold = minVoltage - voltageMargin;
int maxThreshold = maxVoltage + voltageMargin;
int message[messageLength];

bool startReading = false;

void setup() {
  pinMode(synchronizationInPin, INPUT);
  pinMode(analogInPin, INPUT);
  memset(message, 0, sizeof(message)); // to ensure we initialize the values in message
}

/*
Assuming readings are taken over entire time periods
LED1 from 0 to T1, 
LED2 from T1 to T2, and so on...
*/
void loop() {
  unsigned long messageStartTime;
  unsigned long periodStartTime;
  int i;
  if(digitalRead(synchronizationInPin) == HIGH) {
    // maybe this will get triggered multiple times, won't suggest a change rn but maybe it might be nice to have a positive edge-triggered interrupt for synchronizationInPin
    // https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/ 
    startReading = true;
    messageStartTime = millis();
    periodStartTime = millis();
    i = 0;
    Serial.println("synchronize");

  }
  if(startReading) {
    unsigned long currentMillis = millis();
    if(message[i] != 1) {
      inputVoltage = analogRead(analogInPin);
      // do we care if it's below a max threshold?
      if ((inputVoltage > minThreshold) && (inputVoltage < maxThreshold)) {
        message[i] = 1;
      }
    }
    if((currentMillis - periodStartTime) >= timePeriod) {
      // I am unsure about this because it seems like we may end up with skew on the period. I feel that an interrupt might be the best choice, especially as we increase speed
      // maybe not rn, but i'm just flagging this in case we ever end up having problems around this
      periodStartTime = currentMillis;
      i += 1;
    }
    if((currentMillis - messageStartTime) >= (messageLength * timePeriod)) {
      startReading = false;
      // should we reset the message here?
      // memset(message, 0, sizeof(message));
      // Serial.println(message);
    }
  }
}

/* 
Assuming we take readings once every T/2 seconds
LED1 at T/2
LED2 at T + T/2, and so on...
*/
void loop2() {
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
      // Serial.println(message);
    }
  }
}

/* 
Assuming we take readings from (T/2 - timeMargin) to (T/2 + timeMargin)
LED1 from (T/2 - timeMargin) to (T/2 + timeMargin)
LED2 from ((T + T/2) - timeMargin) to ((T + T/2) + timeMargin), and so on...
*/
void loop3() {
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
      // Serial.println(message);
    }
  }
}
