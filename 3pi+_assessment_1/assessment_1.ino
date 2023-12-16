#include "sensors.h";
#include "motors.h";
#include "encoders.h";
#include "kinematics.h"
#include "pid.h";


#define STATE_INITIAL 0
#define STATE_FIND_LINE 1
#define STATE_TURN 2
#define STATE_SIMPLE_LINE 3
#define STATE_GOAL 4
#define STATE_BACK 5

int state;
bool get_threshold = false;
//float threshold_m;
float threshold_n;
float threshold_s;

bool turn_left = false;
bool turn_right = false;
bool turn_back = false;
bool turn_special = false;
bool turn_tri = false;
bool turn_all_black = false;

bool find_special = false;
bool find_left = false;
bool find_right = false;
bool find_tri = false;
bool find_back = false;

bool second_left = false;
bool second_right = false;
bool second_stop = false;

bool is_turn = false;
bool is_tri = false;
bool is_inter = false;
bool is_finish = false;

long current_left_rotation;
long current_right_rotation;
long left_diff;
long right_diff;

unsigned long current_time = 0;
const long interval = 10;

float delta_left;
float delta_right;

float xx;
float yy;
float the;
float origin;

float demand = 1.8;

unsigned long start_time;
unsigned long diff_time;
unsigned long inter_time;
unsigned long line_time;
unsigned long turn_time;
unsigned long test;

float turn_theta;
float turn_angle;
float t;
float final_distance;
float final_x;

// Store our pin numbers into an array, which means
// we can conveniently select one later.
// ls(line sensor)_pin

# define MAX_SAMPLES 1
float DN1_results[ MAX_SAMPLES ];
float DN2_results[ MAX_SAMPLES ];
float DN3_results[ MAX_SAMPLES ];
float DN4_results[ MAX_SAMPLES ];
float DN5_results[ MAX_SAMPLES ];

sensors sensor;
motors motor;
kinematics kinematic;

//pid left_speed;
//pid right_speed;

//float e1_ave;
//float e0_ave;

void setup() {

  motor.initialize();
  sensor.initialize();
  setupEncoder0();
  setupEncoder1();
  
  //left_speed.initialize(180.0, 0.0, 0.0);
  //right_speed.initialize(0.0, 0.0, 0.0);



  

  state = STATE_INITIAL;
  //state = STATE_BACK;




  
  Serial.begin(9600);
  delay(1000);
  Serial.println("***RESET***");

  start_time = millis();

  current_left_rotation = count_e1;
  current_right_rotation = count_e0;

  //motor.set_speed(0, 0);

  //left_speed.reset();
  //right_speed.reset();

  //e1_ave = 0.0;
  //e0_ave = 0.0;

  //test = millis();

} // End of setup()


