int valve_out=11;
int value=0;
int pressure=0;
//int pin=4;
//int frequency=0;
//int t1=0;

void setup()
{
  setPwmFrequency(valve_out,8);
  analogWrite(valve_out,value);
//  pinMode(pin,OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  int a1,a2;
  char a;
  Serial.println("Please input pressure:");
  while(Serial.available()<=0){}
  while(Serial.available()>0)
  {
    a=Serial.read();
    int b=int(a)-48;
    pressure=pressure*10+b;
    delay(10);
  }
//  pressure=(pressure-a)/10;
  Serial.print("pressure=");
  Serial.println(pressure);
  value=int(pressure*10/(0.2*10000)*255);
  Serial.print("value=");
  Serial.println(value);    
  analogWrite(valve_out,value);
  pressure=0;

//  Serial.println("Please input frequency:");
//  frequency=0;
//  while(Serial.available()<=0){}
//  while(Serial.available()>0)
//  {
//    a=Serial.read();
//    frequency=frequency*10+a-48;
//    delay(10);
//  }
//  frequency=(frequency-a+48)/10;
//  Serial.print("frequency=");
//  Serial.println(frequency);
//  t1=int(500/frequency);
//  Serial.print("period=");
//  Serial.println(2*t1);
//  while(1)
//  {
//    a1=digitalRead(switch_pin);
//    delay(10);
//    a2=digitalRead(switch_pin);
//    if(a1&&a2)
//    {
//      break;
//    }
//  }
//  while(1)
//  {
//    digitalWrite(pin,HIGH);
//    delay(t1);
//    digitalWrite(pin,LOW);
//    delay(t1);
//  }
}

void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    } else {
      TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x7; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}
