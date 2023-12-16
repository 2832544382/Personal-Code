// Replace the ? with correct pin numbers
// https://www.pololu.com/docs/0J83/5.9
#define L_PWM_PIN 10
#define L_DIR_PIN 16
#define R_PWM_PIN 9
#define R_DIR_PIN 15

#define FWD LOW
#define REV HIGH

class motor{

  public:

  motors(){
    
  }


   // Runs once.
  void initialise() {
  
    // Set all the motor pins as outputs.
    // There are 4 pins in total to set.
    // ...
    pinMode(L_PWM_PIN,OUTPUT);
    pinMode(L_DIR_PIN, OUTPUT);
    pinMode(R_PWM_PIN, OUTPUT);
    pinMode(R_DIR_PIN, OUTPUT);
  
    // Set initial direction (HIGH/LOW)
    // for the direction pins.
    digitalWrite(L_DIR_PIN, FWD); // Set left motor direction to forward (FWD)
    digitalWrite(R_DIR_PIN, FWD); // Set right motor direction to forward (FWD)
  
    // Set initial power values for the PWM
    // Pins.
    // ...
    analogWrite(L_PWM_PIN, 0);
    analogWrite(R_PWM_PIN, 0);
  
    // Start serial, send debug text.
    Serial.begin(9600);
    delay(1000);
    Serial.println("***RESET***");
  
  }

    /*
   * Sets the power of the motors using analogWrite().
   * This function sets direction and PWM (power).
   * This function catches all errors of input PWM.
   *  inputs:
   *     pwm   accepts negative, 0 and positve
   *           values.  Sign of value used to set
   *           the direction of the motor.  Values
   *           are limited in range [ ??? : ??? ].
   *           Magnitude used to set analogWrite().
   */
  void setMotorPower( float left_pwm, float right_pwm ) {
    //Ensure the input value pwm is inside a reasonable range
    left_pwm = constrain(left_pwm,-255,255);
    right_pwm = constrain(right_pwm,-255,255);
  
    //Determine the direction of the given value
    digitalWrite(L_DIR_PIN,(left_pwm>=0)? FWD:REV);
    digitalWrite(R_DIR_PIN,(right_pwm>=0)? FWD:REV);
  
    analogWrite(L_PWM_PIN,abs(left_pwm));
    analogWrite(R_PWM_PIN,abs(right_pwm));
  }
  
  
  void makeCycle(){
    // Drive on an arc, or trace a large circle.
    digitalWrite(L_DIR_PIN, FWD);
    digitalWrite(R_DIR_PIN, REV);
    analogWrite(L_PWM_PIN, 50); // Reduce power to make an arc
    analogWrite(R_PWM_PIN, 150);
  }

  void stop(){
    analogWrite(L_PWM_PIN, 0); // Reduce power to make an arc
    analogWrite(R_PWM_PIN, 0);
  }

  // Repeats.
  void loop() {
  
  
  }

};
