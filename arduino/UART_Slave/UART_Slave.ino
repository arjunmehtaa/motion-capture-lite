// const int synchronizationInPin = 14; for testing, using UART
// const int analogInPin = 12; for testing, using UART

const int ANALOG_PIN = A0;

const unsigned long timePeriod = 5000;
const int minVoltage = 100;
const int maxVoltage = 1000;
const int timeMargin = 100;
const int voltageMargin = 0;
const unsigned long messageLength = 5;

int inputVoltage = 0;
int minThreshold = minVoltage - voltageMargin;
int maxThreshold = maxVoltage + voltageMargin;
int message[messageLength];

bool startReading = false;

void setup() {
  // pinMode(synchronizationInPin, INPUT);
  // pinMode(analogInPin, INPUT); // 
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  memset(message, 0, sizeof(message)); // to ensure we initialize the values in message
}

unsigned long messageStartTime;
unsigned long periodStartTime;
int i;

/*
Assuming readings are taken over entire time periods
LED1 from 0 to T1, 
LED2 from T1 to T2, and so on...
*/
void loop() {
  // This moves into the interrupt
  if (!startReading && Serial.available() > 0) {
    char sync_inp = Serial.read();
    if(sync_inp == 'v') { // SYNC SIGNAL
      Serial.println("SYNC");
      startReading = true;
      messageStartTime = millis();
      periodStartTime = millis();
      i = 0;
    }
  }

  if(startReading) {
    unsigned long currentMillis = millis();

    inputVoltage = analogRead(ANALOG_PIN);
    if (message[i] != 1 && (inputVoltage > minThreshold) && (inputVoltage < maxThreshold)) {
      message[i] = 1;
      Serial.println(inputVoltage);
      Serial.println(i);
    }
    
    if((currentMillis - periodStartTime) >= timePeriod) { 
      Serial.print("period:");
      Serial.println(currentMillis);
      periodStartTime = currentMillis;
      i += 1;
    }

    if((currentMillis - messageStartTime) >= (messageLength * timePeriod)) {
      if (i >= messageLength) {
        startReading = false;
        for (int k = 0; k < messageLength; k++) {
          Serial.print(message[k]);
        }
        Serial.println();
        memset(message, 0, sizeof(message));
      }
    }
  }
}