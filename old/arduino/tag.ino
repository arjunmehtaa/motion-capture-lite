/* Assign pins */
const int ANALOG_PIN = A0;
const int LOCATION_GPIO = 12;  // TODO: swapped for testing
const int ORIENTATION_GPIO = 14;

/* Define tuneable parameters */
const int messageLength = 3;
const int minVoltage = 18;
const int maxVoltage = 500;
const int voltageMargin = 0;
const unsigned long timePeriod = 5000;
const unsigned long timeMargin = 200;
const unsigned long transitionDelay = 2000;
const bool isOrientationEnabled = false;

/* Declare time markers */
unsigned long observationStartTime;
unsigned long periodStartTime;
unsigned long transitionDelayStartTime;
unsigned long nonReadingStartTime;
unsigned long delayPeriod;
unsigned long currentTime;

/* Additional variables */
int i;
int inputVoltage;
int numTransitionDelays = isOrientationEnabled ? 2 : 1;
int totalObservationTime = (messageLength * timePeriod) + (numTransitionDelays * transitionDelay);
int message[messageLength];
int minThreshold = minVoltage - voltageMargin;
int maxThreshold = maxVoltage + voltageMargin;
bool startReading = false;
bool interruptTrigger = false;
bool transitionDelayInProgress = false;

void IRAM_ATTR ISR() {
  interruptTrigger = true;
}

void setup() {
  Serial.begin(9600);
  pinMode(0, OUTPUT);
  pinMode(LOCATION_GPIO, OUTPUT);
  memset(message, 0, sizeof(message));
  attachInterrupt(digitalPinToInterrupt(15), ISR, HIGH);
  if(isOrientationEnabled) {
    pinMode(ORIENTATION_GPIO, OUTPUT);
  }
}

void loop() {

  /* Update current time */
  currentTime = millis();

  /* Check if interrupt received */
  if (interruptTrigger) {
    handleSyncInterrupt();
  }

  /* Check if transition delay is in progress */
  if (transitionDelayInProgress) {
    /* Check if transition delay has ended */    
    if ((currentTime - transitionDelayStartTime) >= transitionDelay) {
      handleTransitionDelayFinished();
    }
  }

  if(startReading) {

    /* Check if Reading window has started  */
    if ((currentTime - nonReadingStartTime) >= delayPeriod) {
      readInputValue();
    }

    /* Check if Reading window has ended */
    if((currentTime - nonReadingStartTime) >= (delayPeriod + (2 * timeMargin))) {
      nonReadingStartTime = currentTime;
      /* Update delayPeriod after first iteration */
      if(i == 0) {
        delayPeriod = 2 * ((timePeriod / 2) - timeMargin);
      }
    }

    /* Check if time period has ended */
    if((currentTime - periodStartTime) >= timePeriod) { 
      handleTimePeriodFinished();
    }

    /* Check if observation phase is over */
    if((currentTime - observationStartTime) >= totalObservationTime) {
      sendMessage();
    }
  }
}

void handleSyncInterrupt() {
  Serial.println("Received interrupt.");
  Serial.println("Starting 1st transition.");
  transitionDelayInProgress = true;
  transitionDelayStartTime = currentTime;
  observationStartTime = currentTime;
  delayPeriod = (timePeriod / 2) - timeMargin;
  startReading = false;
  i = 0;
  digitalWrite(LOCATION_GPIO, HIGH);
  interruptTrigger = false;
  if(isOrientationEnabled){
    digitalWrite(ORIENTATION_GPIO, LOW);
  }
}

void handleTransitionDelayFinished() {
  Serial.println("Ending transition delay.");
  periodStartTime = currentTime;
  nonReadingStartTime = currentTime;
  transitionDelayInProgress = false;
  startReading = true;
}

void handleTimePeriodFinished() {
  Serial.println("Time period ended.");
  periodStartTime = currentTime;
  i += 1;
  if (isOrientationEnabled && i == messageLength - 1) {
    Serial.println("Starting 2nd transition delay.");
    transitionDelayStartTime = currentTime;
    transitionDelayInProgress = true;
    startReading = false;
    digitalWrite(LOCATION_GPIO, LOW);
    digitalWrite(ORIENTATION_GPIO, HIGH);
  }
}

void readInputValue() {
  inputVoltage = analogRead(ANALOG_PIN);
  int numLocationLEDs = isOrientationEnabled ? messageLength - 1 : messageLength;
  /* Read location */
  if (i < numLocationLEDs) { 
    if (message[i] != 1 && (inputVoltage > minThreshold) && (inputVoltage < maxThreshold)) {
      message[i] = 1;
      Serial.println(inputVoltage);
    }
  /* Read orientation */
  } else if (isOrientationEnabled && i == messageLength - 1) {
    if (message[i] == 0) { // TODO: Orientation is being read at initial start time
      message[i] = inputVoltage;
    }
  }
}

void sendMessage() {
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
  /* Reset message array */
  memset(message, 0, sizeof(message));
}
