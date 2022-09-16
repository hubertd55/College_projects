#include <WiFi.h>
#include <FirebaseESP32.h>
#include <string.h>
#include "DHT.h"
#include "time.h"

#define FIREBASE_HOST "***"
#define FIREBASE_AUTH "***"

#define WIFI_SSID "***"
#define WIFI_PASSWORD "***"

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

FirebaseData firebaseData;
FirebaseJson json;

float h =0;
float t = 0;
int s=55;

String dataa;
String godzina;
String temp;
int silnik;
int probka;
bool flaga=false;

// setting PWM properties
const int freq = 50;
const int ledChannel = 0;
const int resolution = 8;

//-----------------do NTP
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 3600;
const int daylightOffset_sec = 3600;

void setup() 
{
  Serial.begin(9600);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");

  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
 
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
  Firebase.setReadTimeout(firebaseData, 1000 * 60);
  Firebase.setwriteSizeLimit(firebaseData, "tiny");


  Serial.println("------------------------------------");
  Serial.println("Connected...");

  // Init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  dht.begin();

  delay(2000);

  // configure LED PWM functionalitites
  ledcSetup(ledChannel, freq, resolution);
  ledcAttachPin(14, ledChannel);
  
  pinMode(32, OUTPUT);
  pinMode(33, OUTPUT);

  digitalWrite(33,HIGH);//IN1
  digitalWrite(32,HIGH);//IN2
  ledcWrite(14,0);//PWMA


}


void loop() 
{

//---------------------------------- Ponieranie danych o silniku i próbkowaniu------------------------------------
 if( Firebase.getInt(firebaseData,"/Properties/WentylatorS") )
{
  silnik=firebaseData.intData();
}
Serial.println("silnik:");
Serial.println(silnik);

if( Firebase.getInt(firebaseData,"/Properties/TemperaturaON") )
{
  probka=firebaseData.intData();
}
Serial.println("probka:");
Serial.println(probka);

  h = dht.readHumidity();
  t = dht.readTemperature();
  s=analogRead(34);
  
  Serial.println("temperatura:");
  Serial.println(t);
  delay(500);


  // Sprawdza czy ktorys odczyt sie nie udal, jesli tak to ponawia odczyt
  if (isnan(h) || isnan(t)) 
  {
    Serial.print("\nFailed to read from DHT sensor!\n");
    return;
  }

//-------------------------------sterowanie prędkością silnika-----------------------------------------------------
if(t>probka)
{
  digitalWrite(32,LOW);
  if(silnik==0)
{
  ledcWrite(14,0);//PWMA
}
else if(silnik==1)
{
  ledcWrite(14,120);//PWMA
}
else if(silnik==2)
{
  ledcWrite(14,200);//PWMA
}
else if(silnik==3)
{
  ledcWrite(14,255);//PWMA
}

}
else
{
    ledcWrite(14,0);//PWMA
    Serial.println("testowo");
    88555588digitalWrite(32,HIGH);    
}



//-------------------------------------Pobieranie czasu-------------------------------------------------

  dataa="";
  godzina="";
  temp=printLocalTime();

  dataa=dataa+temp[20];
  dataa=dataa+temp[21];
  dataa=dataa+temp[22];
  dataa=dataa+temp[23];
  dataa=dataa+'-';
  dataa=dataa+temp[4];
  dataa=dataa+temp[5];
  dataa=dataa+temp[6];
  dataa=dataa+'-';
  if(temp[8]==' ')dataa=dataa+'0';
  else dataa=dataa+temp[8];
  dataa=dataa+temp[9];
  for(int i=0;i<5;i=i+1)
  {
    godzina=godzina+temp[11+i];
  }
  


//---------------------------------------pobieranie odczytów oraz wysyłanie ich do bazy----------------------------------

if(godzina[3]=='0' && godzina[4]=='0' && flaga==true)
{
  wysylanie_danych();
  flaga=false;
}

if(godzina[3]=='0' && godzina[4]=='5' && flaga==true)
{
  flaga=true;
}


Serial.println("---");

delay(1000);
}

void wysylanie_danych()
{

json.set("naslonecznienie", s);  
json.set("temperatura", t);
json.set("wilgotnosc", h);
Firebase.pushJSON(firebaseData,"/"+dataa+"/"+godzina,json); 
}

String printLocalTime()
{
  String temp;
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
  }
  temp=asctime(&timeinfo);

  return temp;
}
