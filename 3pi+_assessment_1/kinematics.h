// this #ifndef stops this file
// from being included mored than
// once by the compiler. 
#ifndef _KINEMATICS_H
#define _KINEMATICS_H

float r = 16;
//from wheel to point p is 46mm
float l = 90;
float xr;
float xi;
float yi;
float z;
float theta_r;
float theta_i;
float theta;

float left_default = 2 * PI * r / 360;
float right_default = 2 * PI * r / 360;

// Class to track robot position.
class kinematics {
  public:
  
    // Constructor, must exist.
    kinematics() {

    } 

    // Use this function to update
    // your kinematics
    void update(float delta_left, float delta_right) {
      
      
      xr = ((delta_left * left_default) + (delta_right * right_default)) / 2.0;
      theta_r = (((delta_left * left_default) - (delta_right * right_default)) / (l));

      
      xi = xi + xr * cos(theta_i);
      yi = yi + xr * sin(theta_i);

      theta_i += theta_r;

      /*
      Serial.println(delta_left);
      Serial.println(delta_right);

      
      
      
      
      Serial.print("yi: ");
      Serial.println(yi);
      Serial.print("xi: ");
      Serial.println(xi);
      
      Serial.print("theta_i: ");
      Serial.println(theta_i);

      Serial.print("theta_r: ");
      Serial.println(theta_r);
      
       
      Serial.print("left: ");
      Serial.println(delta_left);
      Serial.print("right: ");
      Serial.println(delta_right);
      
       
      Serial.print("xr: ");
      Serial.println(xr);
      
            
      
      */
      
      
    
      
      
      
      

    }

    float get_x(){
      return xi;
    }

    float get_y(){
      return yi;
    }

    float get_theta_i(){
      /*
      if (theta_i > 2 * PI){
        theta_i = (int(theta_i * 100) % int(2 * PI * 100)/100);
        return theta_i;
      }
      else{
        return theta_i;
      }
      */

      return theta_i;
      
      
    }

    float get_theta_r(){
      return theta_r;
    }
    
    float get_z(float x, float y){
      z = (float)sqrt((x*x) + (y*y));
      return z;
    }

    float two_decimals(float number){
      return round(number * 100.0) / 100.0;
    }


};



#endif
