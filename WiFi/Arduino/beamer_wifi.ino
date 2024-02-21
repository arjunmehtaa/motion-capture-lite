#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const int NUM_LEDS = 6;
int LED_GPIOS[NUM_LEDS] = {4, 5, 2, 16, 0, 15};

/* Setup WiFi paramteres */
const char* ssid     = "dlink-A40C";
const char* password = "qybmo02053";
IPAddress local_ip(192, 168, 0, 11);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);

WiFiUDP Udp;
const char* host = "192.168.75.154";
unsigned int portToListen = 4210;  // local port to listen on
// unsigned int portToSend = 5000;
char incomingPacket[255];  // buffer for incoming packets
char replyPacket[20];
unsigned long timeWindow = 5;
unsigned long cycleWindow = 10;
unsigned long startTime;
unsigned long currentTime;
bool startReading = false;

void setup() {
  Serial.begin(19200);
  pinMode(0, OUTPUT);

  // turn LED ON by default
  digitalWrite(0, LOW);

  // We start by connecting to a WiFi network

  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  
  WiFi.config(local_ip, gateway, subnet);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  // turn LED OFF when WiFi is connected
  digitalWrite(0, HIGH);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  uint16 ab = Udp.begin(portToListen);
  // Serial.printf("Now listening at IP %s, UDP port %d, %d\n", WiFi.localIP().toString().c_str(), portToListen, ab);

  int i;
  for (i=0;i<NUM_LEDS;i++){
    pinMode(LED_GPIOS[i], OUTPUT); // Set the pin as an OUTPUT
  }
}

int value = -1;
int ledId = 0;
int cycleCounter = 0;

void loop() {
  currentTime = millis();
  int packetSize = Udp.parsePacket();

  if (packetSize) {
    // received a UDP packet, start light cycle
    value += 1;
    startReading = true;
    startTime = currentTime;
    cycleCounter = 1; // so we go into else if block once cycle time has been reached
    ledId = 0;
    digitalWrite(LED_GPIOS[ledId], HIGH);
  }
  else if (cycleCounter > 0 && (currentTime - startTime) >= cycleWindow) {
    // set next led if cycleWindow millis have passed since last led update
    startReading = true;
    cycleCounter = (cycleCounter+1) % NUM_LEDS;
    startTime = currentTime;
    ledId = (ledId+1) % NUM_LEDS;
    digitalWrite(LED_GPIOS[ledId], HIGH);
  }

  if(startReading) {
    if (currentTime - startTime >= timeWindow) {
      startReading = false;
      digitalWrite(LED_GPIOS[ledId], LOW);
    }
  }
}