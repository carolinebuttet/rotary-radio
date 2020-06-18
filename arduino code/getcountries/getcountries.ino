//Rotary radio : Turn your phone into a radio!
//Find the instructions on the arduino blog: https://create.arduino.cc/projecthub/carolinebuttet/rotary-musical-phone-14fd79
//This script detects which of the jack pins has a connector in it. 
//It then sends ou the information via serial

//We set the active pin to a number that will never match any country
int activePin = -10 ;

//We declare the dgital pins that are used by our countries
//Those pins are connected to the 3.3v on one side (Left) and to a digital pin (through a 10k pulldown resistor) on the other side (Right). 
//If the reading is HIGH, the jack is empty
//If the reading is LOW, the jack has a country connected.
int countries[] = {11,10,9,8,7,6,5,4,3,2};

//The total number of countries
int numCountries = 10;

//The countries are matched with a string label (Country code). 
///For example,  pin 11 matches NZ (New Zealand)
//Note that you can of course edit this list to add the countries your want. 
String labels[] = {"NZ", "JP", "RU", "MD", "UK", "FR", "TU", "US", "CL", "ML" };

void setup() {
  //Start the serial communications
  Serial.begin(9600);

  //Loop through the countries pins and initialize them as INPUT
  for (int i = 0; i <= sizeof countries; i++) {
    pinMode(i, INPUT);
  }
  
}

void loop() {
  int countryCount = 0;
  //Read all the input pins
  for (int i = 0; i <= numCountries ; i++) {
    int state = digitalRead(countries[i]);
    //When the state of a pin is LOW, we know that there is a connector in this pin. 
    //So that means that this country is selected.
    if(state == 0){
      countryCount = 0;
      if(i != activePin){
        //We send out the information via serial if the active pin has changed
        Serial.println(labels[i]);
      }
      //We set this pin as active pin
      activePin = i;
     }
     else if(state == 1){
      //No country is selected
      countryCount ++;
      if(countryCount == numCountries+1){
        activePin = -10;
       }
     }
  }
  //Delay for better stability
  delay(100);  
}
