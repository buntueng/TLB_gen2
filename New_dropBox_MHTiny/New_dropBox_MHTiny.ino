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
int solinoid_logic = 0;
int sticker_logic = 0;
unsigned char sticker_state = 0xFF;

void setup() {
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

  Read_sticker_detect();
  // mySerial.println(sticker_logic);
  mySerial.println(main_state);
  // mySerial.print(tube_drop_logic);
  // mySerial.print(",");
  // mySerial.println(stcick_logic);
  //========================================
  digitalWrite(tube_detect_pin,tube_drop_logic);
  digitalWrite(sticker_detect_pin,solinoid_logic);
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
          main_state = 0;
          state_timer = millis();
        }
        else
        {
          if(sticker_logic==0)
          {
            solinoid_logic = 0;
            on_motor_for();
            main_state = 3;
            // state_timer = millis();
          }
          else
          {
            on_motor_bac();
            delay(100);
            solinoid_logic = 0;
            main_state = 10;
          }
        }
        break;
      }
    case 3:
      {
        if (sticker_logic == 1)
        {
          off_motor();
          delay(100);
          on_motor_bac();
          main_state = 4;
        }
        break;
      }
    case 4:
    {
        if (sticker_logic == 0)
        {
          
          off_motor();
          delay(100);
          on_motor_bac();
          main_state = 5;
          state_timer = millis();
          // solinoid_logic = 1;
        }
      break;
    }
    case 5:
    {
      if(sticker_logic == 1)
      {
        delay(500);
        off_motor();
        main_state = 0;
        solinoid_logic = 1;
      }
      if((millis()-state_timer)>= 3000)
        {
          delay(500);
          off_motor();
          main_state = 0;
          solinoid_logic = 1;
        }
      break;
    }


    case 10:
    {
      on_motor_bac();
      main_state=11;
      break;
    }

    case 11:
    {
      if (sticker_logic == 0)
      {
        on_motor_bac();
        // off_motor();
        main_state = 12;
        state_timer = millis();
        // solinoid_logic = 1;
      }
      break;
    }

    case 12:
    {
      if(sticker_logic == 1)
      {
        delay(500);
        off_motor();
        main_state = 0;
        solinoid_logic = 1;
      }
      if((millis()-state_timer)>= 3000)
        {
          delay(500);
          off_motor();
          main_state = 0;
          solinoid_logic = 1;
        }
      break;
    }
    default:
      {
        main_state = 0;
      }
  }

}
void Read_sticker_detect(void)
  {
    sticker_state = ((sticker_state << 1) + digitalRead(sticker_detec_pin)) & 0xFF;
    if(sticker_state == 0xFE)
    {
      sticker_logic = 1;
    }
    else if(sticker_state == 0x7F)
    {
      sticker_logic = 0;
    }
  }
void off_motor(void)
  {
    digitalWrite(m1_pin1,LOW);
    digitalWrite(m1_pin2,LOW);
  }
void on_motor_for(void)
  {
    digitalWrite(m1_pin1,LOW);
    digitalWrite(m1_pin2,HIGH);
  }
void on_motor_bac(void)
  {
    digitalWrite(m1_pin1,HIGH);
    digitalWrite(m1_pin2,LOW);  
  }
