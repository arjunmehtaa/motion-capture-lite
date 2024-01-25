#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid     = "OnePlus 11";
const char* password = "Arjun123";

const char* host = "192.168.75.154";
WiFiUDP Udp;
unsigned int localUdpPort = 4210;  // local port to listen on
unsigned int portToSend = 5000;
char incomingPacket[255];  // buffer for incoming packets
char  replyPacket[] = "Hello from Arduino 1!";  // a reply string to send back


void setup() {
  Serial.begin(19200);
  delay(100);
  pinMode(0, OUTPUT);
  // turn LED OFF by default
  digitalWrite(0, HIGH);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  IPAddress local_ip(192, 168, 75, 11);
  IPAddress gateway(192, 168, 75, 77);
  IPAddress subnet(255, 255, 255, 0);
  WiFi.config(local_ip, gateway, subnet);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  // turn LED ON when WiFi is connected
  digitalWrite(0, LOW);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  uint16 ab = Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d, %d\n", WiFi.localIP().toString().c_str(), localUdpPort, ab);
}

int value = 0;

void loop() {
  ++value;
  int packetSize = Udp.parsePacket();

  if (packetSize)
  {
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);

    Serial.printf("Remote IP: %d, Remote Port: %d\n", Udp.remoteIP(), Udp.remotePort());

    // send back a reply, to the IP address and port we got the packet from
    Udp.beginPacket(Udp.remoteIP(), portToSend);
    Udp.write(replyPacket);
    Udp.endPacket();
  }

  if (WiFi.status() != WL_CONNECTED) {
    // turn LED OFF if WiFi is disconnected
    digitalWrite(0, HIGH);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    // turn LED ON when WiFi restores
    digitalWrite(0, LOW);
  }
}