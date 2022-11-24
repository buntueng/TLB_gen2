//#include <SoftwareSerial.h>
//const int RX = 13;
//const int TX = 14;
//SoftwareSerial mySerial(RX, TX);

const int got_tube_pin = 0;

const int sensor1_pin = 3;
const int sensor2_pin = 4;
const int sensor3_pin = 5;
const int sensor4_pin = 6;        // check sticker on tube

const int control1_pin = 7;       // drop tube process
const int control2_pin = 8;       // get tube process

const int motor1_pin1 = 9;         // drop tube
const int motor1_pin2 = 10;
const int motor2_pin = 11;        // small roller motor

const int solinoid1_pin = 12;     // lock tube
const int solinoid2_pin = 13;     // shaft of roller motor

byte control1_state = 0xFF;
byte control2_state = 0xFF;
bool run_drop_tube = false;
int run_drop_tube_state = 0;
bool run_get_tube = false;
int run_get_tube_state = 0;
bool got_tube_sensor = false;

void run_get_tube_machine(void);
void run_drop_tube_machine(void);
void open_lock_motor(void);
void close_lock_motor(void);
void stop_lock_motor(void);
unsigned long drop_tube_timer = 0;
unsigned long get_tube_timer = 0;
void setup()
{
  pinMode(sensor1_pin,INPUT_PULLUP);
  pinMode(sensor2_pin,INPUT_PULLUP);
  pinMode(sensor3_pin,INPUT_PULLUP);
  pinMode(sensor4_pin,INPUT_PULLUP);

  pinMode(control1_pin,INPUT_PULLUP);
  pinMode(control2_pin,INPUT_PULLUP);

  pinMode(motor1_pin1,OUTPUT);
  pinMode(motor1_pin2,OUTPUT);
  pinMode(motor2_pin,OUTPUT);

  pinMode(solinoid1_pin,OUTPUT);
  pinMode(solinoid2_pin,OUTPUT);

  pinMode(got_tube_pin,OUTPUT);

  //============================
  stop_lock_motor();
  digitalWrite(got_tube_pin,HIGH);            // tube not detect
  
}

void loop()
{
  control1_state = ((control1_state<<1)&0xFF)+digitalRead(control1_pin);
  control2_state = ((control2_state<<1)&0xFF)+digitalRead(control2_pin);
  got_tube_sensor = !((digitalRead(sensor1_pin)) & (digitalRead(sensor2_pin)) & (digitalRead(sensor3_pin)));
  //========== check state ==========
  if(control1_state == 0xF0) 
  {
    run_drop_tube_state = 0;
    run_drop_tube = true;
    drop_tube_timer = millis();
  }

  if(control2_state == 0xF0)
  {
    run_get_tube_state = 0;
    run_get_tube = true;
    get_tube_timer = millis();
  }
  // =================================
  if(run_drop_tube)
  {
    run_drop_tube_machine();
  }
  if(run_get_tube)
  {
    run_get_tube_machine();
  }
}


// ================== sub program ===============
void run_get_tube_machine(void)
{
  switch(run_get_tube_state)
  {
    case 0:
    {
      if(millis()-get_tube_timer >= 50)
      {
        digitalWrite(solinoid1_pin,HIGH);     // on lock tube solinoid
        run_get_tube_state = 1;
        get_tube_timer = millis();
      }
      break;
    }
    case 1:
    {
      if(millis()-get_tube_timer >= 500)
      {
        digitalWrite(solinoid1_pin,LOW);     // off lock tube solinoid
        run_get_tube_state = 2;
        get_tube_timer = millis();
      }
      break;
    }
    case 2:
    {
      if(millis()-get_tube_timer >= 100)
      {
        run_get_tube_state = 3;
        get_tube_timer = millis();
      }
      break;
    }
    case 3:
    {
      if(millis()-get_tube_timer >= 100)
      {
        
      }
      break;
    }
    case 4:
    {
      break;
    }
    case 5:
    {
      break;
    }
    case 6:
    {
      break;
    }
    case 7:
    {
      break;
    }
    default:
    {
      
    }
  }
  
}


void run_drop_tube_machine(void)
{
  switch(run_drop_tube_state)
   {
    case 0:     // wait for a while
    {
      if(millis()-drop_tube_timer >= 100)
      {
        run_drop_tube_state = 1;
      }
      break;
    }
    case 1:
    {
      open_lock_motor();
      run_drop_tube_state = 2;
      drop_tube_timer = millis();
      break;
    }
    case 2:
    {
      if(millis()-drop_tube_timer>=1000)
      {
        run_drop_tube_state = 3;
        stop_lock_motor();
        drop_tube_timer = millis();
      }
      break;
    }
    case 3:
    {
      if(millis()-drop_tube_timer>=100)
      {
        run_drop_tube_state = 4;
        close_lock_motor();
        drop_tube_timer = millis();
      }
      break;
    }
    case 4:
    {
      if(millis()-drop_tube_timer>= 1000)
      {
        run_drop_tube_state = 5;
        stop_lock_motor();
      }
      break;
    }
    case 5:
    {
      break;
    }
    default:
    {
      
    }
  }
  
}


//====================== control lock motor ===========
void open_lock_motor(void)
{
  digitalWrite(motor1_pin1,HIGH);
  digitalWrite(motor1_pin2,LOW);
}
void close_lock_motor(void)
{
  digitalWrite(motor1_pin1,LOW);
  digitalWrite(motor1_pin2,HIGH);
}
void stop_lock_motor(void)
{
  digitalWrite(motor1_pin1,LOW);
  digitalWrite(motor1_pin2,LOW);
}
