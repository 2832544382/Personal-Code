#include "sensor.h"
#include "ema.h";
#include "motor.h"
// Define the number of sensors
#define NUM_SENSORS 5
#define MAX_SAMPLES 10

String grey_level;
String current_grey_level;
sensor linesensor;
ema filter;
motor motors;
// Sensor pins
int sensorPins[NUM_SENSORS] = {A0, A1, A2, A3, A4};
unsigned long start_time = 0;
unsigned long current_time = 0;
#define SLOPE 0.936
#define INTERCEPT 139.847


float DN1_results[ MAX_SAMPLES ];
float DN2_results[ MAX_SAMPLES ];
float DN3_results[ MAX_SAMPLES ];
float DN4_results[ MAX_SAMPLES ];
float DN5_results[ MAX_SAMPLES ];

float ema_process[NUM_SENSORS][MAX_SAMPLES];
float ema_results_one[NUM_SENSORS][MAX_SAMPLES];
float ema_results_two[NUM_SENSORS][MAX_SAMPLES];

String first_ten[10];
int count = 0;


// Sensor weights
float weights[NUM_SENSORS] = {0.9, 1.0, 1.2, 1.0, 0.9};// Adjust weights as needed

void setup() {
  Serial.begin(9600);
  unsigned long start_time = millis();
}

void loop() {
  // Read sensor values

//  motors.setMotorPower(20,20); 
  for (int i = 0; i < MAX_SAMPLES; i++){

    ema_process[0][i] = linesensor.readLineSensor( 0 );
    ema_process[1][i] = linesensor.readLineSensor( 1 );
    ema_process[2][i] = linesensor.readLineSensor( 2 );
    ema_process[3][i] = linesensor.readLineSensor( 3 );
    ema_process[4][i] = linesensor.readLineSensor( 4 );
  }

  // Calculate weighted average
  filter.e_m_a(ema_process, ema_results_one, 0.55);
  
  float weightedAverageOne = calculateWeightedAverage(ema_results_one, weights, 5, 10);
  float lr = linearRegression(SLOPE, weightedAverageOne, INTERCEPT);

  // Print the results
  //Serial.println("Weighted Average(filter first): ");
  //Serial.println(weightedAverageOne);
  //Serial.println("Linear Regression: ");
  //Serial.println(lr);
 // Serial.println(determineGreyDomain(lr));


  
  if (millis() - start_time > 300){
    Serial.println(determineGreyDomain(lr));
    start_time = millis();
  }
  
  motors.setMotorPower(20,20);
}

// Function to calculate weighted average
int calculateWeightedAverage(float data[][MAX_SAMPLES], float weights[], int numRows, int numCols) {
  float sum = 0.0;
  float weightSum = 0.0;

  for (int i = 0; i < numRows; i++) {
    float rowSum = 0.0;

    for (int j = 0; j < numCols; j++) {
      rowSum += data[i][j] * weights[i];
      weightSum += weights[i];
    }
    sum += rowSum;
  }

  return sum / weightSum;
}

float linearRegression(float slope, float rawData, float intercept){
  float processedValue = slope * rawData + intercept;
  return processedValue;
}

String determineGreyDomain(float value) {
  
  if(value <= 2722 + 50  && value >= 2722 - 157){
    grey_level = "grey level 7";
  }else if (value <= 2402 + 157 && value >= 2402 - 174){
    grey_level = "grey level 39";
  }else if(value <= 2045 + 174 && value >= 2045 - 130){
    grey_level = "grey level 71";
  }else if(value <= 1797 + 130 && value >= 1797 - 51){
    grey_level = "grey level 103";
  }else if(value <= 1634 + 111 && value >=  1634 - 122){
    grey_level = "grey level 135";
  }else if(value <= 1390 + 122 && value >=  1390 - 123){
    grey_level = "grey level 167";
  }else if(value <= 1173 + 243 && value >=  1173 - 23){
    grey_level = "grey level 199";
  }else if(value <= 1004 + 103 && value >= 1004 -30){
    grey_level = "grey level 231";
  }else if(value < 974){
    grey_level = "grey level 255";
  }
  return grey_level;
}
