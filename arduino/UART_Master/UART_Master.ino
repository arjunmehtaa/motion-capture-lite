
char message[5];

int i;

void setup() {
  Serial.begin(9600);
  pinMode(0, OUTPUT);
  // randomSeed(40);
  memset(message, 'x', sizeof(message)); // to ensure we initialize the values in message
  i = 0;
}

void loop() {
  // 0
  Serial.println("v");

  // delay(500*5 + 250);

  int k = 0;
  while(true) {
    if(Serial.available() > 0) {
      char sync_inp = Serial.read();
      if (sync_inp == 'x') {
        break;
      }
      // Serial.print(sync_inp);
      message[k] = sync_inp;
      k++;
    }

  }
  Serial.print("exit");
  Serial.print(message);


  // digitalWrite(0, HIGH);
  // delay(750);
  // digitalWrite(0, LOW);
  // delay(750);
}