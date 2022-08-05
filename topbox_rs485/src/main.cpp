#include<main.hpp>
char node_ID = '1';
SoftwareSerial mySerial (rxPin, txPin);
bool exe_cmd_status = false;
String cmd = "";

// ========== defined roller speed and time rolling constant =========
const int rolling_time = 2000;            // 20 micro seconds
const int rolling_constant = 2000;
// ========== silo control bits =====
bool run_silo1 = false;
bool silo1_state = 0;
bool motor_silo1_logic = 0;
unsigned long silo1_timer = 0;
unsigned long silo1_logic_timer = 0;

bool run_silo2 = false;
bool silo2_state = 0;
bool motor_silo2_logic = 0;
unsigned long silo2_timer = 0;
unsigned long silo2_logic_timer = 0;

bool run_silo3 = false;
bool silo3_state = 0;
bool motor_silo3_logic = 0;
unsigned long silo3_timer = 0;
unsigned long silo3_logic_timer = 0;

bool run_silo4 = false;
bool silo4_state = 0;
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
    if(silo1_state)
    {
      digitalWrite(X_DIR_pin,HIGH);
      if (millis() - silo1_timer >= rolling_constant)
      {
        silo1_timer = millis();
        silo1_state = 1;
      }
    }
    else
    {
      digitalWrite(X_DIR_pin,LOW);
      if (millis() - silo1_timer >= rolling_constant)
        {
          silo1_timer = millis();
          silo1_state = 0;
        }
    }
  }
  //======== run roller under silo2 ==============
  if(run_silo2)
  {
    if (micros()-silo2_logic_timer>=rolling_time)
    {
      motor_silo2_logic = !motor_silo2_logic;
      digitalWrite(Y_STEP_pin,motor_silo2_logic);
      silo2_logic_timer = micros();
    }
    if(silo2_state)
    {
      digitalWrite(Y_DIR_pin,HIGH);
      if (millis() - silo2_timer >= rolling_constant)
      {
        silo2_timer = millis();
        silo2_state = 1;
      }
    }
    else
    {
      digitalWrite(Y_DIR_pin,LOW);
      if (millis() - silo2_timer >= rolling_constant)
        {
          silo2_timer = millis();
          silo2_state = 0;
        }
    }
  }
        
  if(run_silo3)
  {
    if (micros()-silo3_logic_timer>=rolling_time)
    {
      motor_silo3_logic = !motor_silo3_logic;
      digitalWrite(Z_STEP_pin,motor_silo3_logic);
      silo3_logic_timer = micros();
    }
    if(silo3_state)
    {
      digitalWrite(Z_DIR_pin,HIGH);
      if (millis() - silo3_timer >= rolling_constant)
      {
        silo3_timer = millis();
        silo3_state = 1;
      }
    }
    else
    {
      digitalWrite(Z_DIR_pin,LOW);
      if (millis() - silo3_timer >= rolling_constant)
        {
          silo3_timer = millis();
          silo3_state = 0;
        }
    }
  }

  if(run_silo4)
  {
    if (micros()-silo4_logic_timer>=rolling_time)
    {
      motor_silo4_logic = !motor_silo4_logic;
      digitalWrite(A_STEP_pin,motor_silo4_logic);
      silo4_logic_timer = micros();
    }
    if(silo4_state)
    {
      digitalWrite(A_DIR_pin,HIGH);
      if (millis() - silo4_timer >= rolling_constant)
      {
        silo4_timer = millis();
        silo4_state = 1;
      }
    }
    else
    {
      digitalWrite(A_DIR_pin,LOW);
      if (millis() - silo4_timer >= rolling_constant)
        {
          silo4_timer = millis();
          silo4_state = 0;
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
  mySerial.println(cmd);
  if (cmd[0] == node_ID)
  {
    switch(cmd[1])
    {
      case '1':
      {
        mySerial.println("Box1");
        silo1_state = 0;
        run_silo1 = true;
        run_silo2 = false;
        run_silo3 = false;
        run_silo4 = false;
        silo1_timer = millis();
        digitalWrite(EN_pin,LOW);
        break;
      }
      case '2':
      {
        mySerial.println("Box2");
        silo2_state = 0;
        run_silo1 = false;
        run_silo2 = true;
        run_silo3 = false;
        run_silo4 = false;
        silo2_timer = millis();
        digitalWrite(EN_pin,LOW);
        break;
      }
      case '3':
      {
        mySerial.println("Box3");
        run_silo1 = false;
        run_silo2 = false;
        run_silo3 = true;
        run_silo4 = false;
        silo3_timer = millis();
        digitalWrite(EN_pin,LOW);
        break;
      }
      case '4':
      {
        mySerial.println("Box4");
        silo4_state = 0;
        run_silo1 = false;
        run_silo2 = false;
        run_silo3 = false;
        run_silo4 = true;
        silo4_timer = millis();
        digitalWrite(EN_pin,LOW);
        break;
      }
      default:
      {
        run_silo1 = false;
        run_silo2 = false;
        run_silo3 = false;
        run_silo4 = false;
        digitalWrite(EN_pin,HIGH);
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
}