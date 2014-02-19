#include <Servo.h>

#define MIN_THROTTLE 1100 // THESE CAN CHANGE DEPENDING ON INTERNAL VOLTAGE BLACK MAGIC
#define MIN_PWM 800 // THESE CAN CHANGE DEPENDING ON INTERNAL VOLTAGE BLACK MAGIC
#define MID_PWM 1500 // THESE CAN CHANGE DEPENDING ON INTERNAL VOLTAGE BLACK MAGIC
#define MAX_PWM 2195 // THESE CAN CHANGE DEPENDING ON INTERNAL VOLTAGE BLACK MAGIC

#define TRIGPIN 3
#define ECHOPIN 2
#define TOCM 29.1

Servo pitch_pin;
Servo roll_pin;
Servo throttle_pin;
Servo yaw_pin;
Servo stabalizer;

// Inputs from usb serial
int pitch_input = 0;
int roll_input = 0;
int throttle_input = 0;
int yaw_input = 0;
int arm_input = 0;
int hover_input = 0;

// Actual pwm timing outputs for each motor
int pitch_output = 0;
int roll_output = 0;
int throttle_output = 0;
int yaw_output = 0;

// Used so that arming/stabalization persists
int COPTER_ARMED = 0;
int STABALIZED = 0;

// For hover
int height = 0;
int hover_set = 0;
int altitude_threshold = 0;
int hover_throttle = 0;

void setup(){
    pitch_pin.attach(A1);
    roll_pin.attach(A4);
    throttle_pin.attach(A3);
    yaw_pin.attach(A2);
    stabalizer.attach (A0);
      
    // For the range sensor
    pinMode(TRIGPIN, OUTPUT);
    pinMode(ECHOPIN, INPUT);

    // Sets outputs to min
    resetOutputs ();

    Serial.begin(9600);
}


void loop()
{
    parseSerial ();

    getHeight ();

    mapInputs ();

    sendCommand ();
}
    
void getHeight ()
{
    int duration;

    digitalWrite(TRIGPIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGPIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGPIN, LOW);

    duration = pulseIn (ECHOPIN, HIGH);
    height = (duration/2) / TOCM;

    //Serial.print(height);
    //Serial.println(" cm");

    delay(5);
}


void startStabalizer ()
{
  stabalizer.writeMicroseconds(MAX_PWM); 
  delayMicroseconds(1000);
}

void quitStabalizer ()
{
  stabalizer.writeMicroseconds(MIN_PWM); 
  delayMicroseconds(1000);
}

void mapInputs ()
{
    if (arm_input)
    {
        if (!COPTER_ARMED)
        {
            // Start stabalizer before arming
            // startStabalizer definetely working
            if (!STABALIZED) 
                {
                        startStabalizer ();
                }
            arm ();
            COPTER_ARMED = 1;
        }
    }
    if (!arm_input)
    {
        if (COPTER_ARMED)
        {

            unarm ();
            COPTER_ARMED = 0;
            // End stabalizer after unarming
            // quitStabalizer does not appear to be working well but it should not matter
            if (STABALIZED) 
                {
                        quitStabalizer ();
                }
        }
    }
    
    if (hover_input && !hover_set)
    {
        // Step 1: read current height
        hover_set = 1;
        altitude_threshold = height;
        hover_throttle = throttle_input;
    }
    else if (!hover_input && hover_set)
    {
        hover_set = 0;
    }
    
    if (hover_set) { hover ();}
    
    pitch_output = map (pitch_input, -100, 100, MIN_PWM, MAX_PWM); 
    roll_output = map (roll_input, -100, 100, MIN_PWM, MAX_PWM); 
    throttle_output = map (throttle_input, 0, 100, MIN_THROTTLE, MAX_PWM); 
    yaw_output = map (yaw_input, -100, 100, MIN_PWM, MAX_PWM); 
}

void hover ()
{
    // altitude in cm
    if (height < altitude_threshold)
    {
        //hover_throttle += 1;
        throttle_input += 1;
        if (throttle_input > 100) { throttle_input = 100; }
    }
    else if (height > altitude_threshold)
    {
        //hover_throttle -= 1;
        throttle_input -= 1;
        if (throttle_input < 0) { throttle_input = 0; }

    }

    //throttle_input = hover_throttle;

}

void resetOutputs ()
{
    pitch_output = MID_PWM;
    roll_output = MID_PWM;
    throttle_output = MIN_THROTTLE;
    yaw_output = MID_PWM;
    sendCommand ();
}

    
void parseSerial ()
{
    int i = 0;
    while (Serial.available() > 0)
    {
        // Synchronize to leading 'B'
        do
        {
            i = Serial.read ();
        }
        while (i != 'B');
                
        pitch_input = Serial.parseInt(); 
        yaw_input = Serial.parseInt(); 
        roll_input = Serial.parseInt(); 
        throttle_input = Serial.parseInt(); 
        arm_input = Serial.parseInt();
        hover_input = Serial.parseInt();

        if (Serial.read() == '\n')
        {
            //Serial.print(pitch_input);
            //Serial.print (" ");
            //Serial.print(yaw_input);
            //Serial.print (" ");
            //Serial.print(roll_input);
            //Serial.print (" ");
            //Serial.print(throttle_input);
            //Serial.println(arm_input);
            //Serial.print (" ");

            return;
        }
                
    }
}

void arm()
{
    // Safeguard against arming and immedietly taking off
    if (throttle_output == MIN_THROTTLE)
    {
        resetOutputs ();

        throttle_output = MIN_THROTTLE;
        yaw_output = MIN_PWM;
        sendCommand();

        delay(2000);

        yaw_output = MID_PWM;
    }
}

void unarm()
{
    // Safegaurd against unarming in midair
    if (throttle_output == MIN_THROTTLE)
    {
        resetOutputs ();

        throttle_output = MIN_THROTTLE;
        yaw_output = MAX_PWM;
        sendCommand();

        delay(2000);

        yaw_output = MID_PWM;
    }
}

void sendCommand()
{
    yaw_pin.writeMicroseconds(yaw_output);
    delayMicroseconds(1000);

    pitch_pin.writeMicroseconds(pitch_output); 
    delayMicroseconds(1000);   

    roll_pin.writeMicroseconds(roll_output);
    delayMicroseconds(1000); 

    throttle_pin.writeMicroseconds(throttle_output);
    delayMicroseconds(1000);
}

