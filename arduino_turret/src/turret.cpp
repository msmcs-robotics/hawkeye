#include <Arduino.h>
#include <Servo.h>

// Use Serial for now
//#include <Wire.h>

struct {
    int baud = 9600;
    int max_servo_angle = 180;

    int width_resolution = 500;
    int height_resolution = 500;

    int delay_time = 100;

} info_vars;

struct {
    int xServoPin = 9;
    int yServoPin = 10;

    int statusLedPin = 13;

} pinout;

Servo xServo;
Servo yServo;

void setup() {
    Serial.begin(info_vars.baud);
    
    xServo.attach(pinout.xServoPin);
    yServo.attach(pinout.yServoPin);
    pinMode(pinout.statusLedPin, OUTPUT);

    Serial.println("Setup complete");
    Serial.println("Waiting for input...\nFormat: (x,y)");
}

// Convert x and y coordinates to servo angles

int convertX(int x) {
    float x_tmp = map(x, 0, info_vars.width_resolution, 0, info_vars.max_servo_angle);
    return (int) x_tmp;
}

int convertY(int y) {
    float y_tmp = map(y, 0, info_vars.height_resolution, 0, info_vars.max_servo_angle);
    return (int) y_tmp;
}

// Get x and y input from serial
// Format: (x,y)

int getX(String input) {
    int x = input.substring(1, input.indexOf(',')).toInt();
    return x;
}

int getY(String input) {
    int y = input.substring(input.indexOf(',') + 1, input.indexOf(')')).toInt();
    return y;
}

// Main loop

void loop() {
    // blink status led
    digitalWrite(pinout.statusLedPin, HIGH);
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        int x = getX(input);
        int y = getY(input);
        xServo.write(convertX(x));
        yServo.write(convertY(y));
        Serial.println("Input x: " + String(x) + " y: " + String(y));
        Serial.println("Converted x: " + String(convertX(x)) + " y: " + String(convertY(y)));
    }
    delay(info_vars.delay_time);
    digitalWrite(pinout.statusLedPin, LOW);
}

