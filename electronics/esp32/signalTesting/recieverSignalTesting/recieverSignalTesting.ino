#include <esp_now.h>
#include <WiFi.h>

// reciever
// code from+more details at https://randomnerdtutorials.com/esp-now-esp32-arduino-ide/

double expectedRate = 1.0; // Hz, expects 1 packet per second
unsigned long totalMissed = 0;
double timeOfLastPacket = 0;

// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
    unsigned long packetNum;
} struct_message;

// Create a struct_message called myData
struct_message myData;

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Packet Number: ");
  Serial.println(myData.packetNum);
  
  unsigned long currentTime = millis();
  boolean recievedPacket = true;

  double elapsedTime = currentTime-timeOfLastPacket;

  if (elapsedTime > (1000/expectedRate*1.1)) {
    totalMissed += round(int(round(elapsedTime/1000))%int(round(1000/expectedRate/1000)));
  }

  Serial.print("Time since last packet:  ");
  Serial.println(elapsedTime);
  Serial.print("Total packets missed:  ");
  Serial.println(totalMissed);
  Serial.println("");

  timeOfLastPacket = currentTime;

}
 
void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  Serial.println("recieving");
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);
}
 
void loop() {

}
