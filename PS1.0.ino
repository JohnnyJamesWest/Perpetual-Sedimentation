class Stepper{
  public:
  int   Step;
  int   Dir;
  unsigned long previousMicros;
  long  desired_interval;
  long  interval;
  int   Ena;
  int   microsteps;
  char  axis_name;
  long  steps_per_rev;
  bool  active;
  int   acceleration;


  public:
  Stepper(int s, int d, int e, int ms, int a, char an){
    Step = s;
    Dir = d;
    Ena = e;
    microsteps = ms;
    axis_name = an;
    steps_per_rev = 400 * microsteps;
    active = false;
    acceleration = a;
    interval = int((6000000000.0)/float(steps_per_rev * 1000)); // start rotation at 10rpm (*100)
    desired_interval = 3000;
    
    pinMode(Dir,OUTPUT);
    pinMode(Step,OUTPUT);
    pinMode(Ena,OUTPUT);
    digitalWrite(Ena,1);
    digitalWrite(Step,0);
    digitalWrite(Dir,0);
    previousMicros = 0;
  }
  
  void step_int(float rpm){
    desired_interval = int((6000000000.0)/float(steps_per_rev * rpm)); //rpm is actually r per 100 minutes (to avoid floating errors)
    interval = int((6000000000.0)/float(steps_per_rev * 1000)); // start rotation at 10rpm (*100)
  }

  void pumpF(long rpm){
    step_int(rpm);
    digitalWrite(Dir, 1);digitalWrite(Ena, 0);active = true;
  }

  void pump_off(){
    digitalWrite(Ena, 1); active = false; interval = int((6000000000.0)/float(steps_per_rev * 1000)); // start rotation at 10rpm
  }

  void pumpR(long rpm){
    step_int(rpm);
    digitalWrite(Dir, 0);digitalWrite(Ena, 0);active = true;
  }
  
  void update() {
    unsigned long currentMicros = micros();
    if (currentMicros - previousMicros >= max(desired_interval, interval) and active == true) {
      previousMicros = currentMicros; 
      digitalWrite(Step,1);
      digitalWrite(Step,0);
      if (interval > desired_interval){interval = max(interval - acceleration, desired_interval);}
    }
  }
};

class PS{
  public:
  int   Step;
  int   Dir;
  unsigned long previousMicros;
  long  interval;
  int   Ena;
  int   dir;
  int   acceleration;
  int   microsteps;
  char  axis_name;
  long  desiredPosition;
  long  currentPosition;
  long  steps_per_rev;
  bool  active;
  

  public:
  PS(int s, int d, int e, int ms, int a, char an){
    Step = s;
    Dir = d;
    Ena = e;
    microsteps = ms;
    acceleration = a;
    axis_name = an;
    steps_per_rev = 420*microsteps;        //motor has 400 steps but add a little extra here to account for play in the gears
    active = false;
    dir = 0;

    
    pinMode(Dir,OUTPUT);
    pinMode(Step,OUTPUT);
    pinMode(Ena,OUTPUT);
    digitalWrite(Ena,1);
    digitalWrite(Step,0);
    digitalWrite(Dir,0);
    previousMicros = 0;
    interval = 1000;
    currentPosition = steps_per_rev/2;
    desiredPosition = steps_per_rev;
  }
  
  void rpm(int r){interval = int((60000000.0)/float(steps_per_rev * r));}
  
  void on() {active = true; previousMicros = 0; digitalWrite(Ena, 0);}
  
  void off(){active = false; digitalWrite(Ena, 1);}
  
  void update() {
    unsigned long currentMicros = micros();
    if (currentMicros - previousMicros >= interval && active == true) {
      previousMicros = currentMicros; 

      if(currentPosition == desiredPosition){
        currentPosition = 0;
        if(dir == 1){dir = 0;}
        else {dir = 1;}
        digitalWrite(Dir, dir);
        }

      if (desiredPosition > currentPosition) {
        digitalWrite(Step,1);
        currentPosition = currentPosition + 1;
        digitalWrite(Step,0);
      }
    }
  }
};


//                                     step,  direction, enable, microsteps, acceleration, identifier
Stepper                      Syringe_C(54,    55,        38,     16,          100,            "C"); //cells
Stepper                      Syringe_B(60,    61,        56,     16,          100,            "B"); //beads
Stepper                      Syringe_O(46,    48,        62,     16,          100,            "O"); //oil
PS                           Rotation( 26,    28,        24,     8,           1000,           "R");


// serial commands
String device = "";
String command1 = "";
String command2 = "";
int serial_part = 0;


void checkSerial(){   
  char rc;
  while (Serial.available()) {
   rc = Serial.read();
   if      (rc == 47)         {serial_part = 1; device = "";command1 = "";command2 = "";}  // '/' char
   else if (rc == 46)         {serial_part += 1;}                                     // '.' char
   else if (rc == 59)         {respond(device,command1,command2); serial_part = 0;}   // ';' char
   else if (serial_part == 1) {device   += rc;}
   else if (serial_part == 2) {command1 += rc;}
   else if (serial_part == 3) {command2 += rc;}
 }
}

void respond(String device,String command1, String command2) {
    if(device == "af")         {Syringe_O.pumpF(command1.toInt());}
    if(device == "ar")         {Syringe_O.pumpR(command1.toInt());}
    if(device == "aoff")       {Syringe_O.pump_off();}
    if(device == "bf")         {Syringe_B.pumpF(command1.toInt());}
    if(device == "br")         {Syringe_B.pumpR(command1.toInt());}
    if(device == "boff")       {Syringe_B.pump_off();}
    if(device == "cf")         {Syringe_C.pumpF(command1.toInt());}
    if(device == "cr")         {Syringe_C.pumpR(command1.toInt());}
    if(device == "coff")       {Syringe_C.pump_off();}
    if(device == "on")         {Rotation.rpm(command1.toInt());Rotation.on();}
    if(device == "off")        {Rotation.off();}    
    if(device == "hello")      {Serial.println("Hi there");}
    if(device == "stop")       {Syringe_O.pump_off();Syringe_B.pump_off();Syringe_C.pump_off();Rotation.off();}  
  }

void setup() {Serial.begin(115200);}

void loop() {
  checkSerial();
  Syringe_O.update();
  Syringe_B.update();
  Syringe_C.update();
  Rotation.update();
}
