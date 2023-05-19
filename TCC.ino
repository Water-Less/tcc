//Incluindo Bibliotecas
#include <Wire.h>
#include <Adafruit_BMP280.h>
Adafruit_BMP280 bmp; //I2C
#include "dht.h" 
#define pino_sinal_analogico A0

const int pinoDHT11 = A2; //PINO ANALÓGICO UTILIZADO PELO DHT11
const int RelePin = 7; // pino ao qual o Módulo Relé está conectado

dht DHT; //VARIÁVEL DO TIPO DHT

int valor_analogico;
int incomingByte;      // variavel para ler dados recebidos pela serial


void setup()
{
  Serial.begin(9600);
  pinMode(RelePin, OUTPUT); //seta o pino como saída
  pinMode(pino_sinal_analogico, INPUT);
  digitalWrite(RelePin, LOW); // seta o pino com nivel logico baixo
  if (!bmp.begin(0x76)) { /*Definindo o endereço I2C como 0x76. Mudar, se necessário, para (0x77)*/
    
    //Imprime mensagem de erro no caso de endereço invalido ou não localizado. Modifique o valor 
   // Serial.println(F(" Não foi possível encontrar um sensor BMP280 válido, verifique a fiação ou "
                   //   "tente outro endereço!"));
    while (1) delay(10);
  }
}

void loop()
{
  DHT.read11(pinoDHT11); //LÊ AS INFORMAÇÕES DO SENSOR DHT11
  //Serial.print("Umidade: "); //IMPRIME O TEXTO NA SERIAL
  //Serial.print(DHT.humidity); //IMPRIME NA SERIAL O VALOR DE UMIDADE MEDIDO AR
  //Serial.print("%"); //ESCREVE O TEXTO EM SEGUIDA
  //Serial.print(" / Temperatura: "); //IMPRIME O TEXTO NA SERIAL
  //Serial.print(DHT.temperature, 0); //IMPRIME NA SERIAL O VALOR DE UMIDADE MEDIDO E REMOVE A PARTE DECIMAL
  //Serial.println("*C"); //IMPRIME O TEXTO NA SERIAL

  //Imprimindo os valores de Pressão
  //Serial.print(F("Pressão = "));
  //Serial.print(bmp.readPressure());
  //Serial.println(" Pa");
  //Imprimindo os valores de Altitude Aproximada
  //Serial.print(F("Altitude Aprox = "));
  //Serial.print(bmp.readAltitude(1013.25)); /* Ajustar a pressão de nível do mar de acordo com o local!*/
  //Serial.println(" m");
  //Tempo de espera de 1 segundo
  //Serial.println();

  //Le o valor do pino A0 do sensor
  valor_analogico = analogRead(pino_sinal_analogico);
 
  //Mostra o valor da porta analogica no serial monitor
  //Serial.print("Porta analogica: ");
  //Serial.print(valor_analogico);
 
  //Solo umido
  if (valor_analogico > 0 && valor_analogico < 600)
  {
    Serial.println('u');
    Serial.flush();                                             // Função que garante que a informação se mantenha no barramento até ser enviada completamente.
    delay(1000);
  }
 
  //Solo com umidade moderada
  if (valor_analogico > 600 && valor_analogico < 800)
  {
    Serial.println('m'); 
  }
 
  //Solo seco
  if (valor_analogico > 800 && valor_analogico < 1024)
  {
    Serial.print('s');
    Serial.flush();                                             // Função que garante que a informação se mantenha no barramento até ser enviada completamente.
    delay(1000);
  }
  //Acionamento da válvula solenoide
  if (Serial.available() > 0) {
    // verifica se tem algum dado na serial
    incomingByte = Serial.read();  //lê o primeiro dado do buffer da serial

    if (incomingByte == 'l') {     //se for l
      digitalWrite(RelePin, HIGH); //aciona o pino
    } 

    if (incomingByte == 'd') {     //se for d
      digitalWrite(RelePin, LOW);  //desativa o pino
    }
  }
  delay(20000);
}
