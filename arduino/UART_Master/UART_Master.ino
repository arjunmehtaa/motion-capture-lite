
// // create an array of integers
int numbers[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

int message[5] = {1, 2, 3, 4, 5};

int i;

void setup() {
  Serial.begin(9600);
  pinMode(0, OUTPUT);
  // randomSeed(40);
  i = 0;
}

int generateRandomNumber() {
  i = (i + 1) % 10;
  return numbers[i];
  // return random(0, 100);
}

void loop() {
  // 0
  Serial.println("v");

  delay(40000);

  // digitalWrite(0, HIGH);
  // delay(750);
  // digitalWrite(0, LOW);
  // delay(750);
}