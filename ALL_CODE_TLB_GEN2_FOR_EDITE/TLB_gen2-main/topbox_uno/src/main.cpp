#include<main.hpp>
char node_ID = '2';
SoftwareSerial mySerial (rxPin, txPin);
bool exe_cmd_status = false;
String cmd = "";

// ========== defined roller speed and time rolling constant =========
const int rolling_time = 200;              // 2000 micro seconds
const int rolling_constant = 1500;        // time to rolling forward or backward
const int rolling_constant2 = 200;
// ========== silo control bits =====
bool run_silo1 = false;
int silo1_state = 0;
bool motor_silo1_logic = 0;
unsigned long silo1_timer = 0;
unsigned long silo1_logic_timer = 0;

bool run_silo2 = false;
int silo2_state = 0;
bool motor_silo2_logic = 0;
unsigned long silo2_timer = 0;
unsigned long silo2_logic_timer = 0;

bool run_silo3 = false;
int silo3_state = 0;
bool motor_silo3_logic = 0;
unsigned long silo3_timer = 0;
unsigned long silo3_logic_timer = 0;

bool run_silo4 = false;
int silo4_state = 0;
bool motor_silo4_logic = 0;
unsigned long silo4_timer = 0;
unsigned long silo4_logic_timer = 0;

void setup()
{
  mySerial.begin(9600);
  setup_ios();
}

void loop()
{
  mySerial.listen();
  if (mySerial.available())
  {
    check_message();
  }
  //========= check execute cmd =================
  if(exe_cmd_status)
  {
    execute_command();  
  }
  //======== run roller under silo1 ==============
  if(run_silo1)
  {
    if (micros()-silo1_logic_timer>=rolling_time)
    {
      motor_silo1_logic = !motor_silo1_logic;
      digitalWrite(X_STEP_pin,motor_silo1_logic);
      silo1_logic_timer = micros();
    }
    switch(silo1_state)
    {
      case 0:
      {
        if (millis() - silo1_timer >= rolling_constant)
        {
          digitalWrite(X_DIR_pin,LOW);
          silo1_timer = millis();
          silo1_state = 1;
        }
        break;
      }
      case 1:
      {
        if (millis() - silo1_timer >= 100)
        {
          silo1_timer = millis();
          silo1_state = 2;
        }
        break;
      }
      case 2:
      {
        if (millis() - silo1_timer >= rolling_constant2)
          {
            digitalWrite(X_DIR_pin,HIGH);
            silo1_timer = millis();
            silo1_state = 3;
          }
        break;
      }
      case 3:
      {
        if (millis() - silo1_timer >= 100)
        {
          silo1_timer = millis();
          silo1_state = 0;
        }
        break;
      }
      default:
      {
        silo1_state = 0;
        run_silo1 = false;
      }
    }
  }
  //======== run roller under silo2 ==============
  if(run_silo2)
  {
    if (micros()-  silo2_logic_timer >= rolling_time)
    {
      motor_silo2_logic = !motor_silo2_logic;
      digitalWrite(Y_STEP_pin,motor_silo2_logic);
      silo2_logic_timer = micros();
    }
    switch(silo2_state)
    {
      case 0:
      {
        if (millis() - silo2_timer >= rolling_constant)
        {
          digitalWrite(Y_DIR_pin,HIGH);
          silo2_timer = millis();
          silo2_state = 1;
        }
        break;
      }
      case 1:
      {
        if (millis() - silo2_timer >= 50)
        {
          silo2_state = 2;
          silo2_timer = millis();
        }
        break;
      }
      case 2:
      {
        if (millis() - silo2_timer >= rolling_constant2)
          {
            digitalWrite(Y_DIR_pin,LOW);
            silo2_timer = millis();
            silo2_state = 3;
          }
        break;
      }
      case 3:
      {
        if (millis() - silo2_timer >= 50)
        {
          silo2_state = 0;
          silo2_timer = millis();
        }
        break;
      }
      default:
      {
        silo2_state = 0;
        run_silo2 = false;
      }
    }
  }
  //======== run roller under silo3 ==============   
  if(run_silo3)
  {
    if (micros()-silo3_logic_timer>=rolling_time)
    {
      motor_silo3_logic = !motor_silo3_logic;
      digitalWrite(Z_STEP_pin,motor_silo3_logic);
      silo3_logic_timer = micros();
    }
    switch(silo3_state)
    {
      case 0:
      {
        if (millis() - silo3_timer >= rolling_constant)
        {
          digitalWrite(Z_DIR_pin,HIGH);
          silo3_timer = millis();
          silo3_state = 1;
        }
        break;
      }
      case 1:
      {
        if (millis() - silo3_timer >= 100)
        {
          silo3_timer = millis();
          silo3_state = 2;
        }
        break;
      }
      case 2:
      {
        if (millis() - silo3_timer >= rolling_constant2)
          {
            digitalWrite(Z_DIR_pin,LOW);
            silo3_timer = millis();
            silo3_state = 3;
          }
        break;
      }
      case 3:
      {
        if (millis() - silo3_timer >= 100)
        {
          silo3_timer = millis();
          silo3_state = 0;
        }
        break;
      }
      default:
      {
        silo3_state = 0;
        run_silo3 = false;
      }
    }
  }
  //======== run roller under silo4 ==============
  if(run_silo4)
  {
    if (micros()-silo4_logic_timer>=rolling_time)
    {
      motor_silo4_logic = !motor_silo4_logic;
      digitalWrite(A_STEP_pin,motor_silo4_logic);
      silo4_logic_timer = micros();
    }
    switch(silo4_state)
    {
      case 0:
      {
        if (millis() - silo4_timer >= rolling_constant)
        {
          digitalWrite(A_DIR_pin,HIGH);
          silo4_timer = millis();
          silo4_state = 1;
        }
        break;
      }
      case 1:
      {
        if(millis()-silo4_timer >= 50)
        {
          silo4_state = 2;
          silo4_timer = millis();
        }
        break;
      }
      case 2:
      {
        if (millis() - silo4_timer >= rolling_constant2)
          {
            digitalWrite(A_DIR_pin,LOW);
            silo4_timer = millis();
            silo4_state = 3;
          }
        break;
      }
      case 3:
      {
        if(millis()-silo4_timer >= 50)
        {
          silo4_state = 0;
          silo4_timer = millis();
        }
        break;
      }
      default:
      {
        silo4_state = 0;
        run_silo4 = false;
      }
    }
  }
}

