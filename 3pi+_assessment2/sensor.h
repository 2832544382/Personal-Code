#ifndef SENSOR_H
#define SENSOR_H

#define EMIT_PIN    11    // Documentation says 11.
#define LS_LEFT_PIN 12   // Complete for DN1 pin
#define LS_MIDLEFT_PIN 18   // Complete for DN2 pin
#define LS_MIDDLE_PIN 20   // Complete for DN3 pin
#define LS_MIDRIGHT_PIN 21   // Complete for DN4 pin
#define LS_RIGHT_PIN 22   // Complete for DN5 pin


class sensor {
  public:
// Store our pin numbers into an array, which means
// we can conveniently select one later.
// ls(line sensor)_pin

   sensor() {

   }


    void intialise(){
    // Set some initial pin modes and states
    pinMode( EMIT_PIN, INPUT ); // Set EMIT as an input (off)
    pinMode( LS_LEFT_PIN, INPUT );     // Set line sensor pin to input
    pinMode( LS_MIDLEFT_PIN, INPUT );     // Set line sensor pin to input
    pinMode( LS_MIDDLE_PIN, INPUT );
    pinMode( LS_MIDRIGHT_PIN, INPUT );
    pinMode( LS_RIGHT_PIN, INPUT );
    // Start Serial, wait to connect, print a debug message.
    Serial.begin(9600);
    delay(1500);
    Serial.println("***RESET***");
    }
  int ls_pins[5] = {LS_LEFT_PIN,
                    LS_MIDLEFT_PIN,
                    LS_MIDDLE_PIN,
                    LS_MIDRIGHT_PIN,
                    LS_RIGHT_PIN };
  
  
  #define MAX_SAMPLES 5
  float results[ MAX_SAMPLES ]; // An array of MAX_SAMPLES length
  
  void setup() {
  

  
  } // End of setup()
  
  
  void loop() {
    // Collect MAX_SAMPLES readings for each sensor.
    for (int sensorNumber = 0; sensorNumber < 5; sensorNumber++) {
      for (int sample = 0; sample < MAX_SAMPLES; sample++) {
        // Read the current sensor and save the reading into results.
        results[sample] = readLineSensor(sensorNumber);
        delay(200);
      }
    }
  
    // Print the collected results for all sensors.
    for (int sensorNumber = 0; sensorNumber < 5; sensorNumber++) {
      Serial.print("Results for Sensor ");
      Serial.println(sensorNumber);
      for (int i = 0; i < MAX_SAMPLES; i++) {
        Serial.println(results[i]);
      }
    }
  
    // Delay to control the printing interval.
    delay(1000);
  }
  
  
  // A function to read a line sensor.
  // Specify which sensor to read with number.
  // Number should be a value between 0 and 4
  float readLineSensor(int number) {
  
      // These two if statements should be
      // completed to prevent a memory error.
      // What would be a good value to return that
      // would not be mistaken for a sensor reading?
      if( number < 0 ) {
          return -1;
      }
      if( number > 4 ) {
          return -1;
      }
  
  
      // Complete the steps referring to the pseudocode block
      // Algorithm 1.
      // The first steps have been done for you.
      // Fix parts labelled ????
      // Some steps are missing - add these.
      pinMode( EMIT_PIN, OUTPUT );
      digitalWrite( EMIT_PIN, HIGH );
  
      // In this line, we retrieve the pin value
      // stored in the array "ls_pins" at location
      // "number".  So it is like a look-up table.
      // We can think of ls_pins in memory like:
      // Index 0, Index 1, Index 2, Index 3, Index 4
      //[  DN1  ][   DN2 ][  DN3  ][  DN4  ][  DN5  ]
      pinMode( ls_pins[ number ], OUTPUT );
  
      digitalWrite( ls_pins[number], HIGH );
      delayMicroseconds( 10 );
  
      unsigned long time_duration = 1000000;
  
      pinMode( ls_pins[ number ], INPUT );
  
      unsigned long start_time = micros();
  
      while( digitalRead( ls_pins[number] ) == HIGH ) {
      }
  
      unsigned long end_time = micros();
  
  
      unsigned long elapsed_time = end_time - start_time;
  
      // Give the result back to wherever this
      // function was called from.
      return (float)elapsed_time;
  }
};

#endif // SENSOR_H
