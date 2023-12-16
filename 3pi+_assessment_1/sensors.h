// this #ifndef stops this file
// from being included mored than
// once by the compiler. 
//#ifndef _LINESENSOR_H
//#define _LINESENSOR_H

# define EMIT_PIN    11    // Documentation says 11.
# define LS_LEFT_PIN 12   // Complete for DN1 pin
# define LS_MIDLEFT_PIN 18   // Complete for DN2 pin
# define LS_MIDDLE_PIN 20   // Complete for DN3 pin
# define LS_MIDRIGHT_PIN 21   // Complete for DN4 pin
# define LS_RIGHT_PIN 22   // Complete for DN5 pin

// Store our pin numbers into an array, which means
// we can conveniently select one later.
// ls(line sensor)_pin
int ls_pins[5] = {LS_LEFT_PIN,
                  LS_MIDLEFT_PIN,
                  LS_MIDDLE_PIN,
                  LS_MIDRIGHT_PIN,
                  LS_RIGHT_PIN };

class sensors{
  public:
    sensors(){}

    void initialize(){
      // Set some initial pin modes and states
      pinMode( EMIT_PIN, INPUT ); // Set EMIT as an input (off)
      pinMode( LS_LEFT_PIN, INPUT );     // Set line sensor pin to input
      pinMode( LS_MIDLEFT_PIN, INPUT );
      pinMode( LS_MIDDLE_PIN, INPUT );
      pinMode( LS_MIDRIGHT_PIN, INPUT );
      pinMode( LS_RIGHT_PIN, INPUT );
    }
    
    float rdLineSensor( int number ) {

      if( number < 0 ) {
  
          Serial.print("Illegal input: ");
          Serial.print(number);
          return -1;
      }
      if( number > 4 ) {
          Serial.print("Illegal input: ");
          Serial.print(number);
          return -1;
      }
  
      pinMode( EMIT_PIN, OUTPUT );
      digitalWrite( EMIT_PIN, HIGH );
    
      pinMode( ls_pins[number], OUTPUT );
      digitalWrite( ls_pins[number], HIGH );
      delayMicroseconds( 10 );
      unsigned long start_time = micros();
      pinMode( ls_pins[number]  , INPUT );
      
      while( digitalRead( ls_pins[number] ) == HIGH ) {
        // Do nothing here (waiting).
      }
      unsigned long end_time = micros();
      unsigned long elapsed_time;
      
      elapsed_time = end_time  - start_time;
  
      pinMode( EMIT_PIN, INPUT );
  
      // Give the result back to wherever this
      // function was called from.
      return (float)elapsed_time;
    }

    float find_smallest(float sensor_data[]){
      int smallest = sensor_data[0];
      for(int i = 0; i < sizeof(sensor_data); i++){
        if(smallest > sensor_data[i]){
          smallest = sensor_data[i];
        }
      }
      return smallest;
    }

    float weight_single(float s2, float s4){
      float sum = s2 + s4;
      float n2 = (s2 / sum) * 2;
      float n4 = (s4 / sum) * 2;
      float weight = n2 - n4;
      return weight;
    }

    bool on_line(float sensor2,float sensor3,float sensor4, float threshold){
      if(sensor2 > threshold || sensor4 > threshold || sensor3 > threshold){
        return true;
      }
      else{
        return false;
      }
    }
   
};
