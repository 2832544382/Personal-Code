// this #ifndef stops this file
// from being included mored than
// once by the compiler. 
//#ifndef _MOTORS_H
//#define _MOTORS_H

# define L_PWM_PIN 10
# define L_DIR_PIN 16
# define R_PWM_PIN 9
# define R_DIR_PIN 15

# define FWD LOW
# define REV HIGH

class motors{
    public:
      motors(){}

      void initialize(){
        pinMode(L_PWM_PIN, OUTPUT);
        pinMode(L_DIR_PIN, OUTPUT);
        pinMode(R_PWM_PIN, OUTPUT);
        pinMode(R_DIR_PIN, OUTPUT);

        digitalWrite(L_DIR_PIN, FWD);
        digitalWrite(R_DIR_PIN, FWD);

        analogWrite(L_PWM_PIN, 0);
        analogWrite(R_PWM_PIN, 0);
      }

      void foward() {
        digitalWrite(L_DIR_PIN, FWD);
        digitalWrite(R_DIR_PIN, FWD);
        analogWrite( L_PWM_PIN, 25);
        analogWrite( R_PWM_PIN, 25);
      }

      void wheel_stop(){
        analogWrite( L_PWM_PIN, 0);
        analogWrite( R_PWM_PIN, 0);
      }

      void spin_right(){
        digitalWrite(L_DIR_PIN, FWD);
        digitalWrite(R_DIR_PIN, REV);
        analogWrite( L_PWM_PIN, 45);
        analogWrite( R_PWM_PIN, 45);
      }

      void spin_left(){
        digitalWrite(L_DIR_PIN, REV);
        digitalWrite(R_DIR_PIN, FWD);
        analogWrite( L_PWM_PIN, 45);
        analogWrite( R_PWM_PIN, 45);
      }

      void back_around(){
        digitalWrite(L_DIR_PIN, FWD);
        digitalWrite(R_DIR_PIN, REV);
        analogWrite( L_PWM_PIN, 30);
        analogWrite( R_PWM_PIN, 30);
      }

      void set_speed(float left, float right){
        if (left < 0){
          digitalWrite(L_DIR_PIN, REV);
        }
        else{
          digitalWrite(L_DIR_PIN, FWD);  
        }
        
        if (right < 0){
          digitalWrite(R_DIR_PIN, REV);
        }
        else{
          digitalWrite(R_DIR_PIN, FWD);  
        }

        analogWrite( L_PWM_PIN, abs(left));
        analogWrite( R_PWM_PIN, abs(right));
      }

      void alternative_run(float weight, bool on_line){
        float bias_pwm = 20;
        float max_pwm = 25;
         //Serial.println("weight:");
         //Serial.println(weight);
        if(on_line == true){
          float left_pwm = bias_pwm - (weight * max_pwm);
          float right_pwm = bias_pwm + (weight * max_pwm);
          set_speed(left_pwm, right_pwm);
        }
        else{
          set_speed(0,0); 
        }
      }
};
