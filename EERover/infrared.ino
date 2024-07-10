// Define the pin where the signal is connected
const int signalPin = A0;

// Variables to hold the current and last state of the signal pin
float pulseCount=0;
float pulse;
int threshold=40;
int frequency_count_d = 0;
int frequency_count_a = 0;

// Timestamps to calculate the elapsed time
unsigned long startTime;
unsigned long elapsedTime;

// Frequency calculation variables
float frequency;
float frequency_before;
float frequency_after;

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);

  // Set the signal pin as input
  pinMode(signalPin, INPUT);

  startTime = millis();
}

void loop() {
  elapsedTime = millis() - startTime;
  pulse = analogRead(signalPin);
  if(pulse > threshold){
    pulseCount += 1;
  }
  while(pulse > threshold){
     pulse = analogRead(signalPin);
  }
  if(elapsedTime >= 1000){
    frequency = (float)pulseCount / (elapsedTime / 1000.0);
    Serial.println(frequency);
    pulseCount = 0;
    startTime = millis();
  }
  
  if(560 < frequency && frequency < 580){
    frequency_count_a += 1;
    frequency_count_d = 0;
  }
  else if(340 < frequency && frequency < 360){
    frequency_count_d +=  1;
    frequency_count_a = 0;
  }
  else{
    frequency_count_d = 0;
    frequency_count_a = 0;
  }
  
  if(frequency_count_a >= 10){
    Serial.println("Abronia");
    frequency_count_a = 0;
  }
  else if(frequency_count_d >= 10){
    Serial.println("Dixonious");
    frequency_count_d = 0;
  }
}
