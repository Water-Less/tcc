import time
from tkinter import *
import requests
import json
from datetime import datetime, timedelta
import pandas
import tabulate
import matplotlib.pyplot as plt
import pandas as pd
import math
from datetime import date
from datetime import datetime
import numpy as np
#from pyfirmata import Arduino, util
import time
import serial

#import mysql.connector



    # Enter you api key, copies from the OpenWeatherMap dashboard
api_key = "63501f2da776b582cf3b722769b9a372"  # sample API

    # API url
weather_url = 'http://api.openweathermap.org/data/2.5/forecast?lat=-23.724064379441266&lon=-46.579354989752915&appid=63501f2da776b582cf3b722769b9a372&lang=pt_br'

#print (weather_url)

    # Get the response from fetched url
response = requests.get(weather_url)
#print (response)
    # changing response from json to python readable
weather_info = response.json()

#print (weather_info)

tomorrow1 = datetime.today().date() + timedelta(1)
data_em_texto = tomorrow1.strftime('%Y-%m-%d')
Hora=' 12:00:00'
tomorrow= data_em_texto + Hora
amanha=str(tomorrow)
print(tomorrow)

    #    for tomorrow in weather_info['list']:
   #for each in weather_info['list']:
          # print (each['dt_txt'])
          # print (f"Temp = {round(float((each['main']['temp']-273.15)),2)}ºC")
         #  print (f"Pressão = {round(float((each['main']['pressure']/1013)),2)} atm")
         #  print (f"Umidade = {round(float((each['main']['humidity'])),2)} %")
         #  print (f"Descrição = {each['weather'][0]['description']}")

       # plt.plot((each['dt_txt']),(round(float((each['main']['temp']-273)),2)),
           #  marker = 'o')

#plt.show()

#df = pd.read_json('response.json')

#df_csv = weather_url.to_csv('tabela_tempo.csv')

#print(df_csv)

tabela= pd.DataFrame(weather_info["list"])
#print(tabela)

interesse = tabela.loc[3]

temperatura=interesse['main']['temp']-273.1

Pressao=interesse['main']['pressure']/1013

Umidade =interesse['main']['humidity']

Descricao =interesse['weather'][0]['description']

rain=Descricao

#print(temperatura)
#print(Pressao)
#print(Umidade)
#print(Descricao)

#calculo de evapotranspiração do solo

Hoje = tabela.loc[1]

#print(Hoje)

day_corr = date.today().toordinal() - date(date.today().year,1,1).toordinal()
tmax =Hoje['main']['temp_max']-273.1 # tmax is maximum temperature for the day
tmin = Hoje['main']['temp_min']-273.1 # tmin is the minimum temperature for the day
tmed = (tmax+tmin)/2 #
rhmax = Hoje['main']['humidity'] #  rhmax is the maximum relative humidity for the day
v_med = Hoje['wind']['speed']# v_med is the average wind velocity Km/h
alt_v = 2 # alt_v is the altitute from the ground that the wind speed is collected.
rhmed = rhmax


url = "http://api.openweathermap.org/data/2.5/weather?id=3449344&appid=1b43995d45e76484eac79c54b28ad885&units=metric"
payload = {}
headers= {}
response = requests.request("GET", url, headers=headers, data = payload)
r = response.json()
n = datetime.fromtimestamp(r['sys']['sunset']) - datetime.fromtimestamp(r['sys']['sunrise'])
n = n.total_seconds()/3600 # n is the actual duration of sunshine [hour]



# day_corr is the current date in the range 1 to 365
elev = 801  # Elevation from sea level. Used the city of São Bernardo- São Paulo - Brazil. Change if needed.
p = 92.183188  # Atmospheric Pressure use eq 101.3*math.pow((293-0.0065*elev)/293,5.26). Used the city of São Bernardo- São Paulo - Brazil. Change if needed.
phi = -0.414081215084  # latitude in radians.  Used the city of São Bernardo- São Paulo - Brazil. Change if needed.
y = 0.665 * math.pow(10, -3) * p  # y is the psycometric constant
dr = 1 + 0.033 * math.cos((2 * math.pi * day_corr) / 365)  # Dr is Relative Distance Earth-Sun
delt = 0.409 * math.sin(((2 * math.pi * day_corr) / 365) - 1.39)  # Delt is solar declination
e0_tmax = 0.6108 * math.pow(math.e, (
            (17.27 * tmax) / (tmax + 237.3)))  # eo_tmax is saturation vapor pressure for the max air temperature
e0_tmin = 0.6108 * math.pow(math.e, (
            (17.27 * tmin) / (tmin + 237.3)))  # eo_tmin is saturation vapor pressure for the min air temperature
es = (e0_tmax + e0_tmin) / 2  # es is the mean saturation vapor pressure
D = (4098 * (0.6108 * math.pow(math.e, ((17.27 * tmed) / (tmed + 237.3))))) / math.pow((tmed + 237.3),
                                                                                       2)  # D is Slope Vapor Pressure Curve
ea = es * rhmed / 100  # ea us actual vapor pressure considering an average relative humidity
ws = math.acos(-math.tan(phi) * math.tan(delt))  # Ws is sunset hour angle
ra = 37.5860314 * dr * ((ws * math.sin(phi) * math.sin(delt)) + (
            math.cos(phi) * math.cos(delt) * math.sin(ws)))  # Ra is Extraterrestrial Radiation
