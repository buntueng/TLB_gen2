char node_id = '7';
bool execute_cmd = false;
String cmd = "";
bool wait_clear_button = false;
bool button_pressed_status = false;
char button_state = 0xFF;
void setup() {

  pinMode(5,INPUT_PULLUP);
  // put your setup code here, to run once:
  pinMode(16,OUTPUT);  // relay 1
  pinMode(14,OUTPUT);  // relay 2
  pinMode(12,OUTPUT);  // relay 3
  pinMode(13,OUTPUT);  // relay 4

  digitalWrite(16,HIGH);
  digitalWrite(14,HIGH);
  digitalWrite(12,HIGH);
  digitalWrite(13,HIGH);
  Serial.begin(115200);

}

void loop() {
  if(Serial.available())
  {
    char cmd_byte = Serial.read();
    if(cmd_byte == '\n')
    {
      execute_cmd = true;
    }
    else
    {
      cmd = cmd + cmd_byte;
    }
  }
  //====================== execute ==================
  if(execute_cmd)
  {
    if((cmd.length()>=3)&&(cmd[0] == node_id))
    {
      switch(cmd[1])
      {
        case 'o':  // turn on or turn off lamps
        {
          Serial.println(cmd);
          switch(cmd[2])
          {
            case '1':
            {
              wait_clear_button = true;
              button_pressed_status = false;
              button_state = 0xFF;
              digitalWrite(16,LOW);
              break;
            }
            case '2':
            {
              wait_clear_button = true;
              button_pressed_status = false;
              button_state = 0xFF;
              digitalWrite(14,LOW);
              break;
            }
            case '3':
            {
              wait_clear_button = true;
              button_pressed_status = false;
              button_state = 0xFF;
              digitalWrite(12,LOW);
              break;
            }
            case '4':
            {
              wait_clear_button = true;
              button_pressed_status = false;
              button_state = 0xFF;
              digitalWrite(13,LOW);
              break;
            }
            case '5':
            {
              break;
            }
            case '6':
            {
              break;
            }
            default:
            {
              wait_clear_button = false;
              // turn off all lamps
              digitalWrite(16,HIGH);
              digitalWrite(14,HIGH);
              digitalWrite(12,HIGH);
              digitalWrite(13,HIGH);
            }
          }
          break;
        }
        case 'f':
        {
          if(button_pressed_status)
          {
            cmd[2] = '1';
            button_pressed_status = false;
          }
          else
          {
            cmd[2] = '0';
          }
          Serial.println(cmd);
          break;
        }
        default:
        {
          // do nothing
        }
      }
      
    }
    execute_cmd = false;
    cmd = "";
  }


  if(wait_clear_button)
  {
    button_state = (button_state<<1) + digitalRead(5);
    if(button_state == 0xF0)
    {
      button_pressed_status = true;
      wait_clear_button = false;
      // turn off all lamps
      digitalWrite(16,HIGH);
      digitalWrite(14,HIGH);
      digitalWrite(12,HIGH);
      digitalWrite(13,HIGH);
    }
  }
}
