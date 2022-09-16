#define pwma PA11 //lewy - a
#define ain2 PB13
#define ain1 PB14
#define bin1 PB15 //prawy - b
#define bin2 PA8
#define pwmb PB6
//powyzej nazwy silnikow

//------------zmienne do odbierania danych sterowania--------
char buff[5];
byte count;
int crc,b1,b2,b3=0;
char lewy='0';
char prawy='0';

int v=90; //predkosc
char potwierdzenieSilniki='0';

//---------------zmienne do wysylania------------------
int d2=0;//odczyty czujnikow
int d3=0;
int d4=0;
int d5=0;
int d6=0;
int d7=0;
//1-biale 0-czarne

char czujnik[6];//0-1 odczytu czujnika
char msg[10]={'~','0','0','0','0','0','0','0','0','\n'};

unsigned long aktualnyCzas = 0;
unsigned long zapCzas1 = 0;
unsigned long zapCzas2 = 0;

void setup() 
{
  Serial.begin(9600);
  Serial.setTimeout(0.1);
  delay(30000);

  pinMode(PC13,OUTPUT);

  //------Wyjscia Mostka-----
  pinMode(PA11, OUTPUT);//pwmA
  pinMode(PB13,OUTPUT);//ain2
  digitalWrite(PB13, LOW);
  pinMode(PB14,OUTPUT);//ain1
  digitalWrite(PB14, LOW);
  pinMode(PB15,OUTPUT);//bin1
  digitalWrite(PB15, LOW);
  pinMode(PA8,OUTPUT);//bin2
  digitalWrite(PA8, LOW);
  pinMode(PB6,OUTPUT);//pwmB

  //ustawienie pwm predkosci
  analogWrite(pwma,v);
  analogWrite(pwmb,v); 

}

void loop() 
{
  aktualnyCzas=millis();

  if(aktualnyCzas - zapCzas1 >=50UL)
  {
        zapCzas1=aktualnyCzas;
       //-----------------------------------------odbieranie danych sterowania-----------
      while(Serial.available()>0)
        {
              buff[0]=Serial.read();
              
              if(buff[0]=='~')
              {
                    count=1;
                
                    while(count<5)
                    {
                          if(Serial.available()>0)
                          {
                              buff[count]=Serial.read();
                              count++;
                          }
                    }
                
                    if(count=5 && buff[4]=='#')
                    {
                          b1=buff[1]-'0';
                          b2=buff[2]-'0';
                          crc=((b1+b2)*(b1+b2)*177)%7;
                          b3=buff[3]-'0';
                          if(crc==b3)
                          {
                              lewy=buff[1];
                              prawy=buff[2];
                              potwierdzenieSilniki=kodowanie(lewy,prawy);
                          }
                    }
              }
          
        }
    //----------------------------wysterowanie silnikow-----------------------
      //------LEWY-----A
      if(lewy=='3')//przod
        {
        digitalWrite(ain1, HIGH);
        digitalWrite(ain2, LOW);
        }
      else if(lewy=='2')//tył
        {
        digitalWrite(ain1, LOW);
        digitalWrite(ain2, HIGH);
        }
      else//lewy soft hamowanie
        {
        digitalWrite(ain1, LOW);
        digitalWrite(ain2, LOW);    
        }
      //-----PRAWY------B
      if(prawy=='3')//przod
        {
        digitalWrite(bin1, HIGH);
        digitalWrite(bin2, LOW);
        }
      else if(prawy=='2')//tył
        {
        digitalWrite(bin1, LOW);
        digitalWrite(bin2, HIGH);    
        }
      else//prawy soft hamowanie
        {
        digitalWrite(bin1, LOW);
        digitalWrite(bin2, LOW);    
        } 
  }


    if(aktualnyCzas - zapCzas2 >=30UL)
  {
        zapCzas2=aktualnyCzas;

       //-------------------------------sekcja wysylajaca---------------
      odczyt();//d7=czujnik[0]...d2=czujnik[5]
    
      byte j;
      for(j=0; j<6; j++)
      {
        msg[j+1]=czujnik[j];
      }
      msg[7]='0';
      msg[8]=potwierdzenieSilniki;
      turn(msg);
  }

}

//------------------------funkcja wysylajaca---------------------
void turn(char fn[10])
{
  char chk=0;
  int crc=0;
  byte i;
  
  for(i=0; i<6; i++)
  {
    crc=crc+(fn[i+1]-'0');
  }
  chk=crc+'0';
  fn[7]=chk;
  
  for(i=0; i<11; i++)
  {
    Serial.write(fn[i]);
  }
}
//----------------------------funkcja odczytujaca dane z czunikow-----------
void odczyt()
{
d2=analogRead(PA1);
if(d2<3000)
  {
      czujnik[5]='1';
  }
else{czujnik[5]='0';}

d3=analogRead(PA2);
if(d3<2900)
  {
      czujnik[4]='1';
  }
else{czujnik[4]='0';}

d4=analogRead(PA3);
if(d4<120)
  {
      czujnik[3]='1';
  }
else{czujnik[3]='0';}

d5=analogRead(PA4);
if(d5<2900)
  {
      czujnik[2]='1';
  }
else{czujnik[2]='0';}
d6=analogRead(PA5);
if(d6<2700)
  {
      czujnik[1]='1';
  }
else{czujnik[1]='0';}

d7=analogRead(PA6);
if(d7<4035)
  {
      czujnik[0]='1';
  }
else{czujnik[0]='0';}

}

char kodowanie(char l, char p)
{
  int zwrot=0;
  if(l=='3' && p=='3')zwrot='1';
  else if(l=='3' && p=='2')zwrot='2';
  else if(l=='3' && p=='1')zwrot='3';
  else if(l=='2' && p=='3')zwrot='4';
  else if(l=='2' && p=='2')zwrot='5';
  else if(l=='2' && p=='1')zwrot='6';
  else if(l=='1' && p=='3')zwrot='7';
  else if(l=='1' && p=='2')zwrot='8';
  else if(l=='1' && p=='1')zwrot='9';
  return zwrot;
}
