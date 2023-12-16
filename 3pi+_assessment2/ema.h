  # define MAX_LENS 10
  # define SENSOR_SIZES 5
  float window_average;
  float moving_average[SENSOR_SIZES][MAX_LENS];
  
  class ema{
    public:
      ema(){}
  
    void e_m_a(float data[SENSOR_SIZES][MAX_LENS], float results[SENSOR_SIZES][MAX_LENS], float smoothing_factor) {
        for (int i = 0; i < SENSOR_SIZES; i++) {
            results[i][0] = data[i][0];  // 假设第一个值的EMA等于其本身

            for (int j = 1; j < MAX_LENS; j++) {
                window_average = two_decimals((smoothing_factor * data[i][j]) + (1 - smoothing_factor) * results[i][j-1]);
                results[i][j] = window_average;
            }
        }
    }

    void e_m_a_two(){
      
    }
  
    float two_decimals(float number){
      return round(number * 100.0) / 100.0;
    }
  };
