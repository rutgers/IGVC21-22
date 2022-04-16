#include <esp_now.h>
#include <WiFi.h>

// reciever
// this esp32 will recieve a string that will contain "true" for triggering the estop or "false" for not.
// using strings instead of booleans because I don't know if the protocol automatically implements CRCs or anything and a string wont suffer from a bit flip.

// STRINGS MIGHT NOT WORK, USE CHAR ARRAY INSTEAD FOR FIXED SIZE


String estopSignal; // needed for the callback function to know what to expect

bool estop = false; // actual state, as controlled by gpio pins
bool prevState = false;

int relayPin = 13; // right above gnd on my board, LIKELY DIFFERENT ON OTHERS
 
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

  pinMode(relayPin, OUTPUT);
}

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&estopSignal, incomingData, sizeof(estopSignal));
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Should the estop be activated?: ");
  Serial.println(estopSignal);

  if (estopSignal == "true") {
      estop = true;
  } else if (estopSignal == "false") {
      estop = false;
  } else {
      Serial.println("Recieved invalid data. Should only recieve \"true\" or \"false\" right now");
  }
}
 
void loop() {
    if (estop == prevState)
        return;

    if (estop == false)
        digitalWrite(relayPin, LOW);

    if (estop == true)
        digitalWrite(relayPin, HIGH);
}

// does the callback function still work when a loop is running?
