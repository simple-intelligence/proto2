#include <Servo.h>

#define NUM_MOTORS 4

Servo myservo; 
Servo myservo2;
Servo myservo3;
Servo myservo4;
int control[4];
int pin[4] = {5,6,9.10};
char input;
double x = 0;
int starting_point;
int temp[3];

int throttle = 2;
int pitch = 0;
int roll = 1;
int yaw = 3;

void setup(){
  myservo.attach(A5);  // attaches the servo on pin 9 to the servo object   
  myservo2.attach(A4);
  myservo3.attach(A3);
  myservo4.attach(A2);
  //calibrate_motors();
  //setup_motors();
  //all_stop();
  arm();
  Serial.begin(9600);
}

void loop(){
  if(Serial.available()){
    input = Serial.read();
    if(input == 'h'){
        all_stop();
    }
    if(input == 'e'){
        forward();
    }
    else if(input == 'f'){
        right();
    }
    else if(input == 's'){
        left();
    }
    else if(input == 'd'){
        back();
    }
    else if(input == 'q'){
        up();
    }
    else if(input == 'a'){
        down();
    }
    else if(input == 'w'){
      spin_left();
    }
    else if(input == 'r'){
      spin_right();
    }
    else if(input == 'y'){
      arm();  
    }
    else if(input == 'u'){
       unarm(); 
    }
    
    send_command();
}
}

void forward(){
  control[pitch] += 10;
}

void left(){
   control[roll] -= 10;
}

void right(){
   control[roll] += 10;
}

void back(){
  control[pitch] -= 10;
}

void up(){
  control[throttle] += 10;
}

void down(){
  control[throttle] -= 10;
}

void spin_left(){
    control[yaw] -= 10;
}

void spin_right(){
    control[yaw] += 10;
}

void arm(){
    temp[0] = control[yaw];
    temp[1] = control[throttle];
    //temp[2] = control[pitch];
    //control[roll] = 1030;
    //control[pitch] = 1130;
    control[throttle] -= 400;
    control[yaw] = 1030;
    //ntrol[pitch]--;
    //ntrol[roll]--;
    send_command();
    delay(2000);
    control[yaw] = temp[0]; //cause of beeping?
    control[throttle] = temp[1];
    //control[throttle] = temp[1];
    //control[pitch] = temp[2];
    
    
}

void unarm(){
    temp[0] = control[yaw];
    //temp[1] = control[roll];
    //temp[2] = control[pitch];
    //control[roll] = 1950;
    //control[pitch] = 1950;
    control[yaw] = 1950;
    send_command();
    delay(2000);
    control[yaw] = temp[0];
    //control[roll] = temp[1];
    //control[pitch] = temp[2];
    
    
    
}

void all_stop(){
  control[throttle] = starting_point - 340;
  control[pitch] = starting_point;
  control[roll] = starting_point;
  control[yaw] = starting_point;
  
}

void send_command(){
    myservo.writeMicroseconds(control[0]);              // tell servo to go to position in variable 'pos' 
    delayMicroseconds(1000);   
    myservo2.writeMicroseconds(control[1]);
    delayMicroseconds(1500);    // waits 15ms for the servo to reach the position 
    myservo3.writeMicroseconds(control[2]);
    delayMicroseconds(1500);
    myservo4.writeMicroseconds(control[3]);
   
}

void setup_motors(){
  while(x < 1000){
     
     control[0] = map(analogRead(A0), 0, 1023, 1000, 1950);
     control[1] = map(analogRead(A0), 0, 1023, 1000, 1950);
     control[2] = map(analogRead(A0), 0, 1023, 1000, 1950);
     control[3] = map(analogRead(A0), 0, 1023, 1000, 1950);
     starting_point = control[0];
     
     
        // in steps of 1 degree 
    myservo.writeMicroseconds(control[0]);              // tell servo to go to position in variable 'pos' 
    delayMicroseconds(1000);   
    myservo2.writeMicroseconds(control[1]);
    delayMicroseconds(1500);    // waits 15ms for the servo to reach the position 
    myservo3.writeMicroseconds(control[2] - 380);
    delayMicroseconds(1500);
    myservo4.writeMicroseconds(control[3]);
    x += 1;
    Serial.println(x);
  }
}  

void calibrate_motors(){
   for(int i = 0; i < NUM_MOTORS; i++)
     control[i] = 170;
     send_command();
   delay(2000);
   for(int i = 0; i < NUM_MOTORS; i++)
     control[i] = 35; 
     send_command();
   delay(4000);
}
