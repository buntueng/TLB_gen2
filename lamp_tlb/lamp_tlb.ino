const int relay1 = 16;
const int relay2 = 14;
const int relay3 = 12;
const int relay4 = 13;
bool execute_cmd = false;
bool Start_Lamp = false;
int select_lamp = 0;
String cmd_string;

void setup()
  {
    Serial.begin(9600);
    pinMode(relay1, OUTPUT);
    pinMode(relay2, OUTPUT);
    pinMode(relay3, OUTPUT);
    pinMode(relay4, OUTPUT);
  }
void loop() 
  {
    if(Serial.available())
      {
        char input_char = Serial.read(); 
        if(input_char=='\n')
        {  
          execute_cmd = true;
        }
        else
        {
          cmd_string.concat(input_char);
        }
        // Serial.println(input_char);
      }
    if(execute_cmd)
      {
        int cmd_len = cmd_string.length();
        switch(cmd_string[0])
          {
            case 'R':
              {
                switch(cmd_string[1])
                  {
                    case '0':
                      {
                        STOP_ALL_LAMP();
                        select_lamp = 0;
                        Start_Lamp = false;

                        break;
                      }
                    case '1':
                      {
                        select_lamp = 1;
                        Start_Lamp = true;
                        break;
                      }
                    case '2':
                      {
                        select_lamp = 2;
                        Start_Lamp = true;
                        break;
                      }
                    case '3':
                      {
                        select_lamp = 3;
                        Start_Lamp = true;
                        break;
                      }
                    case '4':
                      {
                        select_lamp = 4;
                        Start_Lamp = true;
                        break;
                      }
                    default:
                      {
                        STOP_ALL_LAMP();
                        select_lamp = 0;
                        Start_Lamp =false;
                        break;
                      }
                    // break;
                  }
                break;
              }
            default:
              {
                break;
              }
          }
          execute_cmd = false;
          cmd_string = "";
      }
    if(Start_Lamp)
      {
        switch (select_lamp) 
          {
            case 1:
              {
                R1();
                // Serial.println("R1");
                break;
              }
            case 2:
              {
                R2();
                // Serial.println("R2");
                break;
              }
            case 3:
              {
                R3();
                // Serial.println("R3");
                break;
              }
            case 4:
              {
                R4();
                // Serial.println("R4");
                break;
              }
            default:
              {
                STOP_ALL_LAMP();
                Serial.println("ERROR");
                break;
              }
          }
      }
  }

void R1(void)
  {
    digitalWrite(relay1,HIGH);
  }
void R2(void)
  {
    digitalWrite(relay2,HIGH);
  }
void R3(void)
  {
    digitalWrite(relay3,HIGH);
  }
void R4(void)
  {
    digitalWrite(relay4,HIGH);
  }
void STOP_ALL_LAMP(void)
  {
    digitalWrite(relay1,LOW);
    digitalWrite(relay2,LOW);
    digitalWrite(relay3,LOW);
    digitalWrite(relay4,LOW);
  }