void loop() {
  
  for (int i = 0; i < MAX_SAMPLES; i++){
    DN1_results[i] = sensor.rdLineSensor( 0 );
    DN2_results[i] = sensor.rdLineSensor( 1 );
    DN3_results[i] = sensor.rdLineSensor( 2 );
    DN4_results[i] = sensor.rdLineSensor( 3 );
    DN5_results[i] = sensor.rdLineSensor( 4 );
  }

  if (get_threshold == false){
    //threshold_m = (DN2_results[0] + DN4_results[0])/2;
    threshold_n = DN3_results[0]+200;
    threshold_s = (DN1_results[0] + DN5_results[0])/2 + 200;
    get_threshold = true;
  }

  if (period_record() == true){
    float enc_left = count_e1;
    float enc_right = count_e0;
    
    left_diff = enc_left - current_left_rotation;
    right_diff = enc_right - current_right_rotation;  
    
    current_left_rotation = enc_left;
    current_right_rotation = enc_right;
    
    delta_left = (float)left_diff;
    delta_right = (float)right_diff;

    //delta_left /= (float)interval; 
    //delta_right /= (float)interval;

    //e1_ave = (e1_ave * 0.7) + (delta_left * 0.3);
    //e0_ave = (e0_ave * 0.7) + (delta_right * 0.3);
    
    //float pwm;

    //pwm = left_speed.update(delta_left, demand);
    //motor.set_speed(pwm, 0);
  
    //Serial.print(e1_ave);
    //Serial.print(",");

    kinematic.update(delta_left, delta_right);
  }

 
  float weight = sensor.weight_single(DN2_results[0], DN4_results[0]);
  bool is_on_line = sensor.on_line(DN2_results[0], DN3_results[0],DN4_results[0], threshold_n);

  if (state == STATE_INITIAL){
    unsigned long elapsed;
    elapsed = millis() - start_time;
    
    if (elapsed > 1000){
      change_state(STATE_FIND_LINE);
    }
    else{
      motor.foward();
    }
  }

  else if (state == STATE_FIND_LINE){
    if ((DN3_results[0]) > threshold_n){
      diff_time = millis();
      change_state(STATE_SIMPLE_LINE);
    }
    else{
      motor.foward();
    }
  }

  else if (state == STATE_SIMPLE_LINE){
    
    unsigned long elapsed;
    elapsed = millis() - start_time;
    if (elapsed > 33000 && DN3_results[0] < threshold_n + 200 && DN2_results[0] < threshold_n +200 && DN4_results[0] < threshold_n + 200){
      xx = kinematic.get_x();
      yy = kinematic.get_y();

      the = (1.5*PI) - atan2(xx, yy) - 0.21;
      
      t = kinematic.get_theta_i();
      change_state(STATE_BACK);  
    }

    motor.alternative_run(weight, is_on_line);
    
    
    if ((DN1_results[0] > threshold_s && DN3_results[0] > threshold_n && DN5_results[0] > threshold_s) ||
             (DN1_results[0] > threshold_s && DN3_results[0] > threshold_n && DN5_results[0] < threshold_s) ||
             (DN1_results[0] > threshold_s && DN5_results[0] > threshold_s) ||
             (DN1_results[0] < threshold_s && DN3_results[0] > threshold_n && DN5_results[0] > threshold_s+500)){
               turn_left = true;
               change_state(STATE_TURN);
     }

    else if ((DN1_results[0] < threshold_s && DN3_results[0] < threshold_n && DN2_results[0] < threshold_n && DN4_results[0] < threshold_n && DN5_results[0] > threshold_s)||
             (DN3_results[0] < threshold_n && DN2_results[0] < threshold_n && DN4_results[0])){
      turn_right = true;
      change_state(STATE_TURN);
    }    
  }

  else if (state == STATE_TURN){
    
    if (turn_left == true){
      motor.spin_left();
      if (DN3_results[0] > threshold_s){
        turn_left = false;
        change_state(STATE_SIMPLE_LINE);
      }
    }
    else if (turn_right == true){
      motor.spin_right(); 
      if (DN3_results[0] > threshold_n){
        turn_right = false;
        change_state(STATE_SIMPLE_LINE);
      } 
    }
  }

  else if (state == STATE_BACK){

    float current_t = kinematic.get_theta_i();
    Serial.println(the - t);
    Serial.println(current_t);
    if ((the - t) - current_t > 0.01){
      motor.set_speed(17,-17);
    }
    else if((the - t) - current_t < -0.01){
      motor.set_speed(-17,17);
    }

    else {
      change_state(STATE_GOAL);
    }
    
    //motor.foward();
    //motor.alternative_run(weight, is_on_line);
  }

  else if (state == STATE_GOAL) {
    
    float now = kinematic.get_x();
    if (abs(kinematic.get_x()) > 90 and abs(kinematic.get_y()) > 90){
      motor.set_speed(50,50);
    }
    else{
      motor.wheel_stop();
    }
  }

  
  else {

    // You can catch situations where the robot
    // attempts to move into an unknown state.
    Serial.print("Error: ");
    Serial.println(state);
  }
}

void change_state(int change){
  state = change;
}

bool period_record(){
  bool is_time = false;
  unsigned long start_time = millis();
  if (start_time - current_time >= interval){
    is_time = true;
    current_time = start_time;
  }
  return is_time;
  
}
