#include "WiFi.h"
#include "esp_now.h"

uint8_t broadcastAddress[] = {0x8C, 0xAA, 0xB5, 0x85, 0xE7, 0x90}; // mac adress of reciever

// need to rewrite this to constantly ping the reciever with some ignored info and make sure they are in range and 
// communicating successfully. should work as is but wont know if they are out of range

int stopPin = 13; // LIKELY DIFFERENT ON OTHER BOARDS
int unstopPin = 12;
int errorPin = 2; // i think the onboard led is on gpio 2

unsigned long timeOfLast = 0; // time since last button press, used for debouncing
bool estop = false;

String estopSignal; // data to send 
char otherEstopSignal[10]; // use char array if string doesnt work

esp_now_peer_info_t peerInfo;


void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {
  // Init Serial Monitor
  Serial.begin(115200);
 
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  pinMode(stopPin, INPUT);
  pinMode(unstopPin, INPUT);
}
 
void loop() {
  // Set values to send
  //strcpy(otherEstopSignal, "t/f");

  if ( digitalRead(stopPin) ) {
    unsigned long currentTime = millis();
    if (currentTime - timeOfLast > 200) { // will have to tune this time
        estopSignal = "true";
    }
    sendSignal();
    timeOfLast = currentTime;
  }

  if ( digitalRead(unstopPin) ) {
    unsigned long currentTime = millis();
    if (currentTime - timeOfLast > 200) {
        estopSignal = "false";
    }
    sendSignal();
    timeOfLast = currentTime;
  }
  
  delay(50); // should this be based on interrupts or will that break ESP-Now?
}

// sends the signal. if the signal doesnt make it, led goes on and retries until it makes it
void sendSignal() { 

    esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &estopSignal, sizeof(estopSignal));
    if (result == ESP_OK) {
        digitalWrite(errorPin, LOW);
    } else {
        digitalWrite(errorPin, HIGH);
        while (true) {
            esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &estopSignal, sizeof(estopSignal));
            if (result == ESP_OK) {
                digitalWrite(errorPin, LOW);
                break;
            }
            delay(1000);
        }
        return;
    }
}
