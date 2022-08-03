#include <Arduino.h>
#include <SoftwareSerial.h>
const byte txPin = A2;
const byte rxPin = A3;
SoftwareSerial mySerial (rxPin, txPin);
bool exe_cmd = false;
String cmd = "";

void check_message(void);
void execute_command(void);


void setup()
{
  mySerial.begin(9600);
  mySerial.println("FFF");
 
}

void loop()
{
  mySerial.listen();
  if (mySerial.available())
  {
    check_message();
  }
  //=================================
  if(exe_cmd)
  {
    execute_command();  
  }
  

}

void check_message(void)
{
  char data_in = mySerial.read();
    if(data_in == '\n')
    {
      exe_cmd = true;
    }
    else
    {
      cmd = cmd + String(data_in);
    }
}

void execute_command(void)
{
  switch(cmd[0])
  {
    case 'a':
    {
      mySerial.println("Got as");
      break;
    }
    case 'b':
    {
      mySerial.println("Got bs");
      break;
    }
    default:
    {
      
    }
  }
  exe_cmd = false;
  cmd = "";
}