rs = (0.25 + (0.5 * (n / (7.6394 * ws)))) * ra  # *0.408 Rs is solar radiation
rns = 0.77 * rs  # rns ius Net Shortwave Radiation
rso = (0.75 * ra)  # Rso is Clear Sky Solar Radiation
f_rs_rso = rs / rso
if f_rs_rso > 1:
    f_rs_rso = 1
rnl = (4.903 * math.pow(10, -9)) * ((math.pow((tmax + 273.16), 4) + math.pow((tmin + 273.16), 4)) / 2) * (
            0.34 + (-0.14 * math.sqrt(ea))) * ((1.35 * (f_rs_rso)) - 0.35)  # Rnl is Net Long Wave Radiation
r_n = rns - rnl  # Rn is Neet Radiation
g = 0
uz = v_med * 1000 / 3600  # uz is Wind Speed measured at Z height in m/s
u2 = uz * (4.87 / (math.log(67.8 * alt_v - 5.42)))  # u2 is is wind speed at 2m above ground
et_o = ((0.408 * D * (r_n - g) + y * (900 / (tmed + 273)) * u2 * (es - ea)) / (D + y * (1 + 0.34 * u2))) / 0.85  # Calculate daily evapotranspiration based on the values before

#print(et_o)

#calculo do Kc

#das = date.today().toordinal() - datetime.strptime(response['SeedingDay'], '%Y-%m-%dT%H:%M:%S.%fZ').toordinal()
i=20
tomorrow2 = datetime.today().date() - timedelta(i)
data_inicial=tomorrow2.toordinal()
print(data_inicial)
das=datetime.today().toordinal() -data_inicial

print(das)

#r = requests.request("GET", url, headers=headers, data=payload).json()
kc = 0
IniDays = 5 #Duração do estágio inicial do cultivo
DevDays = 5 #Duração do estágio de desenvolvimento do cultivo
MidDays = 10#Duração do estágio intermediário do cultivo
LateDays = 3 #Duração do estágio final do cultivo
IniKc = 0.3 # Fator do cultivo do estágio inicial do cultivo
MidKc = 1.2 # Fator do cultivo do estágio intermediário do cultivo
LateKc = 0.35 #Fator do cultivo do estágio final do cultivo

if das <= IniDays:
    kc = IniKc
elif das > IniDays and das <= IniDays + DevDays:
    kc = IniKc + ((MidKc - IniKc) * (das - IniDays)) / (DevDays)
elif das > IniDays + DevDays and das <= IniDays + DevDays + MidDays:
    kc = MidKc
elif das > IniDays + DevDays + MidDays and das <= IniDays + DevDays + MidDays + LateDays:
    kc = LateKc + ((MidKc - LateKc) * (IniDays + DevDays + MidDays + LateDays - das)) / (LateDays)
else:
    print('error')

#print(kc)

#Calculo da evapotranspiração da cultura

Et_c=et_o*kc

print(Et_c)

#calculo de quantidade de irrigação

# x=1 para chuva ou X=0 sem chuva

if rain == "Chuva": #Vai chover hoje?
    x=1

else:
    x=0

if rain == "Chuva": #Vai chover amanhã?
    x=1

else:
    x=0

#print(x)

if x==1:

    Tempo_irrigacao=0
else:
    Vazao_aspersor= 0.08  #l/s
    #buscar informação de quantiade de aguá no solo
    #descontar quantidade de aguá por necessidade corrigida pelo Kc da fase milho
    #tempo de irrigação sera Et_c-quantidade de água do solo / vazão
    #Tempo_irrigação= Et_c/Vazao_aspersor #milisegundos
    #print(Tempo_irrigação)

import serial # instalar pyserial


porta = 'COM5' #Olhar qual tá conectado
Velocidade = 115200


conecao = serial.Serial(porta, Velocidade, timeout=0.1)
time.sleep(10)
print('conectou')

while True:
    opcao = 0

    if opcao == 0:   # ativa apenas quando não vai chover
        conecao.write(bytes('a', 'utf-8'))
        time.sleep(10)
        print("deu certo")
        solo = conecao.readline()
        time.sleep(1)
        str_solo = solo.decode('utf-8')
        filtered_data = bytes(filter(lambda x: x != 0, solo))
        time.sleep(3)
        print(str_solo)
        print(filtered_data)
        if solo == 'u':
            time.sleep(10)
            conecao.close()
        if solo == 'm':
            conecao.write(bytes('l', 'utf-8')) #ligar valvula solenoide
            time.sleep (Tempo_irrigacao)
            conecao.write(bytes('d', 'utf-8')) #desligar valvula solenoide
            time.sleep(2)
            conecao.close()
        if solo == 's':
            conecao.write(bytes('l', 'utf-8'))  # ligar valvula solenoide
            time.sleep(Tempo_irrigacao)
            conecao.write(bytes('d', 'utf-8'))  # desligar valvula solenoide
            time.sleep(2)
            conecao.close()

    time.sleep(3)

    #conecao.write(bytes('b', 'utf-8'))
    time.sleep(3)

conecao.close()