void check_message(void)
{
  char data_in = mySerial.read();
    if(data_in == '\n')
    {
      exe_cmd_status = true;
    }
    else
    {
      cmd = cmd + String(data_in);
    }
}

void execute_command(void)
{
  //mySerial.println(cmd);
  if (cmd[0] == node_ID)
  {
    switch(cmd[1])
    {
      case '1':
      {
        mySerial.println("2Box1");
        silo1_state = 0;
        run_silo1 = true;
        run_silo2 = false;
        run_silo3 = false;
        run_silo4 = false;
        silo1_timer = millis();
        //digitalWrite(EN_pin,LOW);
        break;
      }
      case '2':
      {
        mySerial.println("2Box2");
        silo2_state = 0;
        run_silo1 = false;
        run_silo2 = true;
        run_silo3 = false;
        run_silo4 = false;
        silo2_timer = millis();
        //digitalWrite(EN_pin,LOW);
        break;
      }
      case '3':
      {
        mySerial.println("2Box3");
        run_silo1 = false;
        run_silo2 = false;
        run_silo3 = true;
        run_silo4 = false;
        silo3_timer = millis();
        //digitalWrite(EN_pin,LOW);
        break;
      }
      case '4':
      {
        mySerial.println("2Box4");
        silo4_state = 0;
        run_silo1 = false;
        run_silo2 = false;
        run_silo3 = false;
        run_silo4 = true;
        silo4_timer = millis();
       // digitalWrite(EN_pin,LOW);
        break;
      }
      default:
      {
        run_silo1 = false;
        run_silo2 = false;
        run_silo3 = false;
        run_silo4 = false;
        //digitalWrite(EN_pin,HIGH);
      }
    }
  }
  exe_cmd_status = false;
  cmd = "";
}



void setup_ios(void)
{
  pinMode(A_DIR_pin,OUTPUT);
  pinMode(A_STEP_pin,OUTPUT);
  pinMode(X_DIR_pin,OUTPUT);
  pinMode(X_STEP_pin,OUTPUT);
  pinMode(Y_DIR_pin,OUTPUT);
  pinMode(Y_STEP_pin,OUTPUT);
  pinMode(Z_DIR_pin,OUTPUT);
  pinMode(Z_STEP_pin,OUTPUT);
  digitalWrite(X_DIR_pin,HIGH);
  digitalWrite(Y_DIR_pin,LOW);
  digitalWrite(Z_DIR_pin,LOW);
  digitalWrite(A_DIR_pin,LOW);
<<<<<<< HEAD
}
=======
}
>>>>>>> 5c539a3b9cc7af5045deca035c3a320306f3427f
