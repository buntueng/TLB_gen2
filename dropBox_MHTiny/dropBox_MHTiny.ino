#include <SoftwareSerial.h>
const int RX = 4;
const int TX = 5;
SoftwareSerial mySerial(RX, TX);
// ========== motor pin ======================
const int m1_pin1 = 10;
const int m1_pin2 = 11;
// ========== output to main controller ======
const int sticker_detect_pin = 12;
const int tube_detect_pin = 13;
//======== sticker detect sensor ============
const int sticker_detec_pin = 6;
// ========== drop tube sensors =======
const int tube_detect_pin1 = 7;
const int tube_detect_pin2 = 8;
const int tube_detect_pin3 = 9;
// ============ subfunctions ========
void off_motor(void);
void on_motor_for(void);
void on_motor_bac(void);

bool tube_drop_logic = false;
bool sticker_detect_logic = false;

unsigned long state_timer = 0;
unsigned int main_state = 0;

void setup() 
  {
    mySerial.begin(9600);
    pinMode(m1_pin1,OUTPUT);
    pinMode(m1_pin2,OUTPUT);
    off_motor();
    pinMode(sticker_detect_pin,OUTPUT);
    pinMode(tube_detect_pin,OUTPUT);
    pinMode(sticker_detec_pin,INPUT);
    pinMode(tube_detect_pin1,INPUT);
    pinMode(tube_detect_pin2,INPUT);
    pinMode(tube_detect_pin3,INPUT);
  }

void loop()
{
  // ========= get input sensors ===========
  tube_drop_logic = digitalRead(tube_detect_pin1) && digitalRead(tube_detect_pin2) && digitalRead(tube_detect_pin3);
  sticker_detect_logic = digitalRead(sticker_detec_pin);
  mySerial.print(tube_drop_logic);
  mySerial.print(",");
  mySerial.println(sticker_detect_logic);
  //========================================
  digitalWrite(tube_detect_pin,tube_drop_logic);
  // digitalWrite(sticker_detect_pin,sticker_detect_logic);
  // =========== run state machine =========
  switch(main_state)
  {
    case 0:
    {
      if(tube_drop_logic==0)
      {
        main_state = 1;
        state_timer = millis();
      }
      break;
    }
    case 1:
    {
      if((millis()-state_timer)>=500)
      {
        main_state = 2;
        state_timer = millis();
      }
      break;
    }
    case 2:
    {
      if((millis()-state_timer)>= 500)
      {
        if(sticker_detect_logic==0)
        {
          main_state = 3;
          state_timer = millis();
        }
        else 
        {
          on_motor_for();
        }
        if((millis()-state_timer)>= 10000)
        {
          main_state = 3;
          state_timer = millis();
        }
      }
      // if((millis()-state_timer)>= 500)
      // {
      //   main_state = 0;
      //   state_timer = millis();
      // }
      // else
      // {
      //   if(sticker_detect_logic==1)
      //   {
      //     on_motor_for();
      //     main_state = 3;
      //     state_timer = millis();
      //   }
      //   else
      //   {
      //     main_state = 0;
      //     off_motor();
      //   }
      // }
      break;
    }
    case 3:
    {
      digitalWrite(sticker_detect_pin,sticker_detect_logic);
      off_motor();
      main_state = 0;
      // if((millis()-state_timer)>=2000)
      // {
      //   off_motor();
      //   main_state = 0;
      // }
      // if (sticker_detect_logic == 0)
      // {
      //   off_motor();
      //   delay(50);
      //   on_motor_for();
      //   delay(70);
      //   on_motor_bac();
      //   delay(10);
      //   off_motor();
      //   main_state = 0;
      // }
      break;
    }
    default:
    {
      main_state = 0;
    }
  }
}

void off_motor(void)
  {
    digitalWrite(m1_pin1,LOW);
    digitalWrite(m1_pin2,LOW);
  }
void on_motor_for(void)
  {
    digitalWrite(m1_pin1,HIGH);
    digitalWrite(m1_pin2,LOW);
  }
void on_motor_bac(void)
  {
    digitalWrite(m1_pin1,LOW);
    digitalWrite(m1_pin2,HIGH);  
  }
