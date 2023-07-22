// const int synchronizationInPin = 14; for testing, using UART
// const int analogInPin = 12; for testing, using UART

const int ANALOG_PIN = A0;
const int LOCATION_GPIO = 12;  // TODO: swapped for testing
const int ORIENTATION_GPIO = 14;

const unsigned long timePeriod = 5000;
const int minVoltage = 100;
const int maxVoltage = 500;
const int voltageMargin = 0;
const unsigned long messageLength = 5;

const unsigned long transitionDelay = 5000;

unsigned long delayPeriod;
const unsigned long timeMargin = 1000;

unsigned long messageStartTime;
unsigned long periodStartTime;
unsigned long transitionStartTime;
unsigned long nonReadingStartTime; // ~ previousMillis in loop3

int i;


int inputVoltage = 0;
int minThreshold = minVoltage - voltageMargin;
int maxThreshold = maxVoltage + voltageMargin;
int message[messageLength];

bool startReading = false;
bool startTransitionDelay = false;

void setup() {
  // pinMode(synchronizationInPin, INPUT);
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  memset(message, 0, sizeof(message)); // to ensure we initialize the values in message

  pinMode(LOCATION_GPIO, OUTPUT); // Set the pin as an OUTPUT
  pinMode(ORIENTATION_GPIO, OUTPUT); // Set the pin as an OUTPUT
}


/*
Taking readings from (T/2 - timeMargin) to (T/2 + timeMargin)
LED1 from (T/2 - timeMargin) to (T/2 + timeMargin)
LED2 from ((T + T/2) - timeMargin) to ((T + T/2) + timeMargin), and so on...
*/
void loop() {
  unsigned long currentTime = millis();

  // SYNC SIGNAL (SHOULD BE INTERRUPT)
  if (!startReading && !startTransitionDelay) { // && Serial.available() > 0
    // char sync_inp = Serial.read();

    if(true) { // SYNC SIGNAL
      // Serial.println("SYNC");
      Serial.println("STARTING 1st TRANSITION");
      startTransitionDelay = true;
      transitionStartTime = currentTime;
      messageStartTime = currentTime;

      delayPeriod = (timePeriod / 2) - timeMargin;

      i = 0;

      digitalWrite(LOCATION_GPIO, HIGH);
      digitalWrite(ORIENTATION_GPIO, LOW);
    }
  }

  if(startTransitionDelay) {    
    // END TRANSITION TIME
    if ((currentTime - transitionStartTime) >= transitionDelay) {
      Serial.println("ENDING TRANSITION");
      startReading = true;
      periodStartTime = currentTime;
      nonReadingStartTime = currentTime;
      startTransitionDelay = false;
    }
    
  }

  if(startReading) {
    if ((currentTime - nonReadingStartTime) >= delayPeriod) {
      inputVoltage = analogRead(ANALOG_PIN);
      if (i < messageLength - 1) { // READING LOCATION
        Serial.print("V:");
        Serial.println(inputVoltage);
        if (message[i] != 1 && (inputVoltage > minThreshold) && (inputVoltage < maxThreshold)) {
          message[i] = 1;
          Serial.println(inputVoltage);
          // Serial.println(i);
        }
      } else if (i == messageLength - 1) { // READING ORIENTATION
        if (message[i] == 0) { // TODO: Orientation is being read at initial start time
          message[i] = inputVoltage;
        }
      }
    } 

    if((currentTime - nonReadingStartTime) >= (delayPeriod + (2 * timeMargin))) {
      Serial.println("BEGINNING OF NON-READING");
      nonReadingStartTime = currentTime;
      if(i == 0) {
        delayPeriod = 2 * ((timePeriod / 2) - timeMargin);
      }
    }

    if((currentTime - periodStartTime) >= timePeriod) { 
      // Serial.print("period:");
      // Serial.println(currentTime);
      periodStartTime = currentTime;
      i += 1;

      Serial.println("ENDING TIME PERIOD");
      if (i == messageLength - 1) {
        // STARTING SECOND TRANSITION DELAY (AFTER LOCATION)
        Serial.println("STARTING 2nd TRANSITION");
        startTransitionDelay = true;
        startReading = false;
        transitionStartTime = currentTime;

        digitalWrite(LOCATION_GPIO, LOW);
        digitalWrite(ORIENTATION_GPIO, HIGH);
      }
    }

    // MESSAGE PASSING
    if((currentTime - messageStartTime) >= ((messageLength * timePeriod) + (2 * transitionDelay))) {
      if (i >= messageLength) {
        startReading = false;
        for (int k = 0; k < messageLength; k++) {

          if (k < messageLength - 1) {
            char c;
            if (message[k] == 0) {
              c = '0';
            }
            if (message[k] == 1) {
              c = '1';
            } 
            Serial.print(c);
          } else {
            Serial.print(message[k]);
          }
          
        }
        Serial.println("x");
      }
      memset(message, 0, sizeof(message)); // reset the message
    }
  }


}