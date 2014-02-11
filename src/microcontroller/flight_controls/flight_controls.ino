#include <Servo.h>

#define NUM_MOTORS 4
#define MIN_PWM 800
#define MID_PWM 1499
#define MAX_PWM 2197

Servo pitch_pin; 
Servo roll_pin;
Servo throttle_pin;
Servo yaw_pin;

int pitch_input = 0;
int roll_input = 0;
int throttle_input = 0;
int yaw_input = 0;

int pitch_output = 0;
int roll_output = 0;
int throttle_output = 0;
int yaw_output = 0;

void setup(){
	pitch_pin.attach(A5);   	
	roll_pin.attach(A4);
	throttle_pin.attach(A3);
	yaw_pin.attach(A2);

	resetOutputs ();

	arm();

	resetOutputs ();

	Serial.begin(9600);
}


void loop()
{
	parseSerial ();

	sendCommand ();
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
		z_input = Serial.parseInt(); 

		if (Serial.read() == '\n') 
		{
			Serial.print(pitch_input);
			Serial.print (" ");
			Serial.print(yaw_input);
			Serial.print (" ");
			Serial.print(roll_input);
			Serial.print (" ");
			Serial.println(z_input);
			return;
		}
	}
}

void arm(){
	throttle_output = MIN_PWM;
	yaw_output = MIN_PWM;
	sendCommand();

	delay(2000);

	yaw_output = MID_PWM;
}

void unarm(){
    temp[0] = control_vector[yaw];
    //temp[1] = control_vector[roll];
    //temp[2] = control_vector[pitch];
    //control_vector[roll] = 1950;
    //control_vector[pitch] = 1950;
    control_vector[yaw] = 1950;
    sendCommand();
    delay(2000);
    control_vector[yaw] = temp[0];
    //control_vector[roll] = temp[1];
    //control_vector[pitch] = temp[2];
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

