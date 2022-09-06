#include <FastAccelStepper.h>
#include "initval.h"

/*
\\Author: Roman Popov
*/

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepper_1 = NULL;
FastAccelStepper *stepper_2 = NULL;
FastAccelStepper *stepper_3 = NULL;

void btnIsr1(){
  if(stepper_1->isRunning())
    stepper_1->forceStop();
}
void btnIsr2(){
  if(stepper_2->isRunning())
    stepper_2->forceStop();
}
void btnIsr3(){
  if(stepper_3->isRunning())
    stepper_3->forceStop();
}

void gotoX(int32_t pos){
  int32_t current_pos = stepper_1->getCurrentPosition();
  int32_t steps;
  if(pos>current_pos && minX <= current_pos  <= maxX)
  {
    steps = pos - current_pos;
  }else if(pos<current_pos && minX <= current_pos  <= maxX){
    steps = current_pos - pos;
  } else {
    steps = 0;
  }
  stepper_1->setSpeedInUs(default_speed);
  stepper_1->setAcceleration(default_acceleration);
  stepper_1->move(steps);
}
void gotoY(int32_t pos){
  int32_t current_pos = stepper_2->getCurrentPosition();
  int32_t steps;
  if(pos>current_pos && minY <= current_pos <= maxY)
  {
    steps = pos - current_pos;
  }else if(pos<current_pos && minY <= current_pos <= maxY){
    steps = current_pos - pos;
  } else {
    steps = 0;
  }
  stepper_2->setSpeedInUs(default_speed);
  stepper_2->setAcceleration(default_acceleration);
  stepper_2->move(steps);
}
void gotoZ(int32_t pos){
  int32_t current_pos = stepper_3->getCurrentPosition();
  int32_t steps;
  if(pos > current_pos && minZ <= current_pos <= maxZ)
  {
    steps = pos - current_pos;
  }else if(pos<current_pos && minZ <= current_pos <= maxZ){
    steps = current_pos - pos;
  } else {
    steps = 0;
  }
  stepper_3->setSpeedInUs(default_speed);
  stepper_3->setAcceleration(default_acceleration);
  stepper_3->move(steps);
}

void go_x(int32_t val){
  int32_t current_pos = stepper_1->getCurrentPosition();
  stepper_1->setSpeedInHz(10000);
  stepper_1->setAcceleration(1000);
  if(minX <= current_pos <= maxX)
  {
    stepper_1->move(val);
  } 
  else {
    if(stepper_1->isRunning())
      stepper_1->forceStop();
  }  
}
void go_y(int32_t val){
  int32_t current_pos = stepper_2->getCurrentPosition();
  stepper_2->setSpeedInHz(10000);
  stepper_2->setAcceleration(1000);
  if(minZ <= current_pos <= maxZ)
  {
    stepper_2->move(val);
  } 
  else {
    if(stepper_2->isRunning())
      stepper_2->forceStop();
  }
}
void go_z(int val){
  int32_t current_pos = stepper_3->getCurrentPosition();
  stepper_3->setSpeedInHz(10000);
  stepper_3->setAcceleration(default_acceleration);
  if(minZ <= current_pos <= maxZ)
  {
    stepper_3->move(val);
  } 
  else {
    if(stepper_3->isRunning())
      stepper_3->forceStop();
  }  
}

void stop_all(){
    stepper_1->forceStop();
    stepper_2->forceStop();
    stepper_3->forceStop();
}

void setup() {

  engine.init();

  Serial.begin(9600);
  
  pinMode(interruptPin_2, INPUT);
  attachInterrupt(3, btnIsr2, FALLING);
  pinMode(interruptPin_3, INPUT);
  attachInterrupt(1, btnIsr3, FALLING);
  pinMode(interruptPin_1, INPUT);
  attachInterrupt(2, btnIsr1, FALLING);

  stepper_1 = engine.stepperConnectToPin(FirstStepPin);
  stepper_2 = engine.stepperConnectToPin(SecondStepPin);
  stepper_3 = engine.stepperConnectToPin(ThreeStepPin);

  if (stepper_1) {
      stepper_1->setDirectionPin(FirstDirPin);
      stepper_1->setEnablePin(enableFirstPin);
      stepper_1->setAutoEnable(true);
   }
  if(stepper_2){
      stepper_2->setDirectionPin(SecondDirPin);
      stepper_2->setEnablePin(enableSecondPin);
      stepper_2->setAutoEnable(true);
   }
    if(stepper_3){
      stepper_3->setDirectionPin(ThreeDirPin);
      stepper_3->setEnablePin(enableThreePin);
      stepper_3->setAutoEnable(true);
  }
}

