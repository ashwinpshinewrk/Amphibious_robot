#include <SoftwareSerial.h>

// ===== BLUETOOTH =====
SoftwareSerial BT(2, 3); // RX, TX for HC-05

// ===== BTS7960 PIN DEFINITIONS =====
#define L_RPWM 5
#define L_LPWM 6
#define R_RPWM 9
#define R_LPWM 10

int baseSpeed = 200;
char command;

// ===== Motor Control =====
void setMotor(int rpwmPin, int lpwmPin, int speedVal, bool clockwise) {
  if (clockwise) {
    analogWrite(rpwmPin, speedVal);
    analogWrite(lpwmPin, 0);
  } else {
    analogWrite(rpwmPin, 0);
    analogWrite(lpwmPin, speedVal);
  }
}

void stopLeftMotor() {
  analogWrite(L_RPWM, 0);
  analogWrite(L_LPWM, 0);
}

void stopRightMotor() {
  analogWrite(R_RPWM, 0);
  analogWrite(R_LPWM, 0);
}

void stopMotors() {
  stopLeftMotor();
  stopRightMotor();
}

// ===== Motions =====

// Forward: Left CCW, Right CW
void forward() {
  setMotor(L_RPWM, L_LPWM, baseSpeed, true); // Left CCW
  setMotor(R_RPWM, R_LPWM, baseSpeed, false);  // Right CW
}

// Backward: Left CW, Right CCW
void backward() {
  setMotor(L_RPWM, L_LPWM, baseSpeed, false);  // Left CW
  setMotor(R_RPWM, R_LPWM, baseSpeed, true); // Right CCW
}

// Keep these AS IT IS
void leftStraight() {
  setMotor(L_RPWM, L_LPWM, baseSpeed, true);
  setMotor(R_RPWM, R_LPWM, baseSpeed, true);
}

void rightStraight() {
  setMotor(L_RPWM, L_LPWM, baseSpeed, false);
  setMotor(R_RPWM, R_LPWM, baseSpeed, false);
}

// Right Arc: Left CCW, Right STOP
void rightArc() {
  setMotor(L_RPWM, L_LPWM, baseSpeed, true); // Left CCW
  stopRightMotor();
}

// Left Arc: Right CW, Left STOP
void leftArc() {
  stopLeftMotor();
  setMotor(R_RPWM, R_LPWM, baseSpeed, false); // Right CW
}

// Right Back Turn: Right CCW, Left STOP
void rightBackTurn() {
  stopRightMotor();
  setMotor(L_RPWM, L_LPWM, baseSpeed, false); // Right CCW
}

// Left Back Turn: Left CW, Right STOP
void leftBackTurn() {
  setMotor(R_RPWM, R_LPWM, baseSpeed, true); // Left CW
  stopLeftMotor();
}

// ===== Setup =====
void setup() {
  Serial.begin(9600);
  BT.begin(9600);

  pinMode(L_RPWM, OUTPUT);
  pinMode(L_LPWM, OUTPUT);
  pinMode(R_RPWM, OUTPUT);
  pinMode(R_LPWM, OUTPUT);

  stopMotors();
  Serial.println("Bluetooth RC Controller Ready");
}

// ===== Loop =====
void loop() {
  if (BT.available()) {
    command = BT.read();

    // Speed control (0–9)
    if (isDigit(command)) {
      baseSpeed = map(command - '0', 0, 9, 0, 255);
      Serial.print("Speed: ");
      Serial.println(baseSpeed);
      return;
    }

    switch (command) {
      case 'F': forward(); break;
      case 'B': backward(); break;
      case 'L': leftStraight(); break;
      case 'R': rightStraight(); break;
      case 'I': rightArc(); break;
      case 'G': leftArc(); break;
      case 'J': rightBackTurn(); break;
      case 'H': leftBackTurn(); break;
      case 'S': stopMotors(); break;
    }
  }
}