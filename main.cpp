#include <Arduino.h>
#include "config.h"

int bt_byte = 0;
int message[3] = {};

volatile bool LEFT_MOTOR_DIR = 0;
volatile bool RIGHT_MOTOR_DIR = 0;
volatile short LEFT_MOTOR_SPEED = 0;
volatile short RIGHT_MOTOR_SPEED = 0;

volatile bool EX_LEFT_MOTOR_DIR = 0;
volatile bool EX_RIGHT_MOTOR_DIR = 0;
volatile short EX_LEFT_MOTOR_SPEED = 100;
volatile short EX_RIGHT_MOTOR_SPEED = 0;

void motor_pwm_set(short pin, int speed){

  if(speed > 100){
    speed = 100;
  }
  if(speed < 0){
    speed = 0;
  }

  speed = map(speed, 0, 100, 0, 255);
  Serial.println(speed);
  analogWrite(pin, speed);
}

void motor_control(bool side, short speed, bool direction = FORWARD){
  if(side == LEFT){
    if(direction == FORWARD){
      motor_pwm_set(LEFT_MOTOR_PIN_F, speed);
      motor_pwm_set(LEFT_MOTOR_PIN_S, 0);
    }
    else{
      motor_pwm_set(LEFT_MOTOR_PIN_S, speed);
      motor_pwm_set(LEFT_MOTOR_PIN_F, 0);
    }
  }
  else{
    if(direction == FORWARD){
      motor_pwm_set(RIGHT_MOTOR_PIN_F, speed);
      motor_pwm_set(RIGHT_MOTOR_PIN_S, 0);
    }
    else{
      motor_pwm_set(RIGHT_MOTOR_PIN_S, speed);
      motor_pwm_set(RIGHT_MOTOR_PIN_F, 0);
    }
  }
}

void motor_stop(short side = BOTH){
  if(side == LEFT){
    motor_control(LEFT, 0);
  }
  else{
    if(side == RIGHT){
      motor_control(RIGHT, 0);
    }
    else{
      motor_control(LEFT, 0);
      motor_control(RIGHT, 0);
    }
  }

}

void setup() {

  pinMode(LEFT_MOTOR_PIN_F, OUTPUT);
  pinMode(LEFT_MOTOR_PIN_S, OUTPUT);
  pinMode(RIGHT_MOTOR_PIN_F, OUTPUT);
  pinMode(RIGHT_MOTOR_PIN_S, OUTPUT);

  Serial.begin(9600);
  Serial.println("Starting the controller");
  delay(100);

}

void get_serial(){
  if(Serial.available()>=3){
  while(Serial.available() != 3){
    Serial.read();
  }
  for(int i = 0; i < 3; i++){
    message[i] = Serial.read();
  }
  Serial.println("Message is:");
  for(int i = 0; i < 3; i++){
    Serial.println(message[i]);
  }
  }
}

void loop() {
  get_serial();
  motor_control(LEFT, 100, FORWARD);
  delay(2000);
  motor_control(RIGHT, 100, FORWARD);
  delay(2500);
  motor_stop();
  delay(2000);
  motor_control(LEFT, 90, BACKWARD);
  motor_control(RIGHT, 90, BACKWARD);
  delay(2000);
  motor_stop();


}