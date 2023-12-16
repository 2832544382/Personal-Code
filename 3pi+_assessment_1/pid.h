// this #ifndef stops this file
// from being included mored than
// once by the compiler. 
#ifndef _PID_H
#define _PID_H

// Class to contain generic PID algorithm.
class pid {
  public:

    float last_err;
    float p;
    float i;
    float d;
    float sum_i;
    float fb;

    float p_gain;
    float i_gain;
    float d_gain;

    unsigned long last_ts;
  
    // Constructor, must exist.
    pid() {} 

    void initialize(float pk, float ik, float dk){
      last_err = 0;
      p = 0;
      i = 0;
      d = 0;
      sum_i = 0;
      fb = 0;
      p_gain = pk;
      i_gain = ik;
      d_gain = dk;

      last_ts = millis();
  
    }

    void reset(){
      last_err = 0;
      p = 0;
      i = 0;
      d = 0;
      sum_i = 0;
      fb = 0;
      last_ts = millis();
    }

    float update(float spe, float demand){
      float err;
      unsigned long current;
      unsigned long dt;
      float f_dt;
      float diff_err;

      current = millis();
      dt = current - last_ts;
      last_ts = millis();

      f_dt = (float)dt;

      if (f_dt == 0){
        return fb;
      }

      err = demand-spe  ;

      p = p_gain * err;

      sum_i = sum_i + (err * f_dt);

      i = i_gain * sum_i;

      diff_err = (err - last_err) / f_dt;
      last_err = err;
      d = diff_err * d_gain;

      fb = p + i + d;

      return fb;
      
    }

};



#endif
