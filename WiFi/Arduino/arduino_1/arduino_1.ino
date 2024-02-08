#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid     = "dlink-A40C";
const char* password = "qybmo02053";

WiFiUDP Udp;
unsigned int localUdpPort = 4210;  // local port to listen on
unsigned int portToSend = 5000;
char incomingPacket[5];  // buffer for incoming packets
char  replyPacket[2] = "1";


void setup() {
  Serial.begin(115200);
  delay(100);
  pinMode(0, OUTPUT);
  // turn LED ON by default
  digitalWrite(0, LOW);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  IPAddress local_ip(192, 168, 0, 11);
  IPAddress gateway(192, 168, 0, 1);
  IPAddress subnet(255, 255, 255, 0);
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
  uint16 ab = Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d, %d\n", WiFi.localIP().toString().c_str(), localUdpPort, ab);
  digitalWrite(0, LOW);
}

int value = 0;

void loop() {
  int packetSize = Udp.parsePacket();
  if (value >= 100) {
    digitalWrite(0, HIGH);
  }

  if (packetSize)
  {
    // receive incoming UDP packets

    // Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 5);
    if (len > 0)
    {
      incomingPacket[len] = 0;
      value+=1;
    }
    // Serial.printf("UDP packet contents: %s\n", incomingPacket);
    // sprintf(replyPacket, "UDP packet contents: %s\n", incomingPacket);  // a reply string to send back
    // strcat(replyPacket, incomingPacket);
    // char newLine[] = "\n";
    // strcat(replyPacket, newLine);

    // Serial.printf("Remote IP: %d, Remote Port: %d\n", Udp.remoteIP(), Udp.remotePort());

    // send back a reply, to the IP address and port we got the packet from
    // Udp.beginPacket(Udp.remoteIP(), portToSend);
    // Udp.write(replyPacket);
    // Udp.endPacket();
    // digitalWrite(0, HIGH);
  }

  // if (WiFi.status() != WL_CONNECTED) {
  //   // turn LED ON if WiFi is disconnected
  //   digitalWrite(0, LOW);
  //   while (WiFi.status() != WL_CONNECTED) {
  //     delay(500);
  //     Serial.print(".");
  //   }
  //   // turn LED OFF when WiFi restores
  //   digitalWrite(0, HIGH);
  // }
}