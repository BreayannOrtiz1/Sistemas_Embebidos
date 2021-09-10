		// Include all needed libraries here
#include <wiringPi.h>
#include <stdio.h>
		// No need to keep using “std”

int main()
{
wiringPiSetup();			// Setup the library

pinMode(1, OUTPUT);		// Configure GPIO1 as an input

// Main program loop
while(1)
{	// Button is pressed if digitalRead returns 0

	// Toggle the LED
	//digitalWrite(1, !digitalRead(1));
	digitalWrite(1,1);
	//delay(1000); 	// Delay 500ms
	digitalWrite(1,0);
	//delay(1000);
}
return 0;
}
