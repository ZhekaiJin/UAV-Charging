// define the pin connections first 
const int microphonePin= A0; //the microphone positive terminal will connect to analog pin A0 to be read
const int Red=13; //define the three LED determing noise level
const int Yellow=12;
const int Green=11;

int sample; //the variable that will hold the value read from the microphone each time

const double AnalogQuiet = 50; // define boundary condition for three cases
const double AnalogModerate = 400;
const double AnalogLoud = 1022;

void setup() {
    pinMode (Red, OUTPUT); // put pins  to output mode for lED output
    pinMode (Yellow, OUTPUT);
    pinMode (Green, OUTPUT);
    Serial.begin(9600); //coordinate with serial monitor 
    while (! Serial); 
    Serial.println("Enter 'x' to start");
}

//Serial.println(sample);
void loop(){
  if (Serial.available()){
      digitalWrite (Green, LOW);    // specify LED conditions
      digitalWrite(Yellow, LOW);
      digitalWrite(Red, LOW);
      char ch = Serial.read();
      if (ch == 'x'){
         while(1){
            sample= analogRead(microphonePin); //the arduino takes continuous readings from the microphone
            if ((sample > AnalogQuiet) && (sample < AnalogModerate))  //if the reading is greater than the threshold value, LED turns on
            {
                digitalWrite (Green, HIGH);    // specify LED conditions
                digitalWrite(Yellow, LOW);
                digitalWrite(Red, LOW);
            
                delay (50);         //LED stays on for a 0.05 s
                digitalWrite (Green, LOW);  //LED turns off
                
                Serial.print("Quiet. Value: ");   // input to serial monitor
                Serial.print(sample);
                Serial.print('\n');
            
            }
             else if ((sample > AnalogModerate) && ( sample <= AnalogLoud) )  // same case for the moderate volume
             {
                digitalWrite(Green, LOW);
                digitalWrite(Yellow, HIGH);
                digitalWrite(Red, LOW);
                delay (50); 
                digitalWrite (Yellow, LOW); 
                
                Serial.print("Moderate. Value: ");
                Serial.print(sample);
                Serial.print('\n');
            } 
            
             else if (sample> AnalogLoud )   // same case for the moderate volume
             
             {
                digitalWrite(Green, LOW);
                digitalWrite(Yellow, LOW);
                digitalWrite(Red, HIGH);
                delay (50); //LED stays on for a 0.05 s
                digitalWrite (Red, LOW); //LED turns off
                
                Serial.print("Loud. Value: ");
                Serial.print(sample);
                Serial.print('\n');
            
             }
          }
       }
    }
}  


