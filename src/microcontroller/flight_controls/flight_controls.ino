#include <Servo.h>

#define NUM_MOTORS 4
#define MIN_PWM 800
#define MID_PWM 1499
#define MAX_PWM 2197

Servo pitch_pin; 
Servo roll_pin;
Servo throttle_pin;
Servo yaw_pin;
Servo stabalizer;

int pitch_input = 0;
int roll_input = 0;
int throttle_input = 0;
int yaw_input = 0;
int arm_input = 0;

int pitch_output = 0;
int roll_output = 0;
int throttle_output = 0;
int yaw_output = 0;

int COPTER_ARMED = 0;

void setup(){
	pitch_pin.attach(A5);   	
	roll_pin.attach(A4);
	throttle_pin.attach(A3);
	yaw_pin.attach(A2);
        stabalizer.attach (A0);	
      
	resetOutputs ();

	Serial.begin(9600);
}


void loop()
{
	parseSerial ();

	mapInputs ();

	sendCommand ();
}
	
void startStabalizer ()
{
  stabalizer.writeMicroseconds(MAX_PWM); 
  delayMicroseconds(1000);
}

void startStabalizer ()
{
  stabalizer.writeMicroseconds(MIN_PWM); 
  delayMicroseconds(1000);
}

void mapInputs ()
{
	pitch_output = map (pitch_input, -100, 100, MIN_PWM, MAX_PWM); 
	roll_output = map (roll_input, -100, 100, MIN_PWM, MAX_PWM); 
	throttle_output = map (throttle_input, 0, 100, MIN_PWM, MAX_PWM); 
	yaw_output = map (yaw_input, -100, 100, MIN_PWM, MAX_PWM); 
	if (arm_input)
	{
		if (!COPTER_ARMED)
		{
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
                        if (STABALIZED) 
                        {
                                quitStabalizer ();
                        }
		}
	}
}

void resetOutputs ()
{
	pitch_output = MID_PWM;
	roll_output = MID_PWM;
	throttle_output = MIN_PWM;
	yaw_output = MID_PWM;
	sendCommand ();
}

	
void parseSerial ()
{
	while (Serial.available() > 0) 
	{
		pitch_input = Serial.parseInt(); 
		yaw_input = Serial.parseInt(); 
		roll_input = Serial.parseInt(); 
		throttle_input = Serial.parseInt(); 
		arm_input = Serial.parseInt();

		if (Serial.read() == '\n') 
		{
			Serial.print(pitch_input);
			Serial.print (" ");
			Serial.print(yaw_input);
			Serial.print (" ");
			Serial.print(roll_input);
			Serial.print (" ");
			Serial.print(throttle_input);
			Serial.println(arm_input);
			Serial.print (" ");

			return;
		}
	}
}

void arm()
{
	if (throttle_output == MIN_PWM)
	{
		resetOutputs ();

		throttle_output = MIN_PWM;
		yaw_output = MIN_PWM;
		sendCommand();

		delay(2000);

		yaw_output = MID_PWM;
	}
}

void unarm()
{
	if (throttle_output == MIN_PWM)
	{
		resetOutputs ();

		throttle_output = MIN_PWM;
		yaw_output = MAX_PWM;
		sendCommand();

		delay(2000);

		yaw_output = MID_PWM;
	}
}

void sendCommand(){
    pitch_pin.writeMicroseconds(pitch_output); 
    delayMicroseconds(1000);   

    roll_pin.writeMicroseconds(roll_output);
    delayMicroseconds(1000); 

    throttle_pin.writeMicroseconds(throttle_output);
    delayMicroseconds(1000);

    yaw_pin.writeMicroseconds(yaw_output);
    delayMicroseconds(1000);
}