void loop() {
  char str[24]{};
  String compar[10];
  if (Serial.available()) {
    int i = 0;
    int size_data = Serial.readBytesUntil(';', str, 20);
    str[size_data] = NULL;

    char sep [10]=":";
    char *istr;
    istr = strtok (str,sep);

    while (istr != NULL)
    {
      String val = String(istr);
      compar[i] = val;
      istr = strtok (NULL,sep);
      i++;
    }
    if(compar[0] == "gotomax"){
      Serial.println("go "+ String(compar[1])+" to X");
      go_x(1000000);
      go_y(1000000);
      go_z(1000000);
    } 
    if(compar[0] == "gotomin"){
      Serial.println("go "+ String(compar[1])+" to X");
      go_x(-1000000);
      go_y(-1000000);
      go_z(-1000000);
    } 
    else if(compar[0] == "maxx"){
      Serial.println("Set max x "+ String(compar[1]));
      maxX = compar[1].toInt();
    } 
    else if(compar[0] == "maxy"){
      Serial.println("Set max y "+ String(compar[1])); 
      maxY = compar[1].toInt();
    }
    else if(compar[0] == "maxz"){
      Serial.println("Set max z "+ String(compar[1]));
      maxZ = compar[1].toInt();
    }
    else if(compar[0] == "minx"){
      Serial.println("Set min x "+ String(compar[1])); 
      minX = compar[1].toInt();
    }
    else if(compar[0] == "miny"){
      Serial.println("Set min y "+ String(compar[1]));
      minY = compar[1].toInt();
    }
    else if(compar[0] == "minz"){
      Serial.println("Set min z "+ String(compar[1]));
      minZ = compar[1].toInt();
    }
    else if(compar[0] == "goxr"){
      Serial.println("go rx "+ String(compar[1])); 
      go_x(compar[1].toInt());
    }
    else if(compar[0] == "goyr"){
      Serial.println("go ry "+ String(compar[1])); 
      go_y(compar[1].toInt());
    }
    else if(compar[0] == "gozr"){
      Serial.println("go rz "+ String(compar[1])); 
      go_z(compar[1].toInt());
    }
    else if(compar[0] == "gozl"){
      Serial.println("go lz "+ String(compar[1]));
      go_z(compar[1].toInt()* -1);
    }
    else if(compar[0] == "goxl"){
      Serial.println("go lx "+ String(compar[1]));
      go_x(compar[1].toInt()*l_direction);
    }
    else if(compar[0] == "goyl"){
      Serial.println("go ly "+ String(compar[1]));
      go_y(compar[1].toInt()*l_direction); 
    }
    else if(compar[0] == "gox"){
      Serial.println("go lx "+ String(compar[1]));
      go_x(compar[1].toInt()*l_direction);
    }
    else if(compar[0] == "goy"){
      Serial.println("go ly "+ String(compar[1]));
      go_y(compar[1].toInt()*l_direction); 
    }
    else if(compar[0] == "goz"){
      Serial.println("go lz "+ String(compar[1]));
      go_z(compar[1].toInt()*l_direction);
    }
    else if(compar[0] == "setacc"){
      default_acceleration = compar[1].toInt();
    }
    else if (compar[0] == "setsp"){
      default_speed = compar[1].toInt();
    }
    else if (compar[0] == "stop"){
      Serial.println("Stop all");
      stop_all();
    }
    else {
      Serial.println("Wrong command");  
    }
    }
  }
