#include <Arduino.h>
#include <SoftwareSerial.h>

const byte txPin = A2;
const byte rxPin = A3;

const int EN_pin = 8;     // stepper motor enable , active low
const int A_DIR_pin  = 9;
const int X_DIR_pin = 5;
const int Y_DIR_pin = 6;
const int Z_DIR_pin = 7;
const int A_STEP_pin = 10;
const int X_STEP_pin = 2;
const int Y_STEP_pin = 3;
const int Z_STEP_pin = 4;

void check_message(void);
void execute_command(void);
void setup_ios(void);