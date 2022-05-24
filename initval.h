#ifndef initval_h
#define initval_h

//Initialize Pins
//First motion
#define FirstStepPin    10
#define enableFirstPin  3
#define FirstDirPin     4       
//second motion
#define SecondStepPin   9
#define SecondDirPin    6
#define enableSecondPin 8
//third motion
#define ThreeStepPin    11
#define ThreeDirPin     12
#define enableThreePin  13
//Interrupt pins
#define interruptPin_1  0
#define interruptPin_2  1
#define interruptPin_3  2
#define directionPin_1  7

volatile int32_t default_speed = 1000;
volatile int32_t default_acceleration = 100;

volatile int32_t maxX = 10000;
volatile int32_t minX = 0;
volatile int32_t maxY = 10000;
volatile int32_t minY = 0;
volatile int32_t maxZ = 10000;
volatile int32_t minZ = 0;
int32_t l_direction = -1;



#endif