#include <arduino-timer.h>

// state 1 is on 
// state 2 is autonomous
// state 3 is e-stopped

// may need to do sudo chmod a+rw /dev/ttyACM0 to get it to write

int led_pin = 12; // connect this to mosfet
int flash_freq = 5; // Hz

auto timer = timer_create_default();
bool led = true;
int state = 1;

bool check_should_toggle(void *) {
  Serial.print("state: ");
  Serial.println(state);
  
  if (state == 1) {
    led = true;
    digitalWrite(led_pin, led);
  }

  if (state == 2) {
    led = !led;
    digitalWrite(led_pin, led);
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT);

  timer.every(1000/flash_freq, check_should_toggle);
}

void loop() {
  timer.tick();
}

void serialEvent() {
  while(Serial.available()) {
    char ch = Serial.read();
    //Serial.println(ch);
    if(ch == 'a') {
      state = 2;
    } else {
      state = 1;
    }
  }
}
