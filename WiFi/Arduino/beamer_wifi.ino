#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

/* Assign pins */
const int ANALOG_PIN = A0;

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
unsigned long startTime;
unsigned long currentTime;
bool startReading = false;
int inputVoltage;

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
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  // turn LED OFF when WiFi is connected
  digitalWrite(0, HIGH);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  uint16 ab = Udp.begin(portToListen);
  Serial.printf("Now listening at IP %s, UDP port %d, %d\n", WiFi.localIP().toString().c_str(), portToListen, ab);
}

int value = -1;

void loop() {
  currentTime = millis();
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    // receive incoming UDP packets
    value += 1;
    // Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    startReading = true;
    startTime = currentTime;
    int len = Udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket[0].toInt());
  }
  if(startReading) {
    inputVoltage = max(inputVoltage, analogRead(ANALOG_PIN)); 
    if (currentTime - startTime >= timeWindow) {
      startReading = false;
      sprintf(replyPacket, "%d", value);
      Udp.beginPacket(Udp.remoteIP(), portToSend);
      Udp.write(replyPacket);
      Udp.endPacket();
    }
  }
}